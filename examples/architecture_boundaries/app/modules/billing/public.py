"""Intentionally small public application contract for the example."""
from app.modules.billing.domain import validated_minor_units


def total_minor_units(value: int) -> int:
    return validated_minor_units(value)
