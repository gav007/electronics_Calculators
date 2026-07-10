# Electronics Calculators

A small educational Python toolkit for learning electronics calculations and visualising rectifier circuits.

## Current features

- Ohm's Law: calculate voltage, current, or resistance
- Electrical power: calculate power from voltage/current/resistance
- Half-wave rectifier simulation
- Full-wave bridge rectifier simulation
- Average DC output, output RMS, peak output, and ripple frequency
- Optional Matplotlib waveform plots

This is an educational model, not a replacement for circuit-design software or measurements from real hardware.

## Setup

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\\Scripts\\activate    # Windows
python -m pip install -r requirements.txt
```

## Examples

Calculate voltage from current and resistance:

```bash
python3 cli.py ohms --current 2 --resistance 10
```

Calculate power:

```bash
python3 cli.py power --voltage 12 --current 2
```

Simulate a 24 V RMS full-wave bridge rectifier at 50 Hz:

```bash
python3 cli.py rectifier --type full --vrms 24 --frequency 50 --diode-drop 0.7
```

Add `--plot` to display the input and rectified waveforms:

```bash
python3 cli.py rectifier --type full --vrms 24 --frequency 50 --plot
```

## Browser demo

A static browser version is available in [`web/`](web/). Open `web/index.html` locally, or use the published demo when GitHub Pages is enabled.

The browser interface includes Ohm's Law, power, series/parallel resistance, voltage divider, and RC time constant calculators.

## Tests

```bash
pytest -q
```


## Electrical assumptions

- RMS input is treated as a clean sine wave.
- A half-wave rectifier uses one diode drop while conducting.
- A bridge rectifier uses two diode drops while conducting.
- Real diode behaviour, transformer losses, load effects, capacitor smoothing, and ripple under load are not yet modelled.

## Planned improvements

- Resistor series/parallel calculator
- Voltage divider calculator
- Capacitor RC time constant
- Smoothing capacitor and load model
- Browser-based interface
- More worked examples and diagrams

## Safety

Use only simulated values or circuits you are authorised and qualified to work with. Mains electricity can be lethal; do not use this project as a substitute for supervision, isolation, or proper test equipment.
