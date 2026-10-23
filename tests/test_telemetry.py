import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
from telemetry import parse_packet

class PacketTests(unittest.TestCase):
    def test_valid(self):
        t = parse_packet('23.4,42.8,0.55,DANGER')
        self.assertEqual(t.status, 'DANGER')
        self.assertAlmostEqual(t.distance_cm, 23.4)
        self.assertAlmostEqual(t.ttc_s, 0.55)
    def test_no_signal(self):
        self.assertIsNone(parse_packet('NO_SIGNAL'))
    def test_ttc_unavailable(self):
        self.assertIsNone(parse_packet('90.0,-2.3,-1,SAFE').ttc_s)
    def test_bad_packet(self):
        for text in ['DIST: 30cm', '2296,0,-1,SAFE', 'nan,0,-1,SAFE', '33,0,-1,MAYBE']:
            with self.assertRaises(ValueError): parse_packet(text)

if __name__ == '__main__':
    unittest.main()
