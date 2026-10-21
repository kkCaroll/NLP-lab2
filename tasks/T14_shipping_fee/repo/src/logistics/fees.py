"""Shipping fee calculation."""

from .parcels import parse_parcel
from .rates import rate_breakdown


def shipping_fee(parcel):
    """Return the shipping fee for one parcel."""
    parsed = parse_parcel(parcel)
    breakdown = rate_breakdown(
        parsed["weight_kg"], parsed["zone"], parsed["express"]
    )
    return breakdown["total"]


def quote_summary(parcel):
    """Return a short quote line for one parcel."""
    parsed = parse_parcel(parcel)
    fee = shipping_fee(parcel)
    service = "express" if parsed["express"] else "standard"
    return (
        f"{parsed['id']}: {parsed['zone']} "
        f"{parsed['weight_kg']:.2f} kg {service} {fee:.2f}"
    )


def fee_table(parcels):
    """Return a mapping from parcel id to shipping fee."""
    if not isinstance(parcels, (list, tuple)):
        raise TypeError("parcels must be a list or tuple")
    return {
        parse_parcel(item)["id"]: shipping_fee(item) for item in parcels
    }
