import pytest

from src.common.performance_benchmark import (
    _coefficient_of_variation,
    _percentile,
    calculate_speedup,
)


def test_calculate_speedup() -> None:
    assert calculate_speedup(2.0, 1.0) == 2.0
    assert calculate_speedup(1.0, 0.5) == 2.0
    assert calculate_speedup(1.0, 0.0) == 0.0


def test_percentile() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    assert _percentile(values, 50) == 2.5
    assert _percentile(values, 95) == pytest.approx(3.85)


def test_coefficient_of_variation() -> None:
    assert _coefficient_of_variation([1.0, 1.0, 1.0]) == 0.0
    assert _coefficient_of_variation([0.0, 0.0]) == 0.0
    assert _coefficient_of_variation([1.0]) == 0.0
