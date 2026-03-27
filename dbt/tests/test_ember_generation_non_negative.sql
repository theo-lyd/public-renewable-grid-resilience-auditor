select *
from {{ ref('stg_ember_generation_mix') }}
where generation_twh < 0
