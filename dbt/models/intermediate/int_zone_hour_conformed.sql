with entsoe as (
    select
        zone_code,
        timestamp_hour_utc,
        generation_mwh as entsoe_generation_mwh
    from {{ ref('int_entsoe_generation_hourly') }}
),

ember as (
    select
        zone_code,
        timestamp_hour_utc,
        sum(generation_mwh) as ember_generation_mwh
    from {{ ref('int_ember_generation_hourly') }}
    group by 1, 2
),

weather as (
    select
        zone_code,
        timestamp_hour_utc,
        wind_speed_10m,
        shortwave_radiation,
        temperature_2m
    from {{ ref('int_open_meteo_zone_hourly') }}
),

joined as (
    select
        coalesce(e.zone_code, em.zone_code, w.zone_code) as zone_code,
        coalesce(e.timestamp_hour_utc, em.timestamp_hour_utc, w.timestamp_hour_utc) as timestamp_hour_utc,
        e.entsoe_generation_mwh,
        em.ember_generation_mwh,
        w.wind_speed_10m,
        w.shortwave_radiation,
        w.temperature_2m
    from entsoe e
    full outer join ember em
      on e.zone_code = em.zone_code
     and e.timestamp_hour_utc = em.timestamp_hour_utc
    full outer join weather w
      on coalesce(e.zone_code, em.zone_code) = w.zone_code
     and coalesce(e.timestamp_hour_utc, em.timestamp_hour_utc) = w.timestamp_hour_utc
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '')
    ) as zone_hour_key,
    zone_code,
    timestamp_hour_utc,
    entsoe_generation_mwh,
    ember_generation_mwh,
    wind_speed_10m,
    shortwave_radiation,
    temperature_2m,
    'UTC' as timezone_name
from joined
