import unittest
from packspec.rules import RulePack


class TestRules(unittest.TestCase):
    def test_preprocess(self):
        rp = RulePack(
            name="x",
            supplier="acme",

            preprocess=[{"pattern": r"\bctn\b", "repl": "carton"}],
        )
        out = rp.apply_preprocess("12 ctn")
        self.assertIn("carton", out)


if __name__ == "__main__":
    unittest.main()
