with sources as (
    select distinct source_system
    from {{ ref('int_entsoe_generation_hourly') }}
    where source_system is not null

    union

    select distinct source_system
    from {{ ref('int_ember_generation_hourly') }}
    where source_system is not null

    union

    select distinct source_system
    from {{ ref('int_open_meteo_zone_hourly') }}
    where source_system is not null
)

select
    md5(coalesce(cast(source_system as varchar), '')) as source_system_key,
    source_system
from sources
