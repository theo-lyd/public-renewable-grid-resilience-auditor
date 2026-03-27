select c.*
from {{ ref('int_zone_hour_conformed') }} c
left join {{ ref('zone_conformance_mapping') }} z
  on c.zone_code = z.zone_code
where z.zone_code is null
