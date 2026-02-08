from __future__ import annotations
import json
import html
from pathlib import Path
from typing import Any, Optional
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE


def _h(x: Any) -> str:
    return html.escape("" if x is None else str(x))




def _pyre_to_js_literal(rx: re.Pattern) -> str:
    pat = rx.pattern.replace("\\", "\\\\").replace("/", "\\/")
    flags = "i" if (rx.flags & re.IGNORECASE) else ""
    return f"/{pat}/{flags}"








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

    default_case_pack = _pyre_to_js_literal(CASE_PACK_RE)
    default_inner_pack = _pyre_to_js_literal(INNER_PACK_RE)
    default_dims = _pyre_to_js_literal(DIMS_RE)
    default_weight = _pyre_to_js_literal(WEIGHT_RE)

    html_text = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{_h(title)}</title>
<style>
  :root {{
    --bg: #0b0b0b;
    --panel: rgba(255,255,255,.06);
    --border: rgba(255,255,255,.12);
    --muted: #b9b9b9;
    --text: #eee;
    --chip: rgba(255,255,255,.08);

    --hl-dims-bg: rgba(76, 175, 80, .18);
    --hl-dims-br: rgba(76, 175, 80, .35);

    --hl-weight-bg: rgba(33, 150, 243, .18);
    --hl-weight-br: rgba(33, 150, 243, .35);

    --hl-qty-bg: rgba(255, 193, 7, .16);
    --hl-qty-br: rgba(255, 193, 7, .35);
  }}
  body {{
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
    margin: 22px;
    background: var(--bg);
    color: var(--text);
  }}
  .top {{
    display:flex; gap:12px; align-items:flex-end; justify-content:space-between;
    flex-wrap:wrap;
    margin-bottom: 14px;
  }}
  h1 {{ margin:0; font-size: 20px; }}
  .muted {{ color: var(--muted); font-size: 13px; }}
  .card {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px;
  }}



