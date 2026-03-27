select *
from {{ ref('int_zone_hour_conformed') }}
where (entsoe_generation_mwh is not null and entsoe_generation_mwh < 0)
   or (ember_generation_mwh is not null and ember_generation_mwh < 0)
