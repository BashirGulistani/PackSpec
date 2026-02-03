import unittest
from packspec.normalize import normalize_packaging



class TestNormalize(unittest.TestCase):
    def test_case_pack_dims_weight(self):
        s = "Carton: 24 pcs, 18x12x10 in, 22 lb"
        out = normalize_packaging(s)
        self.assertEqual(out.case_pack_qty, 24)
        self.assertIsNotNone(out.case_dims)
        self.assertEqual(out.case_dims.unit, "in")
        self.assertIsNotNone(out.case_weight)
        self.assertEqual(out.case_weight.unit, "lb")
        self.assertGreater(out.confidence, 0.6)

