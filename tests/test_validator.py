import json
import unittest
from pathlib import Path

from contractcheck import validate


ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads((ROOT / "examples" / "contract.json").read_text(encoding="utf-8"))

    def test_accepts_valid_response(self) -> None:
        response = json.loads((ROOT / "tests" / "fixtures" / "valid.json").read_text(encoding="utf-8"))
        self.assertEqual((), validate(response, self.contract))

    def test_reports_precise_paths_for_invalid_response(self) -> None:
        response = json.loads((ROOT / "tests" / "fixtures" / "invalid.json").read_text(encoding="utf-8"))
        errors = validate(response, self.contract)
        paths = {error.path for error in errors}
        self.assertEqual({"$.debug", "$.page", "$.jobs[0].id", "$.jobs[0].title", "$.jobs[0].remote", "$.jobs[0].extra"}, paths)

    def test_rejects_unknown_contract_type(self) -> None:
        with self.assertRaises(ValueError):
            validate("x", {"type": "uuid"})


if __name__ == "__main__":
    unittest.main()
