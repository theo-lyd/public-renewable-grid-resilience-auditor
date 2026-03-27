select
    md5(
        coalesce(cast(timestamp_utc as varchar), '') || '|' ||
        coalesce(cast(latitude as varchar), '') || '|' ||
        coalesce(cast(longitude as varchar), '')
    ) as record_id,
    cast(timestamp_utc as timestamp) as timestamp_utc,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(wind_speed_10m as double) as wind_speed_10m,
    cast(shortwave_radiation as double) as shortwave_radiation,
    cast(temperature_2m as double) as temperature_2m
from read_parquet(
    'data/raw/parquet/source=open_meteo/endpoint=historical_forecast_weather/ingestion_date=*/op_*.parquet',
    union_by_name=true,
    filename=true
)
where filename not like '%_metadata.parquet'
