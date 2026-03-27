with scored as (
    select
        zone_hour_key,
        supply_demand_stress_index,
        stress_band,
        case
            when supply_demand_stress_index < 0.85 then 'low'
            when supply_demand_stress_index < 0.95 then 'moderate'
            when supply_demand_stress_index <= 1.05 then 'high'
            else 'critical'
        end as expected_band
    from {{ ref('mart_zone_hour_kpi_scorecard') }}
)

select
    zone_hour_key,
    supply_demand_stress_index,
    stress_band,
    expected_band
from scored
where stress_band != expected_band
