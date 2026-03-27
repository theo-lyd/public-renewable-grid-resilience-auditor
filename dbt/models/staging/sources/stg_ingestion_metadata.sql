select
    cast(run_id as varchar) as run_id,
    cast(operation_key as varchar) as operation_key,
    cast(source_id as varchar) as source_id,
    cast(endpoint_id as varchar) as endpoint_id,
    cast(requested_at_utc as timestamp) as requested_at_utc,
    cast(window_start_utc as timestamp) as window_start_utc,
    cast(window_end_utc as timestamp) as window_end_utc,
    cast(request_params_json as varchar) as request_params_json,
    cast(record_count as integer) as record_count,
    cast(status as varchar) as status
from read_parquet(
    'data/raw/parquet/source=*/endpoint=*/ingestion_date=*/op_*_metadata.parquet'
)
