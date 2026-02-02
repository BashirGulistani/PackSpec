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



def normalize_packaging(text: str) -> NormalizedPackaging:
    s = _clean(text)
    notes: List[str] = []
    score = 0.0

    out = NormalizedPackaging(notes=notes)

    if not s:
        out.notes.append("empty_input")
        out.confidence = 0.0
        return out

    m = CASE_PACK_RE.search(s)
    if m:
        out.case_pack_qty = int(m.group(1))
        score += 0.25
    else:
        m2 = re.search(r"\b([0-9]{1,5})\s*(?:pcs|pc|units?)\s*/\s*(?:ctn|carton|case)\b", s, re.IGNORECASE)
        if m2:
            out.case_pack_qty = int(m2.group(1))
            score += 0.20
            notes.append("case_pack_inferred_from_units_per_carton")

    m = INNER_PACK_RE.search(s)
    if m:
        out.inner_pack_qty = int(m.group(1))
        score += 0.15

    m = DIMS_RE.search(s)
    if m:
        l = float(m.group(1)); w = float(m.group(3)); h = float(m.group(5))
        u = _unit_dim(m.group(6))
        out.case_dims = Dim(l=l, w=w, h=h, unit=u)
        score += 0.25

    m = WEIGHT_RE.search(s)
    if m:
        v = float(m.group(1))
        u = _unit_w(m.group(2))
        out.case_weight = Weight(value=v, unit=u)
        score += 0.20

    ptype = None
    for key, rx in PACKAGING_HINTS.items():
        if rx.search(s):
            ptype = key
            break
    if ptype:
        out.packaging_type = ptype
        score += 0.10

    out.confidence = min(1.0, score)

    if out.case_pack_qty is None and ("case" in s.lower() or "carton" in s.lower()):
        notes.append("mentions_case_or_carton_but_no_qty_found")
    if out.case_dims is None and ("x" in s.lower() or "*" in s):
        notes.append("maybe_dims_but_unparsed")
    if out.case_weight is None and ("lb" in s.lower() or "kg" in s.lower()):
        notes.append("maybe_weight_but_unparsed")

    return out


