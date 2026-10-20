"""Conditional DC/settling calculations, using the identified Rev17 mirror."""
import itertools
import json
import math


def monitor_current(vana, upper, lower, series):
    # Conservative ideal PA0 clamp to 0V. Not a model of an unpowered MCU.
    voltage = vana * lower / (upper + lower)
    resistance = upper * lower / (upper + lower) + series
    return voltage / resistance


def main():
    source = (10_000 * 1.01) / 2 + 1000 * 1.01
    switch = 1000  # Rev17 Table 46 maximum R_ADC; not Rev20 verification.
    sample_cap = 8e-12  # Rev17 Table 46 maximum C_ADC.
    tau = (source + switch) * sample_cap
    quarter_lsb_settle = tau * math.log(2 ** 14)
    sample_time = 239.5 / 14e6
    conversion_time = (239.5 + 12.5) / 14e6
    currents = [monitor_current(5.25, 10_000 * a, 10_000 * b, 1000 * c)
                for a, b, c in itertools.product((0.99, 1.01), repeat=3)]
    assert source < 10_000
    assert quarter_lsb_settle < sample_time
    assert math.isclose(conversion_time, 18e-6)
    assert math.isclose(56e6 / 4, 14e6)
    assert max(currents) < 0.00045
    assert max(currents) > 0.0004
    assert math.isclose(2 * 5e-9 * 180_000, 0.0018)
    assert math.isclose(2 * 80e-9 * 180_000, 0.0288)
    print(json.dumps({
        "status": "conditional models only; do not establish powered-off MCU safety",
        "stm32_source": "ST DocID13587 Rev17, August2015; WeAct mirror, NOT DS5319 Rev20",
        "assertions": 8,
        "adc_sampling": {
            "source_resistance_max_ohm": source,
            "tau_s": tau,
            "quarter_lsb_settling_s": quarter_lsb_settle,
            "sample_time_s": sample_time,
            "conversion_time_s": conversion_time,
            "limits": "no added input capacitor; ideal passive source; excludes reference dynamic impedance, board parasitics and switching transients",
        },
        "pa0_off_clamp": {
            "vana_v": 5.25,
            "nominal_current_a": monitor_current(5.25, 10_000, 10_000, 1000),
            "resistor_corner_max_current_a": max(currents),
            "warning": "less than an absolute injection-current limit does NOT authorize operation with VDDA/VDD absent",
        },
        "diode_leakage_sensitivity": {
            "source": "Diodes BAV199 DS30232 Rev11-2, p2; per-diode VR=75V pulse test",
            "two_diodes_25C_input_error_v": 0.0018,
            "two_diodes_150C_input_error_v": 0.0288,
            "limits": "these are sensitivities at stated test points, not an interpolated 0-70C full-board leakage guarantee; op-amp/PCB omitted",
        },
    }, indent=2))


if __name__ == "__main__":
    main()
