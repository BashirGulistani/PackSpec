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






