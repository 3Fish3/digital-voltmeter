"""Reproducible DC candidate budgets; not a circuit simulation or safety proof.

Run from the repository root. JSON is printed, not written implicitly.
All power inputs are assumptions explicitly named below.
"""
import itertools
import json
import math


def front_end(rs, rg, rb, vin, supply):
    gs, gg = 1 / rs, 1 / rg
    gb = 0 if rb is None else 1 / rb
    total = gs + gg + gb
    alpha, beta = gs / total, gb / total
    node = alpha * vin + beta * supply
    return {
        "alpha": alpha,
        "beta": beta,
        "node_v": node,
        "input_current_a": (vin - node) / rs,
        "incremental_input_ohm": rs + 1 / (gg + gb),
        "thevenin_ohm": 1 / total,
        "upper_headroom_v": supply - node,
        "input_step_v": supply / (256 * alpha),
    }


def corners(rs, rg, rb, supply):
    rows = []
    for factors in itertools.product((0.99, 1.01), repeat=3 if rb else 2):
        s, g = rs * factors[0], rg * factors[1]
        b = None if rb is None else rb * factors[2]
        low = front_end(s, g, b, 0, supply)
        high = front_end(s, g, b, 5, supply)
        rows.append((low, high))
    return {
        "incremental_input_min_ohm": min(lo["incremental_input_ohm"] for lo, _ in rows),
        "zero_node_min_v": min(lo["node_v"] for lo, _ in rows),
        "five_node_max_v": max(hi["node_v"] for _, hi in rows),
        "upper_headroom_min_v": min(hi["upper_headroom_v"] for _, hi in rows),
    }


def main():
    # These are allocated limits, not measured module or board values.
    vin_min = 4.75  # Required voltage AT BOARD CONNECTOR, not adapter nameplate.
    total_peak_a = 0.25
    input_path_budget_ohm = 0.25  # fuse, connector, PFET where fitted, routing
    mux_max_ohm = 0.15  # TPS2115A max at listed hot electrical test condition
    analog_peak_a = 0.02
    analog_series_ohm = 1.01  # 1 ohm nominal, +1% tolerance worst case
    sys_min = vin_min - total_peak_a * (input_path_budget_ohm + mux_max_ohm)
    vana_min = sys_min - analog_peak_a * analog_series_ohm
    assert math.isclose(vana_min, 4.6298)
    assert math.isclose(front_end(120e3, 1.2e6, 10e6, 5, 5)["node_v"], 4.550359712230216)
    cases = []
    for rs in (120e3, 180e3):
        for rb in (None, 10e6):
            for supply in (4.5, vana_min, 4.63, 4.7, 5.0, 5.25):
                cases.append({
                    "rs_ohm": rs, "rg_ohm": 1.2e6, "rb_ohm": rb,
                    "supply_v": supply,
                    "zero": front_end(rs, 1.2e6, rb, 0, supply),
                    "five": front_end(rs, 1.2e6, rb, 5, supply),
                    "resistor_1pct_corners": corners(rs, 1.2e6, rb, supply),
                })
    new = corners(180e3, 1.2e6, 10e6, vana_min)
    plain = corners(180e3, 1.2e6, None, vana_min)
    assert new["incremental_input_min_ohm"] > 1e6
    assert plain["incremental_input_min_ohm"] > 1e6
    assert new["upper_headroom_min_v"] > 0.25
    assert plain["upper_headroom_min_v"] > 0.25
    assert corners(120e3, 1.2e6, 10e6, 4.5)["upper_headroom_min_v"] < 0
    expected = front_end(180e3, 1.2e6, None, 5, 5)
    assert math.isclose(expected["alpha"], 1.2 / 1.38)
    assert front_end(180e3, 1.2e6, None, 0, 5)["input_current_a"] == 0
    assert front_end(180e3, 1.2e6, 10e6, 0, 5)["input_current_a"] < 0
    rc_tau = 220 * 100e-9
    output = {
        "status": "DC candidate calculation only; no leakage/opamp/transient/thermal/USB compliance proof",
        "power_assumptions": {
            "connector_min_v": vin_min, "connector_max_v": 5.25,
            "total_peak_a": total_peak_a,
            "input_path_budget_ohm": input_path_budget_ohm,
            "mux_hot_max_ohm": mux_max_ohm,
            "analog_peak_a": analog_peak_a,
            "analog_series_ohm": analog_series_ohm,
            "sys_min_v": sys_min, "vana_min_v": vana_min,
        },
        "rc_candidate": {"tau_s": rc_tau, "cutoff_hz": 1 / (2 * math.pi * rc_tau),
                         "ideal_half_lsb_settle_s": math.log(512) * rc_tau},
        "cases": cases,
        "assertions": "10 DC sanity checks passed",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
