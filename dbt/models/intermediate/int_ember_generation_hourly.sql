with expanded as (
    select
        z.zone_code,
        e.country_code,
        e.fuel_category,
        cast(e.date as timestamp)
            + (h.generate_series * interval '1 hour') as timestamp_hour_utc,
        cast(e.generation_twh as double) * 1000000.0 / 24.0 as generation_mwh
    from {{ ref('stg_ember_generation_mix') }} e
    cross join generate_series(0, 23) as h
    left join {{ ref('zone_conformance_mapping') }} z
      on z.country_code = e.country_code
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '') || '|' ||
        coalesce(cast(fuel_category as varchar), '')
    ) as zone_hour_fuel_key,
    zone_code,
    country_code,
    fuel_category,
    timestamp_hour_utc,
    generation_mwh,
    'MWh' as unit_name,
    'UTC' as timezone_name,
    'ember_electricity' as source_system
from expanded
