"""Shipping rate tables and helpers."""

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
BASE_FEE = Decimal("5.00")
PER_KILOGRAM = Decimal("2.50")
EXPRESS_MULTIPLIER = Decimal("1.50")
ZONE_SURCHARGES = {
    "north": Decimal("0.00"),
    "south": Decimal("2.00"),
    "remote": Decimal("5.00"),
}


def zone_surcharge(zone):
    """Return the surcharge for a shipping zone."""
    if not isinstance(zone, str):
        raise TypeError("zone must be a string")
    normalized = zone.strip().lower()
    if normalized not in ZONE_SURCHARGES:
        raise ValueError("unknown zone")
    return ZONE_SURCHARGES[normalized]


def base_rate(weight_kg):
    """Return the base fee for a weight in kilograms."""
    weight = Decimal(str(weight_kg))
    if weight < 0:
        raise ValueError("weight must be non-negative")
    return (BASE_FEE + PER_KILOGRAM * weight).quantize(
        CENT, rounding=ROUND_HALF_UP
    )


def express_multiplier(express):
    """Return the multiplier for standard or express service."""
    if not isinstance(express, bool):
        raise TypeError("express must be boolean")
    return EXPRESS_MULTIPLIER if express else Decimal("1.00")


def rate_breakdown(weight_kg, zone, express=False):
    """Return the components of a shipping rate."""
    base = base_rate(weight_kg)
    surcharge = zone_surcharge(zone)
    multiplier = express_multiplier(express)
    total = ((base + surcharge) * multiplier).quantize(
        CENT, rounding=ROUND_HALF_UP
    )
    return {
        "base": base,
        "surcharge": surcharge,
        "multiplier": multiplier,
        "total": total,
    }
