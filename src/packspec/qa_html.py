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
  .controls {{
    display:grid;
    grid-template-columns: 1.4fr 1fr 1fr 1fr;
    gap: 10px;
    align-items:end;
  }}
  @media(max-width: 900px) {{
    .controls {{ grid-template-columns: 1fr; }}
  }}
  label {{ font-size: 12px; color: var(--muted); display:block; margin-bottom: 6px; }}
  input[type="text"], textarea {{
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,.03);
    color: var(--text);
    outline: none;
  }}
  textarea {{
    min-height: 92px;
    resize: vertical;
  }}
  input[type="range"] {{ width: 100%; }}
  .row {{
    display:flex; gap:10px; align-items:center; justify-content:space-between;
  }}
  .chip {{
    display:inline-block;
    padding: 4px 8px;
    border-radius: 999px;
    background: var(--chip);
    border: 1px solid var(--border);
    font-size: 12px;
    color: #ddd;
  }}
  .btn {{
    cursor:pointer;
    user-select:none;
    padding: 9px 11px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,.04);
    color: var(--text);
    font-size: 13px;
    white-space: nowrap;
  }}
  .btn:active {{ transform: translateY(1px); }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    font-size: 13px;
  }}
  th, td {{
    border-bottom: 1px solid rgba(255,255,255,.08);
    padding: 10px;
    vertical-align: top;
  }}
  th {{
    text-align:left;
    color: #ddd;
    cursor: pointer;
    position: sticky;
    top: 0;
    background: rgba(11,11,11,.92);
    backdrop-filter: blur(6px);
    z-index: 2;
  }}
  code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 12px;
  }}
  details {{
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 12px;
    padding: 10px 12px;
  }}
  summary {{
    cursor:pointer;
    color: #ddd;
    font-weight: 600;
  }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
  .small {{ font-size: 12px; color: var(--muted); }}
  .kvs {{
    display:grid;
    grid-template-columns: 140px 1fr;
    gap: 6px 12px;
    margin-top: 8px;
  }}
  .kvs div:nth-child(odd) {{ color: var(--muted); }}
  .warn {{
    border: 1px solid rgba(255, 193, 7, .25);
    background: rgba(255, 193, 7, .06);
  }}

  .hl {{
    padding: 1px 3px;
    border-radius: 6px;
    border: 1px solid transparent;
  }}
  .hl-dims {{
    background: var(--hl-dims-bg);
    border-color: var(--hl-dims-br);
  }}
  .hl-weight {{
    background: var(--hl-weight-bg);
    border-color: var(--hl-weight-br);
  }}
  .hl-qty {{
    background: var(--hl-qty-bg);
    border-color: var(--hl-qty-br);
  }}

  .panelGrid {{
    margin-top: 14px;
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 12px;
    align-items: start;
  }}
  @media(max-width: 1100px) {{
    .panelGrid {{ grid-template-columns: 1fr; }}
  }}
  .panelTitle {{
    font-size: 14px;
    margin: 0 0 8px;
    color: #ddd;
  }}
  .kvRow {{
    display:grid;
    grid-template-columns: 160px 1fr;
    gap: 10px;
    align-items:center;
    margin-bottom: 10px;
  }}
  .kvRow .small {{
    margin-top: 4px;
  }}
  .select {{
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,.03);
    color: var(--text);
    outline: none;
  }}
  .outBox {{
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 12px;
    padding: 10px 12px;
    overflow:auto;
  }}
</style>
</head>
<body>
  <div class="top">
    <div>
      <h1>{_h(title)}</h1>
      <div class="muted">Interactive QA table (search, sort, filter, drill-down, highlighting, rule authoring).</div>
    </div>
    <div class="row">
      <span class="chip" id="statRows">rows: 0</span>
      <span class="chip" id="statLow">low-confidence: 0</span>
      <span class="chip" id="statAvg">avg: 0.000</span>
    </div>
  </div>

  <div class="card controls">
    <div>
      <label>Search (supplier, raw text, notes, rule)</label>
      <input id="q" type="text" placeholder="e.g. carton 24, polybag, ACME..." />
    </div>

    <div>
      <label>Confidence threshold: <span class="mono" id="thrVal">{default_low_threshold:.2f}</span></label>
      <input id="thr" type="range" min="0" max="1" step="0.01" value="{default_low_threshold:.2f}" />
      <div class="small">Rows below this are considered “low confidence”.</div>
    </div>




