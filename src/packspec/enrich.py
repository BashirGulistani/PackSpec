from __future__ import annotations
from typing import Optional
from .units import Dim, Weight, normalize_dim, normalize_weight, lb_to_kg
from .types import PackSpecResult


def volume_cuin(dim: Dim) -> float:
    d = normalize_dim(dim, to_unit="in")
    return float(d.l * d.w * d.h)





def volume_cc(dim: Dim) -> float:
    d = normalize_dim(dim, to_unit="cm")
    return float(d.l * d.w * d.h)




