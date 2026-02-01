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



def lb_to_kg(x: float) -> float:
    return x / 2.2046226218


def normalize_dim(dim: Dim, to_unit: str = "in") -> Dim:
    if dim.unit == to_unit:
        return dim
    if dim.unit == "cm" and to_unit == "in":
        return Dim(cm_to_in(dim.l), cm_to_in(dim.w), cm_to_in(dim.h), "in")
    if dim.unit == "in" and to_unit == "cm":
        return Dim(in_to_cm(dim.l), in_to_cm(dim.w), in_to_cm(dim.h), "cm")
    return dim


def normalize_weight(w: Weight, to_unit: str = "lb") -> Weight:
    if w.unit == to_unit:
        return w
    if w.unit == "kg" and to_unit == "lb":
        return Weight(kg_to_lb(w.value), "lb")
    if w.unit == "lb" and to_unit == "kg":
        return Weight(lb_to_kg(w.value), "kg")
    return w

