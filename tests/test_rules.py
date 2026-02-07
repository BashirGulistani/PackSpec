import unittest
from packspec.rules import RulePack


class TestRules(unittest.TestCase):
    def test_preprocess(self):
        rp = RulePack(
            name="x",
            supplier="acme",

