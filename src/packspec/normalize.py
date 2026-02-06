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


