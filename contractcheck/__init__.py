"""Small JSON API contract validator."""

from .validator import ValidationError, validate

__all__ = ["ValidationError", "validate"]
