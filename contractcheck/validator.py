from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    path: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


_TYPES = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "object": dict,
    "array": list,
    "null": type(None),
}


def _type_matches(value: Any, expected: str) -> bool:
    if expected not in _TYPES:
        raise ValueError(f"Unsupported contract type: {expected}")
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[expected])


def _validate_node(value: Any, contract: dict[str, Any], path: str, errors: list[ValidationError]) -> None:
    expected = contract.get("type")
    if not isinstance(expected, str):
        raise ValueError(f"Contract at {path} is missing a string type")
    if not _type_matches(value, expected):
        errors.append(ValidationError(path, "type", f"expected {expected}, got {type(value).__name__}"))
        return

    if expected == "object":
        properties = contract.get("properties", {})
        if not isinstance(properties, dict):
            raise ValueError(f"Contract properties at {path} must be an object")
        required = contract.get("required", [])
        if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
            raise ValueError(f"Contract required list at {path} is invalid")
        for name in required:
            if name not in value:
                errors.append(ValidationError(f"{path}.{name}", "required", "required field is missing"))
        if contract.get("additionalProperties", True) is False:
            for name in value.keys() - properties.keys():
                errors.append(ValidationError(f"{path}.{name}", "unknown", "field is not allowed by contract"))
        for name, child_contract in properties.items():
            if name in value:
                _validate_node(value[name], child_contract, f"{path}.{name}", errors)

    if expected == "array" and "items" in contract:
        for index, item in enumerate(value):
            _validate_node(item, contract["items"], f"{path}[{index}]", errors)


def validate(value: Any, contract: dict[str, Any]) -> tuple[ValidationError, ...]:
    errors: list[ValidationError] = []
    _validate_node(value, contract, "$", errors)
    return tuple(errors)
