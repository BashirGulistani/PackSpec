from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, Tuple, List
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE, PACKAGING_HINTS
from .units import Dim, Weight


def _clean(s: str) -> str:
    return (s or "").strip()


def _unit_dim(u: str) -> str:
    u = u.lower().strip()
    if u in {"in", "inch", "inches", '"'}:
        return "in"
    if u in {"cm", "centimeter", "centimeters"}:
        return "cm"
    return "in"


def _unit_w(u: str) -> str:
    u = u.lower().strip()
    if u in {"lb", "lbs", "pound", "pounds"}:
        return "lb"
    if u in {"kg", "kgs", "kilogram", "kilograms"}:
        return "kg"
    return "lb"


@dataclass
class NormalizedPackaging:
    case_pack_qty: Optional[int] = None
    inner_pack_qty: Optional[int] = None
    case_dims: Optional[Dim] = None
    case_weight: Optional[Weight] = None
    packaging_type: Optional[str] = None
    confidence: float = 0.0
    notes: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.case_dims:
            d["case_dims"] = {"l": self.case_dims.l, "w": self.case_dims.w, "h": self.case_dims.h, "unit": self.case_dims.unit}
        if self.case_weight:
            d["case_weight"] = {"value": self.case_weight.value, "unit": self.case_weight.unit}
        if d.get("notes") is None:
            d["notes"] = []
        return d






