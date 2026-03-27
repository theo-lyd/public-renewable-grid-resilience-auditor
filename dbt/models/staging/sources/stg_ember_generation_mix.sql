select
    md5(
        coalesce(cast(date as varchar), '') || '|' ||
        coalesce(cast(country_code as varchar), '') || '|' ||
        coalesce(cast(fuel_category as varchar), '')
    ) as record_id,
    cast(date as date) as date,
    cast(country_code as varchar) as country_code,
    cast(fuel_category as varchar) as fuel_category,
    cast(generation_twh as double) as generation_twh
from read_parquet(
    'data/raw/parquet/source=ember_electricity/endpoint=national_generation_mix/ingestion_date=*/op_*.parquet',
    union_by_name=true,
    filename=true
)
where filename not like '%_metadata.parquet'
