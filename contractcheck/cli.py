from __future__ import annotations

import argparse
import json
from pathlib import Path

from .validator import validate


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a saved JSON API response")
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    response = json.loads(args.response.read_text(encoding="utf-8"))
    errors = validate(response, contract)
    report = {"valid": not errors, "error_count": len(errors), "errors": [error.to_dict() for error in errors]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"{'PASS' if not errors else 'FAIL'}: {len(errors)} contract error(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
