with latest_source_ingestion as (
    select
        source_id,
        endpoint_id,
        max(requested_at_utc) as max_requested_at_utc
    from {{ ref('stg_ingestion_metadata') }}
    group by 1, 2
),

freshness_thresholds as (
    select * from (
        values
            ('open_meteo', 'historical_forecast_weather', 6),
            ('entsoe_transparency', 'generation_actual_per_type', 6),
            ('ember_electricity', 'national_generation_mix', 48)
    ) as t(source_id, endpoint_id, freshness_threshold_hours)
),

joined as (
    select
        l.source_id,
        l.endpoint_id,
        l.max_requested_at_utc,
        t.freshness_threshold_hours,
        datediff('hour', l.max_requested_at_utc, now()) as lag_hours
    from latest_source_ingestion l
    left join freshness_thresholds t using (source_id, endpoint_id)
)

select
    source_id,
    endpoint_id,
    max_requested_at_utc,
    freshness_threshold_hours,
    lag_hours,
    case
        when freshness_threshold_hours is null then false
        when lag_hours <= freshness_threshold_hours then true
        else false
    end as is_fresh
from joined
