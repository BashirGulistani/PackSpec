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





