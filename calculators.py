"""Reusable electronics calculations for the learning toolkit."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RectifierResult:
    time: list[float]
    input_wave: list[float]
    output_wave: list[float]
    input_peak: float
    output_peak: float
    average_output: float
    output_rms: float
    ripple_frequency: float


def _positive(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _required(value: float | None, name: str) -> float:
    if value is None:
        raise ValueError(f"{name} is required")
    return value


def ohms_law(*, voltage: float | None = None, current: float | None = None,
             resistance: float | None = None) -> float:
    """Return the one missing Ohm's Law value."""
    values = [voltage, current, resistance]
    if sum(value is None for value in values) != 1:
        raise ValueError("Provide exactly two of voltage, current, and resistance")
    if voltage is None:
        return _positive(_required(current, "Current"), "Current") * _positive(_required(resistance, "Resistance"), "Resistance")
    if current is None:
        return _positive(_required(voltage, "Voltage"), "Voltage") / _positive(_required(resistance, "Resistance"), "Resistance")
    return _positive(_required(voltage, "Voltage"), "Voltage") / _positive(_required(current, "Current"), "Current")


def power(*, voltage: float | None = None, current: float | None = None,
          resistance: float | None = None) -> float:
    """Return power using any valid pair of voltage, current, and resistance."""
    if voltage is not None and current is not None:
        return _positive(voltage, "Voltage") * _positive(current, "Current")
    if current is not None and resistance is not None:
        return _positive(current, "Current") ** 2 * _positive(resistance, "Resistance")
    if voltage is not None and resistance is not None:
        return _positive(voltage, "Voltage") ** 2 / _positive(resistance, "Resistance")
    raise ValueError("Provide any two of voltage, current, and resistance")


def simulate_rectifier(rectifier_type: str, vrms: float, frequency: float,
                       diode_drop: float, num_cycles: int = 2,
                       steps_per_cycle: int = 200) -> RectifierResult:
    """Simulate a half-wave or full-wave bridge rectifier."""
    rectifier_type = rectifier_type.lower().strip()
    if rectifier_type not in {"half", "full"}:
        raise ValueError("rectifier_type must be 'half' or 'full'")
    _positive(vrms, "RMS voltage")
    _positive(frequency, "Frequency")
    if diode_drop < 0:
        raise ValueError("Diode drop cannot be negative")
    if num_cycles < 1 or steps_per_cycle < 2:
        raise ValueError("num_cycles must be at least 1 and steps_per_cycle at least 2")

    input_peak = vrms * math.sqrt(2)
    omega = 2 * math.pi * frequency
    sample_count = num_cycles * steps_per_cycle
    time = [i / (frequency * steps_per_cycle) for i in range(sample_count + 1)]
    input_wave = [input_peak * math.sin(omega * t) for t in time]
    conduction_drop = diode_drop if rectifier_type == "half" else 2 * diode_drop
    output_wave = [max((vin if rectifier_type == "half" else abs(vin)) - conduction_drop, 0.0)
                   for vin in input_wave]

    average_output = sum(output_wave) / len(output_wave)
    output_rms = math.sqrt(sum(value ** 2 for value in output_wave) / len(output_wave))
    return RectifierResult(time, input_wave, output_wave, input_peak,
                           max(output_wave), average_output, output_rms,
                           frequency if rectifier_type == "half" else 2 * frequency)
