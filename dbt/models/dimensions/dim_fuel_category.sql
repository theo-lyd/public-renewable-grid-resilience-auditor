with fuels as (
    select distinct fuel_category
    from {{ ref('int_ember_generation_hourly') }}
    where fuel_category is not null
)

select
    md5(coalesce(cast(fuel_category as varchar), '')) as fuel_category_key,
    fuel_category
from fuels
