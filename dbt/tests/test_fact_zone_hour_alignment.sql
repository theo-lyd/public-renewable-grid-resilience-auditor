with fact as (
    select
        zone_code,
        timestamp_hour_utc
    from {{ ref('fct_zone_hour_resilience_inputs') }}
),

conformed as (
    select
        zone_code,
        timestamp_hour_utc
    from {{ ref('int_zone_hour_conformed') }}
)

select
    f.zone_code,
    f.timestamp_hour_utc
from fact f
left join conformed c
  on c.zone_code = f.zone_code
 and c.timestamp_hour_utc = f.timestamp_hour_utc
where c.zone_code is null
