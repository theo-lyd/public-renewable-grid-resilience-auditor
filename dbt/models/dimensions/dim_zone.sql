with mapped as (
    select distinct
        zone_code,
        country_code,
        cast(latitude as double) as latitude,
        cast(longitude as double) as longitude
    from {{ ref('zone_conformance_mapping') }}
    where zone_code is not null
),

observed as (
    select distinct zone_code
    from {{ ref('int_zone_hour_conformed') }}
    where zone_code is not null
),

conformed as (
    select
        o.zone_code,
        m.country_code,
        m.latitude,
        m.longitude,
        case
            when m.zone_code is null then 'unmapped'
            else 'mapped'
        end as mapping_status,
        'zone_conformance_mapping' as mapping_source
    from observed o
    left join mapped m
      on m.zone_code = o.zone_code
)

select
    md5(coalesce(cast(zone_code as varchar), '')) as zone_key,
    zone_code,
    country_code,
    latitude,
    longitude,
    mapping_status,
    mapping_source
from conformed
