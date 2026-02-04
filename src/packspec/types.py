from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

from .units import Dim, Weight


@dataclass
class PackSpecResult:
    case_pack_qty: Optional[int] = None
    inner_pack_qty: Optional[int] = None
    case_dims: Optional[Dim] = None
    case_weight: Optional[Weight] = None
    packaging_type: Optional[str] = None

    case_volume_cuin: Optional[float] = None
    case_volume_cc: Optional[float] = None
    dim_weight_lb: Optional[float] = None
    dim_weight_kg: Optional[float] = None

    confidence: float = 0.0
    notes: List[str] = field(default_factory=list)

    supplier: Optional[str] = None
    source_text: Optional[str] = None
    rule_applied: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.case_dims:
            d["case_dims"] = {
                "l": self.case_dims.l,
                "w": self.case_dims.w,
                "h": self.case_dims.h,
                "unit": self.case_dims.unit,
            }
        if self.case_weight:
            d["case_weight"] = {
                "value": self.case_weight.value,
                "unit": self.case_weight.unit,
            }
        return d




