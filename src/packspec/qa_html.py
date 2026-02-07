from __future__ import annotations
import json
import html
from pathlib import Path
from typing import Any


def _h(x: Any) -> str:
    return html.escape("" if x is None else str(x))




def write_interactive_qa_html(
    path: str,
    *,
    rows: list[dict],
    text_col: str,
    supplier_col: str | None = None,
    title: str = "PackSpec QA Report",
    default_low_threshold: float = 0.45,
    max_rows: int = 5000,
) -> None:
    """
    Writes a self-contained interactive HTML report for QA.
    - Search
    - Sort columns
    - Confidence threshold slider + low-only toggle
    - Expandable row details (raw text, notes, rule applied)
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    data = rows[:max_rows]


    def pick(r: dict) -> dict:
        dims = {
            "l": r.get("case_dim_l"),
            "w": r.get("case_dim_w"),
            "h": r.get("case_dim_h"),
            "u": r.get("case_dim_unit"),
        }
        return {
            "supplier": (r.get(supplier_col) if supplier_col else None),
            "confidence": float(r.get("confidence") or 0.0),
            "case_pack_qty": r.get("case_pack_qty"),
            "inner_pack_qty": r.get("inner_pack_qty"),
            "case_weight_value": r.get("case_weight_value"),
            "case_weight_unit": r.get("case_weight_unit"),
            "dims": dims,
            "packaging_type": r.get("packaging_type"),
            "rule_applied": r.get("rule_applied"),
            "notes": r.get("notes"),
            "raw": r.get(text_col),
        }

    payload = [pick(r) for r in data]
    payload_json = json.dumps(payload)




