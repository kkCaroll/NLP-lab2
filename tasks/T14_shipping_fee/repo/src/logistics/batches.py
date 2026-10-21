"""Batch parcel helpers."""

from decimal import Decimal

from .fees import shipping_fee
from .parcels import parse_many
from .rates import CENT


def batch_total(parcels):
    """Return the total shipping fee for several parcels."""
    parsed = parse_many(parcels)
    total = sum(
        (shipping_fee(item) for item in parcels),
        start=Decimal("0.00"),
    )
    return total.quantize(CENT)


def group_by_zone(parcels):
    """Return parcel ids grouped by shipping zone."""
    groups = {}
    for item in parse_many(parcels):
        groups.setdefault(item["zone"], []).append(item["id"])
    return groups


def heaviest_parcel(parcels):
    """Return the normalized parcel with the largest weight."""
    prepared = parse_many(parcels)
    if not prepared:
        raise ValueError("parcels must not be empty")
    return max(prepared, key=lambda item: item["weight_kg"])


def express_parcels(parcels):
    """Return only the parcels that use express service."""
    return [item for item in parse_many(parcels) if item["express"]]


def batch_summary(parcels):
    """Return a compact summary of a parcel batch."""
    prepared = parse_many(parcels)
    total = batch_total(parcels)
    return (
        f"{len(prepared)} parcels, "
        f"{len(express_parcels(parcels))} express, total {total:.2f}"
    )
