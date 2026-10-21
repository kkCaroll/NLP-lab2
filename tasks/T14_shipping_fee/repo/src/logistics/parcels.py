"""Parcel parsing helpers."""

from decimal import Decimal

from .units import normalize_unit, to_kilograms

ZONES = {"north", "south", "remote"}


def parse_parcel(data):
    """Return a normalized parcel dictionary."""
    if not isinstance(data, dict):
        raise TypeError("parcel must be a mapping")
    for field in ("id", "weight", "unit", "zone"):
        if field not in data:
            raise ValueError(f"parcel is missing {field}")
    zone = data["zone"]
    if not isinstance(zone, str):
        raise TypeError("zone must be a string")
    zone = zone.strip().lower()
    if zone not in ZONES:
        raise ValueError("zone must be north, south or remote")
    express = data.get("express", False)
    if not isinstance(express, bool):
        raise TypeError("express must be boolean")
    return {
        "id": str(data["id"]),
        "weight_kg": to_kilograms(data["weight"], data["unit"]),
        "unit": normalize_unit(data["unit"]),
        "zone": zone,
        "express": express,
    }


def parse_many(items):
    """Return normalized parcels for a list or tuple of mappings."""
    if isinstance(items, (str, bytes)) or not isinstance(items, (list, tuple)):
        raise TypeError("items must be a list or tuple")
    return [parse_parcel(item) for item in items]


def describe_parcel(parcel):
    """Return a one-line description of a parcel."""
    parsed = parse_parcel(parcel)
    service = "express" if parsed["express"] else "standard"
    return (
        f"{parsed['id']} {parsed['weight_kg']:.2f}kg "
        f"{parsed['zone']} {service}"
    )


def total_weight(parcels):
    """Return the combined weight of several parcels in kilograms."""
    weights = [parse_parcel(item)["weight_kg"] for item in parcels]
    if not weights:
        return Decimal("0")
    return sum(weights, start=Decimal("0")) / len(weights)
