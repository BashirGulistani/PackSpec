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


