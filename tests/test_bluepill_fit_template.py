import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from bluepill_fit_template import render,main

class PinCentreTests(unittest.TestCase):
    def test_standard_geometry(self):
        root=ET.fromstring(render(15.24,2.54,20,True))
        circles=root.findall('.//{http://www.w3.org/2000/svg}circle')
        self.assertEqual(40,len(circles))
        self.assertTrue(root.get('width').endswith('mm'))
        a=[e for e in circles if e.get('data-row')=='A']
        b=[e for e in circles if e.get('data-row')=='B']
        self.assertAlmostEqual(float(b[0].get('cx'))-float(a[0].get('cx')),15.24)
        self.assertAlmostEqual(float(a[-1].get('cy'))-float(a[0].get('cy')),48.26)
    def test_provisional_marking(self):
        self.assertIn('NOT MEASURED',render(15.24,2.54,20,True))
        self.assertIn('NOT FOR PCB',render(15.16,2.54,20))
    def test_reject_invalid(self):
        for dims in ((0,2.54,20),(15.24,-1,20),(15.24,2.54,1),(float('nan'),2.54,20)):
            with self.subTest(dims=dims),self.assertRaises(ValueError): render(*dims)
    def test_cli_requires_measurement(self):
        with self.assertRaises(SystemExit) as ctx:
            main(['--output','/tmp/no-output.svg'])
        self.assertEqual(ctx.exception.code,2)

if __name__=='__main__': unittest.main()
