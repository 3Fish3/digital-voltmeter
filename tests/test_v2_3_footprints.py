import importlib.util
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('v23_footprints', BASE / 'scripts/verify_v2_3_footprints.py')
if SPEC is None or SPEC.loader is None:
    raise RuntimeError('Cannot load footprint verifier')
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class FootprintVerificationTests(unittest.TestCase):
    def test_actual_assignments(self):
        result = VERIFIER.verify(BASE / '.tmp/v2.3-validation/voltmeter-v2.3-draft.xml')
        self.assertEqual(result['assigned_count'], 64)
        self.assertEqual(result['unassigned_count'], 0)
        self.assertEqual(result['unassigned_references'], [])
        by_ref = {item['reference']: item for item in result['components']}
        self.assertEqual(by_ref['Q1']['symbol_pins'], ['D', 'G', 'S'])
        self.assertEqual([pad['number'] for pad in by_ref['Q1']['pads']], ['G', 'S', 'D'])
        self.assertEqual(by_ref['Q2']['symbol_pins'], ['B', 'C', 'E'])
        self.assertEqual([pad['number'] for pad in by_ref['Q2']['pads']], ['E', 'B', 'C'])
        self.assertEqual(by_ref['U6']['symbol_pins'], ['1', '2', '3'])
        self.assertTrue(all(pad['drill_mm'][0] == 0.85 for pad in by_ref['U6']['pads']))


if __name__ == '__main__':
    unittest.main()
