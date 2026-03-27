with hourly_inputs as (
    select
        zone_hour_key,
        zone_code,
        timestamp_hour_utc,
        entsoe_generation_mwh,
        wind_speed_10m,
        shortwave_radiation,
        temperature_2m,
        quality_flag
    from {{ ref('fct_zone_hour_resilience_inputs') }}
),

fuel_rollup as (
    select
        zone_code,
        timestamp_hour_utc,
        sum(generation_mwh) as ember_total_generation_mwh,
        sum(
            case
                when lower(fuel_category) in (
                    'wind',
                    'solar',
                    'hydro',
                    'geothermal',
                    'biomass',
                    'renewables'
                ) then generation_mwh
                else 0
            end
        ) as renewable_gen_mwh
    from {{ ref('fct_zone_hour_fuel_generation') }}
    group by 1, 2
),

joined as (
    select
        h.zone_hour_key,
        h.zone_code,
        h.timestamp_hour_utc,
        h.entsoe_generation_mwh as total_gen_mwh,
        least(coalesce(f.renewable_gen_mwh, 0.0), coalesce(h.entsoe_generation_mwh, 0.0)) as renewable_gen_mwh,
        h.wind_speed_10m,
        h.shortwave_radiation,
        h.temperature_2m,
        h.quality_flag
    from hourly_inputs h
    left join fuel_rollup f
      on f.zone_code = h.zone_code
     and f.timestamp_hour_utc = h.timestamp_hour_utc
),

kpis as (
    select
        zone_hour_key,
        zone_code,
        timestamp_hour_utc,
        total_gen_mwh,
        renewable_gen_mwh,
        coalesce(total_gen_mwh, 0.0) - coalesce(renewable_gen_mwh, 0.0) as non_renewable_gen_mwh,
        100.0 * renewable_gen_mwh / nullif(total_gen_mwh, 0.0) as renewable_share_pct,
        (coalesce(total_gen_mwh, 0.0) - coalesce(renewable_gen_mwh, 0.0)) * 0.45 as co2_proxy_tonnes,
        ((coalesce(total_gen_mwh, 0.0) - coalesce(renewable_gen_mwh, 0.0)) * 0.45)
            / nullif(total_gen_mwh, 0.0) as carbon_intensity_proxy_tco2_per_mwh,
        total_gen_mwh / nullif(renewable_gen_mwh + (0.25 * total_gen_mwh), 0.0) as supply_demand_stress_index,
        abs(
            total_gen_mwh - lag(total_gen_mwh)
                over (partition by zone_code order by timestamp_hour_utc)
        ) / nullif(total_gen_mwh, 0.0) as ramping_risk_index,
        greatest(
            0.0,
            least(
                1.0,
                (0.4 * coalesce(wind_speed_10m / 20.0, 0.0))
                + (0.4 * coalesce(shortwave_radiation / 800.0, 0.0))
                + (0.2 * greatest(0.0, 1.0 - abs(coalesce(temperature_2m, 15.0) - 15.0) / 25.0))
            )
        ) as weather_index,
        quality_flag
    from joined
)

select
    zone_hour_key,
    zone_code,
    timestamp_hour_utc,
    total_gen_mwh,
    renewable_gen_mwh,
    coalesce(renewable_share_pct, 0.0) as renewable_share_pct,
    co2_proxy_tonnes,
    coalesce(carbon_intensity_proxy_tco2_per_mwh, 0.0) as carbon_intensity_proxy_tco2_per_mwh,
    coalesce(supply_demand_stress_index, 1.0) as supply_demand_stress_index,
    case
        when coalesce(supply_demand_stress_index, 1.0) < 0.85 then 'low'
        when coalesce(supply_demand_stress_index, 1.0) < 0.95 then 'moderate'
        when coalesce(supply_demand_stress_index, 1.0) <= 1.05 then 'high'
        else 'critical'
    end as stress_band,
    coalesce(ramping_risk_index, 0.0) as ramping_risk_index,
    weather_index,
    greatest(
        (renewable_gen_mwh * (1.0 + (0.5 * weather_index))) - renewable_gen_mwh,
        0.0
    ) as curtailment_proxy_mwh,
    coalesce(100.0 * greatest(
        (renewable_gen_mwh * (1.0 + (0.5 * weather_index))) - renewable_gen_mwh,
        0.0
    ) / nullif((renewable_gen_mwh * (1.0 + (0.5 * weather_index))), 0.0), 0.0) as curtailment_proxy_pct,
    cast(null as double) as import_dependency_ratio,
    quality_flag
from kpis
where quality_flag = 'ok'
