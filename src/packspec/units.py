from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Dim:
    l: float
    w: float
    h: float
    unit: str  # "in" or "cm"






