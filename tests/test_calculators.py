from math import isclose

import pytest

from calculators import (
    ohms_law,
    parallel_resistance,
    power,
    rc_time_constant,
    series_resistance,
    simulate_rectifier,
    voltage_divider,
)


def test_ohms_law_calculates_voltage():
    assert ohms_law(current=2, resistance=10) == 20


def test_ohms_law_calculates_current():
    assert ohms_law(voltage=12, resistance=6) == 2


def test_power_uses_voltage_and_current():
    assert power(voltage=12, current=2) == 24


def test_power_uses_voltage_and_resistance():
    assert power(voltage=12, resistance=6) == 24


def test_series_resistance():
    assert series_resistance(100, 220, 330) == 650


def test_parallel_resistance():
    assert isclose(parallel_resistance(100, 100), 50)


def test_voltage_divider():
    assert voltage_divider(12, 1000, 1000) == 6


def test_rc_time_constant():
    assert rc_time_constant(1000, 0.000001) == 0.001


def test_rectifier_peak_values():
    result = simulate_rectifier("full", 24, 50, 0.7)
    assert isclose(result.input_peak, 24 * 2**0.5)
    assert isclose(result.output_peak, result.input_peak - 1.4, abs_tol=0.02)
    assert result.ripple_frequency == 100


def test_invalid_rectifier_is_rejected():
    with pytest.raises(ValueError, match="rectifier_type"):
        simulate_rectifier("invalid", 24, 50, 0.7)


def test_invalid_ohms_law_input_is_rejected():
    with pytest.raises(ValueError):
        ohms_law(voltage=12, current=2, resistance=6)
