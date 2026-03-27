from __future__ import annotations

import duckdb
import pandas as pd
import streamlit as st

from src.common.config import get_project_paths
from src.monitoring.dashboard_narrative import get_metric_cards

st.set_page_config(page_title="Grid Resilience Auditor", layout="wide")


@st.cache_data
def _load_dashboard_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = get_project_paths()

    daily_query = """
        select
            zone_code,
            date_utc,
            renewable_share_pct,
            carbon_intensity_proxy_tco2_per_mwh,
            supply_demand_stress_index,
            stress_band,
            ramping_risk_index_avg,
            weather_sensitivity_score,
            curtailment_proxy_pct
        from main_marts.mart_zone_day_kpi_scorecard
        order by date_utc, zone_code
    """

    composite_query = """
        select
            zone_code,
            date_utc,
            resilience_composite_baseline,
            resilience_composite_security_heavy,
            resilience_composite_transition_heavy
        from main_marts.mart_zone_day_resilience_composite
        order by date_utc, zone_code
    """

    with duckdb.connect(str(paths.duckdb_path)) as conn:
        daily_frame = conn.execute(daily_query).df()
        composite_frame = conn.execute(composite_query).df()

    return daily_frame, composite_frame


def _render_metric_cards() -> None:
    st.subheader("KPI explanation cards")

    for card in get_metric_cards():
        with st.expander(card.title, expanded=False):
            st.markdown(f"**Plain-language explanation:** {card.plain_language_explanation}")
            st.markdown(f"**Technical definition:** {card.technical_definition}")
            st.markdown(f"**Caveat:** {card.caveat}")


def main() -> None:
    st.title("Public Renewable Grid Resilience Auditor")
    st.caption("Phase 10 dashboard: stakeholder view + technical narrative cards")

    try:
        daily_frame, composite_frame = _load_dashboard_data()
    except Exception as err:
        st.error("Dashboard data load failed. Run `make dbt-marts` first.")
        st.exception(err)
        return

    if daily_frame.empty or composite_frame.empty:
        st.warning("No dashboard-ready records found. Ensure upstream phases produced mart outputs.")
        return

    zones = sorted(daily_frame["zone_code"].dropna().unique().tolist())
    selected_zone = st.selectbox("Zone", options=zones)

    zone_daily = daily_frame[daily_frame["zone_code"] == selected_zone].copy()
    zone_composite = composite_frame[composite_frame["zone_code"] == selected_zone].copy()

    latest_daily = zone_daily.sort_values("date_utc").iloc[-1]
    latest_composite = zone_composite.sort_values("date_utc").iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Renewable Share (%)", f"{latest_daily['renewable_share_pct']:.2f}")
    col2.metric("Stress Index", f"{latest_daily['supply_demand_stress_index']:.2f}")
    col3.metric(
        "Composite Resilience (Baseline)",
        f"{latest_composite['resilience_composite_baseline']:.2f}",
    )

    st.subheader("Daily KPI trends")
    st.line_chart(
        zone_daily.set_index("date_utc")[
            [
                "renewable_share_pct",
                "carbon_intensity_proxy_tco2_per_mwh",
                "supply_demand_stress_index",
                "ramping_risk_index_avg",
                "curtailment_proxy_pct",
            ]
        ]
    )

    st.subheader("Composite sensitivity variants")
    st.line_chart(
        zone_composite.set_index("date_utc")[
            [
                "resilience_composite_baseline",
                "resilience_composite_security_heavy",
                "resilience_composite_transition_heavy",
            ]
        ]
    )

    _render_metric_cards()


if __name__ == "__main__":
    main()
