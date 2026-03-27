with mapped as (
    select
        z.zone_code,
        date_trunc('hour', w.timestamp_utc) as timestamp_hour_utc,
        w.wind_speed_10m,
        w.shortwave_radiation,
        w.temperature_2m
    from {{ ref('stg_open_meteo_weather') }} w
    left join {{ ref('zone_conformance_mapping') }} z
      on round(w.latitude, 2) = round(cast(z.latitude as double), 2)
     and round(w.longitude, 2) = round(cast(z.longitude as double), 2)
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '')
    ) as zone_hour_key,
    zone_code,
    timestamp_hour_utc,
    cast(wind_speed_10m as double) as wind_speed_10m,
    cast(shortwave_radiation as double) as shortwave_radiation,
    cast(temperature_2m as double) as temperature_2m,
    'UTC' as timezone_name,
    'open_meteo' as source_system
from mapped
