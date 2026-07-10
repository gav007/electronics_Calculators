"""Command-line interface for the electronics calculator toolkit."""

import argparse

from calculators import (
    ohms_law,
    parallel_resistance,
    power,
    rc_time_constant,
    series_resistance,
    simulate_rectifier,
    voltage_divider,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Educational electronics calculators")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ohm = subparsers.add_parser("ohms", help="Calculate the missing Ohm's Law value")
    ohm.add_argument("--voltage", type=float)
    ohm.add_argument("--current", type=float)
    ohm.add_argument("--resistance", type=float)

    power_parser = subparsers.add_parser("power", help="Calculate electrical power")
    power_parser.add_argument("--voltage", type=float)
    power_parser.add_argument("--current", type=float)
    power_parser.add_argument("--resistance", type=float)

    resistance = subparsers.add_parser("resistance", help="Calculate series or parallel resistance")
    resistance.add_argument("kind", choices=["series", "parallel"])
    resistance.add_argument("values", nargs="+", type=float)

    divider = subparsers.add_parser("divider", help="Calculate voltage-divider output")
    divider.add_argument("--input-voltage", type=float, required=True)
    divider.add_argument("--top-resistance", type=float, required=True)
    divider.add_argument("--bottom-resistance", type=float, required=True)

    rc = subparsers.add_parser("rc", help="Calculate an RC time constant")
    rc.add_argument("--resistance", type=float, required=True)
    rc.add_argument("--capacitance", type=float, required=True)

    rectifier = subparsers.add_parser("rectifier", help="Simulate a rectifier")
    rectifier.add_argument("--type", choices=["half", "full"], required=True)
    rectifier.add_argument("--vrms", type=float, required=True)
    rectifier.add_argument("--frequency", type=float, required=True)
    rectifier.add_argument("--diode-drop", type=float, default=0.7)
    rectifier.add_argument("--plot", action="store_true", help="Display a Matplotlib plot")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "ohms":
        print(f"Result: {ohms_law(voltage=args.voltage, current=args.current, resistance=args.resistance):.3f}")
    elif args.command == "power":
        print(f"Power: {power(voltage=args.voltage, current=args.current, resistance=args.resistance):.3f} W")
    elif args.command == "resistance":
        result = series_resistance(*args.values) if args.kind == "series" else parallel_resistance(*args.values)
        print(f"Resistance: {result:.3f} ohms")
    elif args.command == "divider":
        result = voltage_divider(args.input_voltage, args.top_resistance, args.bottom_resistance)
        print(f"Divider output: {result:.3f} V")
    elif args.command == "rc":
        print(f"RC time constant: {rc_time_constant(args.resistance, args.capacitance):.6f} seconds")
    else:
        result = simulate_rectifier(args.type, args.vrms, args.frequency, args.diode_drop)
        print(f"Input peak voltage:  {result.input_peak:.3f} V")
        print(f"Output peak voltage: {result.output_peak:.3f} V")
        print(f"Average DC output:   {result.average_output:.3f} V")
        print(f"Output RMS voltage:  {result.output_rms:.3f} V")
        print(f"Ripple frequency:    {result.ripple_frequency:.3f} Hz")
        if args.plot:
            import matplotlib.pyplot as plt
            plt.plot(result.time, result.input_wave, label="AC input")
            plt.plot(result.time, result.output_wave, label="Rectified output")
            plt.title(f"{args.type.title()}-wave rectifier")
            plt.xlabel("Time (s)")
            plt.ylabel("Voltage (V)")
            plt.grid(True)
            plt.legend()
            plt.show()


if __name__ == "__main__":
    main()
