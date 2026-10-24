"""Regression tests for the exported draft's verification guardrails."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("v23_verify", BASE / "scripts/verify_v2_3_netlist.py")
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Cannot load verifier")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class NetlistVerificationTests(unittest.TestCase):
    def setUp(self):
        self.blueprint = BASE / "hardware/v2.3/connections-draft.json"
        self.netlist = BASE / ".tmp/v2.3-validation/voltmeter-v2.3-draft.xml"
        try:
            self.original = json.loads(self.blueprint.read_text())
        except (OSError, ValueError) as exc:
            raise RuntimeError("Blueprint fixture unavailable") from exc

    def check_rejected(self, mutate):
        changed = copy.deepcopy(self.original)
        mutate(changed)
        with tempfile.TemporaryDirectory(dir=self.netlist.parent) as temporary:
            path = Path(temporary) / "changed.json"
            path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                VERIFIER.verify(path, self.netlist)

    def test_actual_export(self):
        result = VERIFIER.verify(self.blueprint, self.netlist)
        self.assertEqual(result["component_count"], 64)
        self.assertEqual(result["wired_pin_count"], 183)
        self.assertEqual(result["assigned_footprints"], 61)
        self.assertEqual(result["unassigned_footprints"], 3)
        self.assertEqual(result["power_declaration_count"], 3)

    def test_wrong_net(self):
        self.check_rejected(lambda data: data["components"][0]["pins"].update({"2": "WRONG_NET"}))

    def test_missing_component(self):
        self.check_rejected(lambda data: data["components"].pop())

    def test_nc_connected(self):
        self.check_rejected(lambda data: data["components"][2]["pins"].update({"11": "GND"}))

    def test_wrong_resistance(self):
        def mutate(data):
            next(c for c in data["components"] if c["reference"] == "R10")["value"] = "18k 1%"
        self.check_rejected(mutate)

    def test_wrong_symbol(self):
        self.check_rejected(lambda data: data["components"][0].update({"lib_id": "OtherLibrary:ADC0832_Draft"}))

    def test_missing_power_declaration(self):
        self.check_rejected(lambda data: data["power_declarations"].pop())

    def test_wrong_power_declaration_net(self):
        self.check_rejected(lambda data: data["power_declarations"][0].update({"net": "GND"}))

    def test_moved_power_declaration(self):
        self.check_rejected(lambda data: data["power_declarations"][0].update({"x": 1.0}))


if __name__ == "__main__":
    unittest.main()
