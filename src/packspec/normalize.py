from __future__ import annotations
from typing import Optional, List
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE, PACKAGING_HINTS
from .units import Dim, Weight
from .types import PackSpecResult
from .utils import clean_text, safe_int, safe_float, clamp01
from .rules import RulePack



def _unit_dim(u: str) -> str:
    u = (u or "").lower().strip()
    if u in {"in", "inch", "inches", '"'}:
        return "in"
    if u in {"cm", "centimeter", "centimeters"}:
        return "cm"
    return "in"


def _unit_w(u: str) -> str:
    u = (u or "").lower().strip()
    if u in {"lb", "lbs", "pound", "pounds"}:
        return "lb"
    if u in {"kg", "kgs", "kilogram", "kilograms"}:
        return "kg"
    return "lb"


def normalize_packaging(
    text: str,
    *,
    supplier: Optional[str] = None,
    rulepack: RulePack | None = None,
) -> PackSpecResult:
    raw = text or ""
    s = clean_text(raw)
    notes: List[str] = []
    score = 0.0


    r = PackSpecResult(
        supplier=supplier,
        source_text=raw,
        notes=notes,
        confidence=0.0,
    )

    if not s:
        r.notes.append("empty_input")
        return r

    if rulepack:
        r.rule_applied = rulepack.name
        s2 = rulepack.apply_preprocess(s)
        if s2 != s:
            notes.append("preprocess_applied")
        s = s2

    case_pack_rx = re.compile(rulepack.case_pack_regex, re.IGNORECASE) if (rulepack and rulepack.case_pack_regex) else CASE_PACK_RE
    inner_pack_rx = re.compile(rulepack.inner_pack_regex, re.IGNORECASE) if (rulepack and rulepack.inner_pack_regex) else INNER_PACK_RE
    dims_rx = re.compile(rulepack.dims_regex, re.IGNORECASE) if (rulepack and rulepack.dims_regex) else DIMS_RE
    weight_rx = re.compile(rulepack.weight_regex, re.IGNORECASE) if (rulepack and rulepack.weight_regex) else WEIGHT_RE

    m = case_pack_rx.search(s)
    if m:
        qty = safe_int(m.group(1))
        if qty is not None:
            r.case_pack_qty = qty
            score += 0.25

    else:
        m2 = re.search(r"\b([0-9]{1,5})\s*(?:pcs|pc|units?)\s*/\s*(?:ctn|carton|case)\b", s, re.IGNORECASE)
        if m2:
            qty = safe_int(m2.group(1))
            if qty is not None:
                r.case_pack_qty = qty
                score += 0.20
                notes.append("case_pack_inferred_from_units_per_carton")

    m = inner_pack_rx.search(s)
    if m:
        qty = safe_int(m.group(1))
        if qty is not None:
            r.inner_pack_qty = qty
            score += 0.15

    m = dims_rx.search(s)
    if m:
        l = safe_float(m.group(1))
        w = safe_float(m.group(3))
        h = safe_float(m.group(5))
        u = _unit_dim(m.group(6))
        if l and w and h:
            r.case_dims = Dim(l=float(l), w=float(w), h=float(h), unit=u)
            score += 0.25

    m = weight_rx.search(s)
    if m:
        v = safe_float(m.group(1))
        u = _unit_w(m.group(2))
        if v is not None:
            r.case_weight = Weight(value=float(v), unit=u)
            score += 0.20

    if rulepack and rulepack.packaging_type:
        r.packaging_type = rulepack.packaging_type
        score += 0.10
        notes.append("packaging_type_forced_by_rulepack")
    else:
        for key, rx in PACKAGING_HINTS.items():
            if rx.search(s):
                r.packaging_type = key
                score += 0.10
                break
    low = s.lower()
    if r.case_pack_qty is None and ("case" in low or "carton" in low or "ctn" in low):
        notes.append("mentions_case_or_carton_but_no_qty_found")
    if r.case_dims is None and ("x" in low or "*" in s):
        notes.append("maybe_dims_but_unparsed")
    if r.case_weight is None and ("lb" in low or "kg" in low):
        notes.append("maybe_weight_but_unparsed")

    r.confidence = clamp01(score)
    return r
