select
    zone_day_key,
    resilience_composite_baseline,
    resilience_composite_security_heavy,
    resilience_composite_transition_heavy
from {{ ref('mart_zone_day_resilience_composite') }}
where
    resilience_composite_baseline < 0
    or resilience_composite_baseline > 100
    or resilience_composite_security_heavy < 0
    or resilience_composite_security_heavy > 100
    or resilience_composite_transition_heavy < 0
    or resilience_composite_transition_heavy > 100
