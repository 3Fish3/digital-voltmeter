"""Tests of conditional arithmetic and guardrails, not hardware stability tests."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ref_budget", BASE / "scripts/reference_sampling_budget.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load reference budget")
BUDGET = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUDGET)


class ReferenceSamplingBudgetTests(unittest.TestCase):
    def setUp(self):
        try:
            self.blueprint = json.loads((BASE / "hardware/v2.3/connections-draft.json").read_text())
        except (OSError, ValueError) as exc:
            raise RuntimeError("Missing connection blueprint") from exc
        self.result = BUDGET.calculate()

    def test_actual_connections(self):
        BUDGET.check_connections(self.blueprint)

    def test_reject_wrong_feed_resistor(self):
        data = copy.deepcopy(self.blueprint)
        next(c for c in data["components"] if c["reference"] == "R40")["value"] = "680R 1%"
        with self.assertRaises(ValueError):
            BUDGET.check_connections(data)

    def test_reject_extra_node_capacitor(self):
        data = copy.deepcopy(self.blueprint)
        data["components"].append({"reference": "C999", "lib_id": "Device:C_Small",
                                   "value": "100n", "pins": {"1": "REF_2V495", "2": "GND"}})
        with self.assertRaises(ValueError):
            BUDGET.check_connections(data)

    def test_reject_wrong_monitor_endpoint(self):
        data = copy.deepcopy(self.blueprint)
        next(c for c in data["components"] if c["reference"] == "M1")["pins"]["9"] = "MON_REF"
        with self.assertRaises(ValueError):
            BUDGET.check_connections(data)

    def test_reject_reference_pin_miswire(self):
        data = copy.deepcopy(self.blueprint)
        next(c for c in data["components"] if c["reference"] == "U6")["pins"]["3"] = "GND"
        with self.assertRaises(ValueError):
            BUDGET.check_connections(data)

    def test_conditional_cathode_current(self):
        current = self.result["current"]
        self.assertGreater(current["conditional_cathode_low_a"], current["recommended_cathode_min_a"])
        self.assertLess(current["conditional_cathode_high_a"], current["recommended_cathode_max_a"])
        self.assertAlmostEqual(current["feed_min_a"], 0.0069452533488643)

    def test_source_corner(self):
        self.assertAlmostEqual(self.result["sampling"]["pa0_source_max_ohm"], 6060)

    def test_quarter_lsb_settle(self):
        sample = self.result["sampling"]
        self.assertAlmostEqual(sample["pa0_quarter_lsb_settle_s"] * 1e6, 0.548085338612, places=6)
        self.assertLess(sample["pa0_quarter_lsb_settle_s"], sample["sample_time_s"])

    def test_group_timing(self):
        sample = self.result["sampling"]
        self.assertAlmostEqual(sample["conversion_time_s"], 18e-6)
        self.assertAlmostEqual(sample["two_groups_per_frame_lower_bound_s"], 216e-6)

    def test_discarded_samples_still_draw_charge(self):
        current = self.result["current"]
        self.assertEqual(current["pa1_conversions_per_second"], 160)
        self.assertAlmostEqual(current["absolute_average_sampling_charge_current_bound_a"], 3.22944e-9)

    def test_four_millivolt_sensitivity(self):
        current = self.result["current"]
        self.assertGreater(current["extra_4mV_reference_shift_sensitivity_low_a"], 0.001)
        self.assertLess(current["extra_4mV_reference_shift_sensitivity_low_a"], current["conditional_cathode_low_a"])


if __name__ == "__main__":
    unittest.main()
