"""Conditional reference-current and ideal SAR budgets; not a TL431 loop model."""
import itertools
import json
import math
from pathlib import Path


def check_connections(blueprint):
    components = {c["reference"]: c for c in blueprint["components"]}
    expected = {
        "U6": ("TL431BCLP", {"1": "REF_2V495", "2": "GND", "3": "REF_2V495"}),
        "R40": ("68R 1%", {"1": "3V3", "2": "REF_2V495"}),
        "R41": ("1k 1%", {"1": "REF_2V495", "2": "MON_REF"}),
        "R42": ("10k 1%", {"1": "VANA", "2": "VANA_HALF"}),
        "R43": ("10k 1%", {"1": "VANA_HALF", "2": "GND"}),
        "R44": ("1k 1%", {"1": "VANA_HALF", "2": "MON_VANA"}),
    }
    for reference, (value, pins) in expected.items():
        actual = components[reference]
        if actual["value"] != value or actual["pins"] != pins:
            raise ValueError(f"Reference/sampling baseline changed: {reference}")
    module = components["M1"]["pins"]
    if module["9"] != "MON_VANA" or module["10"] != "MON_REF":
        raise ValueError("Logical PA0/PA1 endpoints changed")
    for net in ("REF_2V495", "MON_REF", "MON_VANA", "VANA_HALF"):
        expected_ends = {(ref, pin) for ref, (_, pins) in expected.items()
                         for pin, name in pins.items() if name == net}
        expected_ends.update(("M1", pin) for pin in ("9", "10") if module[pin] == net)
        actual_ends = {(c["reference"], pin) for c in components.values()
                       for pin, name in c["pins"].items() if name == net}
        if actual_ends != expected_ends:
            raise ValueError(f"Added or removed sampling-node load: {net}")


def calculate():
    ref_min, ref_max = 2.495 - 0.012 - 0.016, 2.495 + 0.012 + 0.016
    feed_min = (3.0 - ref_max) / (68 * 1.01)
    feed_max = (3.6 - ref_min) / (68 * 0.99)
    # These are explicit allocations, not guaranteed full-temperature/full-current bounds.
    reference_pin_allowance = (4 + 1.2) * 1e-6
    adc_leakage_allowance = 1e-6
    sample_cap = 8e-12  # Rev17 Table46 maximum internal ADC sample capacitance.
    charge_out = sample_cap * ref_max  # Initial ADC capacitor at 0V.
    peak_out = ref_max / (1000 * 0.99)  # R_ADC=0 for this ideal upper-current estimate.
    peak_into_ref = (3.6 - ref_min) / (1000 * 0.99)
    cathode_low = feed_min - reference_pin_allowance - adc_leakage_allowance - peak_out
    cathode_high = feed_max + adc_leakage_allowance + peak_into_ref
    # Two six-conversion reference/VANA/reference groups per 20Hz main frame.
    # Four PA1 conversions per group, including the discarded conversions.
    groups_per_second = 2 * 20
    pa1_conversions_per_second = groups_per_second * 4
    corners = []
    for a, b, c in itertools.product((0.99, 1.01), repeat=3):
        upper, lower, series = 10_000 * a, 10_000 * b, 1000 * c
        corners.append(upper * lower / (upper + lower) + series)
    source_max = max(corners)
    tau = (source_max + 1000) * sample_cap
    sample_time = 239.5 / 14e6
    conversion_time = (239.5 + 12.5) / 14e6
    return {
        "status": "conditional DC + ideal switched-capacitor calculations; no loop-stability or hardware proof",
        "baseline": "68ohm feed, 1kohm PA1 isolation, 10k/10k+1k PA0; no node capacitors",
        "sources": "TI SLVS543S sections6.4/6.11/9.2.2.2.3; ST DocID13587 Rev17 tables46/48/49, not Rev20",
        "current": {
            "reference_envelope_v": [ref_min, ref_max],
            "feed_min_a": feed_min, "feed_max_a": feed_max,
            "reference_pin_allowance_a": reference_pin_allowance,
            "adc_leakage_allowance_a": adc_leakage_allowance,
            "ideal_initial_sampling_peak_out_a": peak_out,
            "ideal_initial_sampling_peak_into_ref_a": peak_into_ref,
            "conditional_cathode_low_a": cathode_low,
            "conditional_cathode_high_a": cathode_high,
            "recommended_cathode_min_a": 0.001,
            "recommended_cathode_max_a": 0.100,
            "charge_per_pa1_conversion_bound_c": charge_out,
            "pa1_conversions_per_second": pa1_conversions_per_second,
            "absolute_average_sampling_charge_current_bound_a": charge_out * pa1_conversions_per_second,
            "extra_4mV_reference_shift_sensitivity_low_a": (
                (3.0 - (ref_max + 0.004)) / (68 * 1.01)
                - reference_pin_allowance - adc_leakage_allowance
                - (ref_max + 0.004) / (1000 * 0.99)
            ),
        },
        "sampling": {
            "pa0_source_max_ohm": source_max,
            "pa0_ideal_tau_s": tau,
            "pa0_quarter_lsb_settle_s": tau * math.log(2 ** 14),
            "sample_time_s": sample_time,
            "conversion_time_s": conversion_time,
            "six_conversion_group_lower_bound_s": conversion_time * 6,
            "two_groups_per_frame_lower_bound_s": conversion_time * 12,
            "quarter_lsb_at_3V_v": 3.0 / 4096 / 4,
            "sample_cap_not_total_pin_or_probe_cap": True,
        },
        "excluded": [
            "TL431 loop transfer function and high-frequency dynamic impedance",
            "charge injection, parasitic/probe capacitance, ADC switching transients",
            "startup, VDDA disturbances, temperature/current accuracy guarantees",
            "ADC0832 frame duration, firmware overhead and main-frame VANA transients",
        ],
    }


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / "hardware/v2.3/connections-draft.json"
    try:
        blueprint = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Cannot read baseline: {path}") from exc
    check_connections(blueprint)
    print(json.dumps(calculate(), indent=2))


if __name__ == "__main__":
    main()
