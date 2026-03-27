select
    zone_code,
    mapping_status
from {{ ref('dim_zone') }}
where mapping_status = 'unmapped'
