with grouped as (
    select
        zone_code,
        sum(case when is_current then 1 else 0 end) as current_rows
    from {{ ref('dim_zone_scd2') }}
    group by 1
)

select
    zone_code,
    current_rows
from grouped
where current_rows != 1
