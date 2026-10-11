"""Domain logic has no framework or database dependencies."""


def validated_minor_units(value: int) -> int:
    if value < 0:
        raise ValueError("minor units must not be negative")
    return value
