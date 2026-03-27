with timestamps as (
    select distinct timestamp_hour_utc
    from {{ ref('int_zone_hour_conformed') }}
    where timestamp_hour_utc is not null
)

select
    md5(coalesce(cast(timestamp_hour_utc as varchar), '')) as time_hour_key,
    timestamp_hour_utc,
    cast(timestamp_hour_utc as date) as date_utc,
    extract(hour from timestamp_hour_utc) as hour_of_day_utc,
    extract(isodow from timestamp_hour_utc) as iso_day_of_week,
    date_trunc('week', timestamp_hour_utc) as week_start_utc,
    extract(month from timestamp_hour_utc) as month_of_year,
    extract(quarter from timestamp_hour_utc) as quarter_of_year,
    extract(year from timestamp_hour_utc) as year_utc,
    case
        when extract(isodow from timestamp_hour_utc) in (6, 7) then true
        else false
    end as is_weekend
from timestamps
