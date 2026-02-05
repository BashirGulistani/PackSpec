from __future__ import annotations
from .units import Dim, Weight, normalize_dim, normalize_weight


def canonicalize(dim: Dim | None, weight: Weight | None, *, dim_unit: str = "in", weight_unit: str = "lb"):
    nd = normalize_dim(dim, to_unit=dim_unit) if dim else None
    nw = normalize_weight(weight, to_unit=weight_unit) if weight else None
    return nd, nw
