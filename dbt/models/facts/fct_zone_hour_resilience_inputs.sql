with conformed as (
    select
        zone_hour_key,
        zone_code,
        timestamp_hour_utc,
        entsoe_generation_mwh,
        ember_generation_mwh,
        wind_speed_10m,
        shortwave_radiation,
        temperature_2m
    from {{ ref('int_zone_hour_conformed') }}
),

joined as (
    select
        c.zone_hour_key,
        c.zone_code,
        c.timestamp_hour_utc,
        z.zone_key,
        t.time_hour_key,
        c.entsoe_generation_mwh,
        c.ember_generation_mwh,
        c.wind_speed_10m,
        c.shortwave_radiation,
        c.temperature_2m,
        z.mapping_status
    from conformed c
    left join {{ ref('dim_zone') }} z
      on z.zone_code = c.zone_code
    left join {{ ref('dim_time_hourly') }} t
      on t.timestamp_hour_utc = c.timestamp_hour_utc
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '')
    ) as zone_hour_fact_key,
    zone_hour_key,
    zone_key,
    time_hour_key,
    zone_code,
    timestamp_hour_utc,
    entsoe_generation_mwh,
    ember_generation_mwh,
    case
        when entsoe_generation_mwh is not null and ember_generation_mwh is not null
            then entsoe_generation_mwh - ember_generation_mwh
        else null
    end as generation_gap_mwh,
    wind_speed_10m,
    shortwave_radiation,
    temperature_2m,
    case
        when mapping_status = 'unmapped' then 'unmapped_zone'
        else 'ok'
    end as quality_flag
from joined
