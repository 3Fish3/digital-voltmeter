"""V2.2 conditional calculations; ideal DC, not hardware validation."""
import itertools
import json
import math


def node(rs, rg, vin, rail):
    # Default un-biased divider. rail retained for explicit test semantics.
    return vin * rg / (rs + rg)


def dormant_rail(inputs, series, bleed):
    # Conservative shared upper clamps: zero Vf, ignore Rg sinks and all chip load.
    active = [(v, r) for v, r in zip(inputs, series, strict=True) if v > 0]
    while active:
        rail = sum(v / r for v, r in active) / (1 / bleed + sum(1 / r for _, r in active))
        conducting = [(v, r) for v, r in active if v >= rail]
        if len(conducting) == len(active):
            return rail
        active = conducting
    return 0.0


def adc_ratio(rail, vref, vdda, gain):
    return (gain * rail / vdda) / (vref / vdda) * vref / gain


def main():
    checks = 0
    rows = []
    for inputs in ((0, 0), (5, 0), (0, 5), (5, 5)):
        values = [dormant_rail(inputs, (180e3 * a, 180e3 * b), 4700 * c)
                  for a, b, c in itertools.product((0.99, 1.01), repeat=3)]
        assert max(values) < 0.26
        checks += 1
        rows.append({"inputs_v": inputs, "max_dormant_rail_v": max(values)})
    assert dormant_rail((5, 5), (180e3, 180e3), 1e99) > 4.99
    checks += 1
    assert math.isclose(dormant_rail((5, 5), (180e3, 180e3), 4700), 0.24815205913410776)
    checks += 1
    # Reference candidate supplied by 3.3V, not VANA: 68 ohm 1%.
    ref_min, ref_max = 2.495 - 0.012 - 0.016, 2.495 + 0.012 + 0.016
    ref_current_min = (3.0 - ref_max) / (68 * 1.01)
    ref_current_max = (3.6 - ref_min) / (68 * 0.99)
    assert ref_current_min > 0.001
    checks += 1
    assert ref_current_max < 0.018
    checks += 1
    monitor_gain_max = 1.01 / (0.99 + 1.01)
    assert monitor_gain_max * 5.25 < 3.0
    checks += 1
    for rail in (4.4, 4.61978, 4.6298, 5, 5.25):
        for vdda in (3.0, 3.3, 3.6):
            assert math.isclose(adc_ratio(rail, 2.495, vdda, 0.5), rail)
            checks += 1
    # Conditional revised load budgets, not measured limits.
    sys_min = 4.75 - 0.270 * (0.25 + 0.15)
    rail_min = sys_min - 0.022 * 1.01
    assert math.isclose(rail_min, 4.61978)
    checks += 1
    highs = [node(180e3 * a, 1.2e6 * b, 5, rail_min)
             for a, b in itertools.product((0.99, 1.01), repeat=2)]
    assert rail_min - max(highs) > 0.25
    checks += 1
    assert min(180e3 * a + 1.2e6 * b for a, b in itertools.product((0.99, 1.01), repeat=2)) >= 1e6
    checks += 1
    # Additive allocations only. 5 LSB auxiliary ADC error is an UNVERIFIED assumption.
    ref_code_min = ref_min / 3.6 * 4096
    monitor_code_min = (0.99 / 2) * rail_min / 3.6 * 4096
    auxiliary_ratio_error = (1 + 5 / monitor_code_min) / (1 - 5 / ref_code_min) - 1
    adc0832_step_max = 5.25 / 256 / (1.2 / 1.38)
    allocations_v = {
        "ADC0832_TUE_1LSB": adc0832_step_max,
        "quantization_half_LSB_separate_conservative": adc0832_step_max / 2,
        "MCP_offset_4p5mV_input_referred": 0.0045 / (1.2 / 1.38),
        "net_leakage_30nA_assumption": 30e-9 * 180e3 * 1.01,
        "reference_temp_full_range_16mV": 5 * 0.016 / 2.495,
        "reference_operating_current_shift_4mV_allocation": 5 * 0.004 / 2.495,
        "auxiliary_ADC_ratio_5LSB_unverified": 5 * auxiliary_ratio_error,
        "combined_resistor_thermal_0p6pct_allocation": 5 * 0.006,
    }
    print(json.dumps({
        "status": "conditional DC; no complete injection/transient/source-impedance/temperature proof",
        "assertion_count": checks,
        "off_rail_cases": rows,
        "off_rail_assumptions": "two inputs <=5V; 180k +/-1%; bleed4k7 +/-1%; no other injection; zero-Vf conservative",
        "reference_candidate": {"type": "TI TL431BCLP, 3.3V feed through 68ohm",
                                "min_current_a": ref_current_min, "max_current_a": ref_current_max,
                                "max_feed_resistor_w": (3.6 - ref_min) ** 2 / (68 * 0.99)},
        "revised_power_assumptions": {"peak_a": 0.270, "analog_a": 0.022,
                                      "sys_min_v": sys_min, "vana_min_v": rail_min,
                                      "upper_headroom_min_v": rail_min - max(highs)},
        "calibrated_error_allocations_v": allocations_v,
        "allocation_sum_v_not_guarantee": sum(allocations_v.values()),
    }, indent=2))


if __name__ == "__main__":
    main()
