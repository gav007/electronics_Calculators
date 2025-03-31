import math
import matplotlib.pyplot as plt


def simulate_rectifier(rectifier_type, vrms, frequency, diode_drop, num_cycles=2, steps_per_cycle=200):
    """
    Simulates either a half-wave or full-wave rectifier output (ideal diodes except for a fixed diode_drop).

    rectifier_type: 'half' or 'full'
    vrms: RMS value of the AC input
    frequency: frequency of the AC signal (Hz)
    diode_drop: approximate forward drop of the diodes (V)
    num_cycles: how many cycles to simulate
    steps_per_cycle: granularity of simulation per cycle
    """
    # Derived values
    vpeak = vrms * math.sqrt(2.0)  # peak voltage
    omega = 2.0 * math.pi * frequency  # angular frequency

    # Create time array
    t_end = num_cycles / frequency
    dt = t_end / (num_cycles * steps_per_cycle)
    time = [i * dt for i in range(num_cycles * steps_per_cycle + 1)]

    # Calculate input AC waveform
    input_wave = [vpeak * math.sin(omega * t) for t in time]

    # Rectified output
    output_wave = []
    for vin in input_wave:
        if rectifier_type.lower() == "half":
            # Conduct only if vin > diode_drop
            if vin > diode_drop:
                vout = vin - diode_drop
            else:
                vout = 0.0
        elif rectifier_type.lower() == "full":
            # Full-wave: rectified magnitude minus diode drops.
            # In a typical bridge, two diodes conduct at once => total drop ~ 2 * diode_drop.
            # For simplicity, we assume symmetrical conduction each half-cycle:
            mag = abs(vin)
            if mag > 2 * diode_drop:
                vout = mag - 2.0 * diode_drop
            else:
                vout = 0.0
        else:
            raise ValueError("rectifier_type must be 'half' or 'full'.")

        output_wave.append(vout)

    # Return the time array, input, and output for plotting or further analysis
    return time, input_wave, output_wave


if __name__ == "__main__":
    # 1) Get user inputs
    rectifier_type = input("Enter rectifier type ('half' or 'full'): ").strip().lower()
    vrms = float(input("Enter the RMS voltage of the AC source (e.g. 24): "))
    frequency = float(input("Enter the line frequency (Hz) (e.g. 50 or 60): "))
    diode_drop = float(input("Enter the diode forward drop (V) (e.g. 0.7): "))

    # 2) Run the simulation
    t, vin, vout = simulate_rectifier(rectifier_type, vrms, frequency, diode_drop)

    # 3) Plot the results
    plt.figure()
    plt.plot(t, vin, label="AC Input")
    plt.plot(t, vout, label="Rectified Output")
    plt.title(f"{rectifier_type.capitalize()}-Wave Rectification Simulation")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.grid(True)
    plt.show()
