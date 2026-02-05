from __future__ import annotations
from .types import PackSpecResult
from .utils import clamp01


def validate_and_score(r: PackSpecResult) -> PackSpecResult:
    notes = r.notes

    score = r.confidence

    if r.case_pack_qty is not None:
        if r.case_pack_qty <= 0:
            notes.append("invalid_case_pack_qty")
            score -= 0.25
        elif r.case_pack_qty > 50000:
            notes.append("suspiciously_large_case_pack_qty")
            score -= 0.10



    if r.inner_pack_qty is not None:
        if r.inner_pack_qty <= 0:
            notes.append("invalid_inner_pack_qty")
            score -= 0.20
        elif r.case_pack_qty and r.inner_pack_qty > r.case_pack_qty:
            notes.append("inner_pack_gt_case_pack")
            score -= 0.10





