select *
from {{ ref('stg_entsoe_generation') }}
where generation_mw < 0
