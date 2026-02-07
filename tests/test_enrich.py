import unittest
from packspec.types import PackSpecResult
from packspec.units import Dim
from packspec.enrich import enrich



class TestEnrich(unittest.TestCase):
    def test_volume_and_dim_weight(self):
        r = PackSpecResult(case_dims=Dim(10, 10, 10, "in"), confidence=0.8, notes=[])
        r = enrich(r)
        self.assertIsNotNone(r.case_volume_cuin)
        self.assertIsNotNone(r.dim_weight_lb)


if __name__ == "__main__":
    unittest.main()
