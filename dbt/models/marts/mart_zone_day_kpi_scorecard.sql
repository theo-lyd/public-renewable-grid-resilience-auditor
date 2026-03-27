with hourly as (
    select
        zone_code,
        cast(timestamp_hour_utc as date) as date_utc,
        total_gen_mwh,
        renewable_gen_mwh,
        co2_proxy_tonnes,
        supply_demand_stress_index,
        ramping_risk_index,
        weather_index,
        curtailment_proxy_mwh,
        curtailment_proxy_pct
    from {{ ref('mart_zone_hour_kpi_scorecard') }}
),

daily_rollup as (
    select
        zone_code,
        date_utc,
        sum(total_gen_mwh) as total_gen_mwh,
        sum(renewable_gen_mwh) as renewable_gen_mwh,
        sum(co2_proxy_tonnes) as co2_proxy_tonnes,
        sum(curtailment_proxy_mwh) as curtailment_proxy_mwh,
        avg(supply_demand_stress_index) as supply_demand_stress_index_avg,
        avg(ramping_risk_index) as ramping_risk_index_avg,
        quantile_cont(ramping_risk_index, 0.9) as ramping_risk_index_p90,
        avg(weather_index) as weather_index_avg,
        abs(corr(renewable_gen_mwh, weather_index)) as weather_sensitivity_score
    from hourly
    group by 1, 2
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(date_utc as varchar), '')
    ) as zone_day_key,
    zone_code,
    date_utc,
    total_gen_mwh,
    renewable_gen_mwh,
    coalesce(100.0 * renewable_gen_mwh / nullif(total_gen_mwh, 0.0), 0.0) as renewable_share_pct,
    co2_proxy_tonnes,
    coalesce(co2_proxy_tonnes / nullif(total_gen_mwh, 0.0), 0.0) as carbon_intensity_proxy_tco2_per_mwh,
    coalesce(supply_demand_stress_index_avg, 1.0) as supply_demand_stress_index,
    case
        when coalesce(supply_demand_stress_index_avg, 1.0) < 0.85 then 'low'
        when coalesce(supply_demand_stress_index_avg, 1.0) < 0.95 then 'moderate'
        when coalesce(supply_demand_stress_index_avg, 1.0) <= 1.05 then 'high'
        else 'critical'
    end as stress_band,
    coalesce(ramping_risk_index_avg, 0.0) as ramping_risk_index_avg,
    coalesce(ramping_risk_index_p90, 0.0) as ramping_risk_index_p90,
    coalesce(weather_index_avg, 0.0) as weather_index_avg,
    coalesce(weather_sensitivity_score, 0.0) as weather_sensitivity_score,
    curtailment_proxy_mwh,
    coalesce(100.0 * curtailment_proxy_mwh / nullif((renewable_gen_mwh + curtailment_proxy_mwh), 0.0), 0.0) as curtailment_proxy_pct,
    cast(null as double) as import_dependency_ratio
from daily_rollup
