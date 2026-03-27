with daily as (
    select
        zone_day_key,
        zone_code,
        date_utc,
        renewable_share_pct,
        carbon_intensity_proxy_tco2_per_mwh,
        supply_demand_stress_index,
        ramping_risk_index_p90,
        curtailment_proxy_pct,
        weather_sensitivity_score,
        import_dependency_ratio
    from {{ ref('mart_zone_day_kpi_scorecard') }}
),

normalized as (
    select
        zone_day_key,
        zone_code,
        date_utc,
        least(greatest(renewable_share_pct, 0.0), 100.0) as renewable_share_norm,
        least(greatest((1.0 - (coalesce(carbon_intensity_proxy_tco2_per_mwh, 0.8) / 0.8)) * 100.0, 0.0), 100.0)
            as carbon_intensity_norm,
        least(greatest((1.0 - (abs(coalesce(supply_demand_stress_index, 1.4) - 1.0) / 0.4)) * 100.0, 0.0), 100.0)
            as stress_norm,
        least(greatest((1.0 - (coalesce(ramping_risk_index_p90, 0.5) / 0.5)) * 100.0, 0.0), 100.0)
            as ramping_norm,
        least(greatest(100.0 - coalesce(curtailment_proxy_pct, 100.0), 0.0), 100.0) as curtailment_norm,
        least(greatest((1.0 - coalesce(import_dependency_ratio, 0.5)) * 100.0, 0.0), 100.0) as import_dependency_norm,
        least(greatest((1.0 - coalesce(weather_sensitivity_score, 1.0)) * 100.0, 0.0), 100.0) as weather_sensitivity_norm
    from daily
)

select
    zone_day_key,
    zone_code,
    date_utc,
    renewable_share_norm,
    carbon_intensity_norm,
    stress_norm,
    ramping_norm,
    curtailment_norm,
    import_dependency_norm,
    weather_sensitivity_norm,
    (
        (0.25 * renewable_share_norm)
        + (0.20 * carbon_intensity_norm)
        + (0.20 * stress_norm)
        + (0.15 * ramping_norm)
        + (0.10 * curtailment_norm)
        + (0.10 * weather_sensitivity_norm)
    ) as resilience_composite_baseline,
    (
        (0.20 * renewable_share_norm)
        + (0.15 * carbon_intensity_norm)
        + (0.25 * stress_norm)
        + (0.20 * ramping_norm)
        + (0.10 * curtailment_norm)
        + (0.10 * weather_sensitivity_norm)
    ) as resilience_composite_security_heavy,
    (
        (0.30 * renewable_share_norm)
        + (0.25 * carbon_intensity_norm)
        + (0.15 * stress_norm)
        + (0.10 * ramping_norm)
        + (0.10 * curtailment_norm)
        + (0.10 * weather_sensitivity_norm)
    ) as resilience_composite_transition_heavy
from normalized
