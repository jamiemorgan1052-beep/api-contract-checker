# JSON API Contract Checker

A dependency-free Python CLI that validates saved JSON API responses against a
compact, reviewable contract. It is designed for CI checks, integration QA, and
handoffs where deterministic error locations matter.

![Abstract project illustration](docs/featured.png)

Need a small API-QA or automation task delivered for you? Book the fixed-scope [Python Automation, Data Cleanup & QA service](https://contra.com/s/mXUk6X3o-python-automation-data-cleanup-and-qa) from USD 75.

Prefer a reusable download? Buy the [single-user commercial toolkit for USD 19](https://contra.com/products/7dM3HzIe-json-api-contract-checker-python-toolkit).

## Features

- Nested object and array validation
- Required and optional fields
- String, integer, number, boolean, object, array, and null types
- Unknown-field detection
- JSON-path error locations
- Machine-readable JSON reports
- Non-zero exit status when validation fails

## Requirements

- Python 3.10 or newer
- No third-party packages

## Quick start

Validate the included passing fixture:

```powershell
python -m contractcheck.cli `
  --contract examples/contract.json `
  --response tests/fixtures/valid.json `
  --report report.json
```

Console result:

```text
PASS: 0 contract error(s)
```

The report is suitable for CI artifacts:

```json
{
  "valid": true,
  "error_count": 0,
  "errors": []
}
```

Running the same command against `tests/fixtures/invalid.json` returns exit
status `1` and reports six contract errors. Invalid command input returns exit
status `2`.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Scope

The tool checks response structure from local files. It does not send network
requests, validate business meaning, or replace API security testing.

See [PROVENANCE.md](PROVENANCE.md) for authorship and AI-assistance disclosure.
Licensed under the [MIT License](LICENSE).
