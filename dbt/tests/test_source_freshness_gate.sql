select *
from {{ ref('stg_source_freshness_gate') }}
where is_fresh = false
