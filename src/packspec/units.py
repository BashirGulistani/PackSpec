from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Dim:
    l: float
    w: float
    h: float
    unit: str  # "in" or "cm"






@dataclass(frozen=True)
class Weight:
    value: float
    unit: str  # "lb" or "kg"


def cm_to_in(x: float) -> float:
    return x / 2.54


def in_to_cm(x: float) -> float:
    return x * 2.54


def kg_to_lb(x: float) -> float:
    return x * 2.2046226218


