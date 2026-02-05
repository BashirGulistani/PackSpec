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



def dim_weight_lb_from_cuin(cuin: float, divisor: float = 139.0) -> float:
    return float(cuin / divisor) if divisor > 0 else 0.0


def enrich(result: PackSpecResult, *, dim_divisor_in: float = 139.0) -> PackSpecResult:
    r = result

    if r.case_dims:
        cuin = volume_cuin(r.case_dims)
        r.case_volume_cuin = round(cuin, 3)

        cc = volume_cc(r.case_dims)
        r.case_volume_cc = round(cc, 3)

        dw_lb = dim_weight_lb_from_cuin(cuin, divisor=dim_divisor_in)
        r.dim_weight_lb = round(dw_lb, 3)
        r.dim_weight_kg = round(lb_to_kg(dw_lb), 3)

    return r
