from src.common.performance_benchmark import calculate_speedup


def test_calculate_speedup() -> None:
    assert calculate_speedup(2.0, 1.0) == 2.0
    assert calculate_speedup(1.0, 0.5) == 2.0
    assert calculate_speedup(1.0, 0.0) == 0.0
