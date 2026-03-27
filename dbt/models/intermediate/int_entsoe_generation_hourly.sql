with base as (
    select
        zone_code,
        date_trunc('hour', timestamp_utc) as timestamp_hour_utc,
        generation_mw
    from {{ ref('stg_entsoe_generation') }}
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '')
    ) as zone_hour_key,
    zone_code,
    timestamp_hour_utc,
    cast(generation_mw as double) as generation_mw,
    cast(generation_mw as double) as generation_mwh,
    'UTC' as timezone_name,
    'entsoe_transparency' as source_system
from base
