"""Allowed cross-module call via the other module's public application API."""
from app.modules.billing.public import total_minor_units


def describe_order(amount_minor_units: int) -> str:
    return f"Amount: {total_minor_units(amount_minor_units)}"
