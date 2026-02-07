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
  input[type="text"] {{
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,.03);
    color: var(--text);
    outline: none;
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
</style>
</head>
<body>
  <div class="top">
    <div>
      <h1>{_h(title)}</h1>
      <div class="muted">Interactive QA table for parsed packaging specs (search, sort, filter, drill-down).</div>
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

    <div>
      <label>Mode</label>
      <div class="row">
        <button class="btn" id="toggleLow">Show: All</button>
        <button class="btn" id="reset">Reset</button>
      </div>
      <div class="small">Toggle “Only low confidence”.</div>
    </div>

    <div>
      <label>Export</label>
      <div class="row">
        <button class="btn" id="copyJSON">Copy filtered JSON</button>
      </div>
      <div class="small">Copies current filtered rows to clipboard.</div>
    </div>
  </div>




