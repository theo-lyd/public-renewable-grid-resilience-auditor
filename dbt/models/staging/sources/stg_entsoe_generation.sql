select
    md5(
        coalesce(cast(timestamp_utc as varchar), '') || '|' ||
        coalesce(cast(zone_code as varchar), '') || '|' ||
        coalesce(cast(position as varchar), '')
    ) as record_id,
    cast(timestamp_utc as timestamp) as timestamp_utc,
    cast(zone_code as varchar) as zone_code,
    cast(position as integer) as position,
    cast(generation_mw as double) as generation_mw
from read_parquet(
    'data/raw/parquet/source=entsoe_transparency/endpoint=generation_actual_per_type/ingestion_date=*/op_*.parquet',
    union_by_name=true,
    filename=true
)
where filename not like '%_metadata.parquet'
