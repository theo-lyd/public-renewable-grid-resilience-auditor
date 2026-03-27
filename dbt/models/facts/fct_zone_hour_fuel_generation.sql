with ember as (
    select
        zone_code,
        timestamp_hour_utc,
        fuel_category,
        generation_mwh,
        source_system
    from {{ ref('int_ember_generation_hourly') }}
),

joined as (
    select
        e.zone_code,
        e.timestamp_hour_utc,
        e.fuel_category,
        e.generation_mwh,
        z.zone_key,
        t.time_hour_key,
        f.fuel_category_key,
        s.source_system_key
    from ember e
    left join {{ ref('dim_zone') }} z
      on z.zone_code = e.zone_code
    left join {{ ref('dim_time_hourly') }} t
      on t.timestamp_hour_utc = e.timestamp_hour_utc
    left join {{ ref('dim_fuel_category') }} f
      on f.fuel_category = e.fuel_category
    left join {{ ref('dim_source_system') }} s
      on s.source_system = e.source_system
)

select
    md5(
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(timestamp_hour_utc as varchar), '') || '|' ||
        coalesce(cast(fuel_category as varchar), '')
    ) as zone_hour_fuel_fact_key,
    zone_key,
    time_hour_key,
    fuel_category_key,
    source_system_key,
    zone_code,
    timestamp_hour_utc,
    fuel_category,
    generation_mwh
from joined
