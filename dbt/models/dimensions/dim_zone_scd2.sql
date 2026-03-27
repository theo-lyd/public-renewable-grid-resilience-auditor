with history as (
    select
        zone_code,
        mapping_status,
        country_code,
        cast(latitude as double) as latitude,
        cast(longitude as double) as longitude,
        timezone_name,
        cast(valid_from as date) as valid_from_date,
        cast(valid_to as date) as valid_to_date
    from {{ ref('zone_conformance_mapping_history') }}
),

ordered as (
    select
        zone_code,
        mapping_status,
        country_code,
        latitude,
        longitude,
        timezone_name,
        valid_from_date,
        valid_to_date,
        lead(valid_from_date) over (
            partition by zone_code
            order by valid_from_date
        ) as next_valid_from
    from history
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(valid_from_date as varchar), '')
    ) as zone_scd2_key,
    zone_code,
    mapping_status,
    country_code,
    latitude,
    longitude,
    timezone_name,
    valid_from_date as valid_from,
    coalesce(
        valid_to_date,
        case
            when next_valid_from is not null then next_valid_from - interval '1 day'
            else cast('9999-12-31' as date)
        end
    ) as valid_to,
    case
        when coalesce(valid_to_date, cast('9999-12-31' as date)) = cast('9999-12-31' as date)
            then true
        else false
    end as is_current
from ordered
