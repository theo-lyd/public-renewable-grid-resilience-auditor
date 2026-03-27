select *
from {{ ref('int_zone_hour_conformed') }}
where date_part('minute', timestamp_hour_utc) <> 0
   or date_part('second', timestamp_hour_utc) <> 0
