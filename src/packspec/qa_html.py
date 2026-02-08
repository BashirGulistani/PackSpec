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
        <button class="btn" id="exportLowCSV">Export low-conf CSV</button>
      </div>
      <div class="small">CSV is generated in-browser from the current dataset.</div>
    </div>
  </div>

  <table id="tbl">
    <thead>
      <tr>
        <th data-key="confidence">confidence</th>
        <th data-key="supplier">supplier</th>
        <th data-key="case_pack_qty">case pack</th>
        <th data-key="dims">dims</th>
        <th data-key="case_weight">weight</th>
        <th data-key="packaging_type">packaging</th>
        <th data-key="detail">details</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <div class="panelGrid">
    <div class="card">
      <div class="panelTitle">Regex Builder (supplier rule authoring)</div>
      <div class="small">Select a row, tweak regexes, and see what they match in the raw text. Copy rulepack snippet when ready.</div>

      <div style="height:10px"></div>

      <div class="kvRow">
        <div class="small">Selected row</div>
        <select class="select" id="selectedRow"></select>
      </div>

      <div class="kvRow">
        <div class="small">Supplier (for rulepack)</div>
        <input id="rbSupplier" type="text" placeholder="e.g. ACME Supplies" />
      </div>

      <div class="kvRow">
        <div class="small">Rulepack name</div>
        <input id="rbName" type="text" placeholder="e.g. acme-cleanup" />
      </div>

      <div class="kvRow">
        <div class="small">case_pack_regex</div>
        <input id="rxCasePack" type="text" />
      </div>
      <div class="kvRow">
        <div class="small">inner_pack_regex</div>
        <input id="rxInnerPack" type="text" />
      </div>

      <div class="kvRow">
        <div class="small">dims_regex</div>
        <input id="rxDims" type="text" />
      </div>

      <div class="kvRow">
        <div class="small">weight_regex</div>
        <input id="rxWeight" type="text" />
      </div>

      <div class="row" style="margin-top:10px">
        <button class="btn" id="rbTest">Test regexes</button>
        <button class="btn" id="rbCopyYAML">Copy YAML snippet</button>
        <button class="btn" id="rbCopyJSON">Copy JSON snippet</button>
      </div>

      <div style="height:10px"></div>

      <div class="small">Test output</div>
      <div class="outBox" style="margin-top:6px">
        <pre class="mono" id="rbOut" style="margin:0; white-space:pre-wrap;"></pre>
      </div>
    </div>

    <div class="card">
      <div class="panelTitle">Highlighted Raw Text (dims / weight / qty)</div>
      <div class="small">Uses your current regex builder values (not just defaults).</div>
      <div style="height:10px"></div>
      <div class="outBox">
        <div id="liveHighlight" class="mono" style="white-space:pre-wrap;"></div>
      </div>
      <div style="height:10px"></div>
      <div class="small">
        Legend:
        <span class="hl hl-dims">dims</span>
        <span class="hl hl-weight">weight</span>
        <span class="hl hl-qty">qty</span>
      </div>
    </div>
  </div>

<script>
  const DATA = {payload_json};

  const DEFAULT_RX = {{
    casePack: {default_case_pack},
    innerPack: {default_inner_pack},
    dims: {default_dims},
    weight: {default_weight},
  }};

  const elQ = document.getElementById("q");
  const elThr = document.getElementById("thr");
  const elThrVal = document.getElementById("thrVal");
  const elToggleLow = document.getElementById("toggleLow");
  const elReset = document.getElementById("reset");
  const elCopy = document.getElementById("copyJSON");
  const elExportLowCSV = document.getElementById("exportLowCSV");

  const statRows = document.getElementById("statRows");
  const statLow = document.getElementById("statLow");
  const statAvg = document.getElementById("statAvg");

  const tbody = document.querySelector("#tbl tbody");
  const headers = Array.from(document.querySelectorAll("th[data-key]"));

  const elSelectedRow = document.getElementById("selectedRow");
  const elRbSupplier = document.getElementById("rbSupplier");
  const elRbName = document.getElementById("rbName");
  const elRxCasePack = document.getElementById("rxCasePack");
  const elRxInnerPack = document.getElementById("rxInnerPack");
  const elRxDims = document.getElementById("rxDims");
  const elRxWeight = document.getElementById("rxWeight");
  const elRbTest = document.getElementById("rbTest");
  const elRbCopyYAML = document.getElementById("rbCopyYAML");
  const elRbCopyJSON = document.getElementById("rbCopyJSON");
  const elRbOut = document.getElementById("rbOut");
  const elLiveHighlight = document.getElementById("liveHighlight");

  let onlyLow = false;
  let sortKey = "confidence";
  let sortDir = "desc";

  function dimsToString(d) {{
    if (!d) return "";
    const {{l,w,h,u}} = d;
    if (l==null || w==null || h==null) return "";
    return `${{l}}x${{w}}x${{h}} ${{u||""}}`.trim();
  }}

  function weightToString(r) {{
    if (r.case_weight_value == null) return "";
    return `${{r.case_weight_value}} ${{r.case_weight_unit||""}}`.trim();
  }}

  function haystack(r) {{
    return [
      r.supplier || "",
      r.raw || "",
      r.notes || "",
      r.rule_applied || "",
      r.packaging_type || ""
    ].join(" ").toLowerCase();
  }}

  function passes(r, q, thr) {{
    if (onlyLow && !(r.confidence < thr)) return false;
    if (!q) return true;
    return haystack(r).includes(q);
  }}

  function compare(a, b) {{
    const dir = sortDir === "asc" ? 1 : -1;

    const getVal = (r) => {{
      if (sortKey === "dims") return dimsToString(r.dims);
      if (sortKey === "case_weight") return weightToString(r);
      if (sortKey === "detail") return (r.raw || "");
      const v = r[sortKey];
      return v == null ? "" : v;
    }};

    const va = getVal(a);
    const vb = getVal(b);

    if (sortKey === "confidence") {{
      return (va - vb) * dir;
    }}
    return String(va).localeCompare(String(vb)) * dir;
  }}
  function escapeHtml(s) {{
    return (s||"")
      .replace(/&/g,"&amp;")
      .replace(/</g,"&lt;")
      .replace(/>/g,"&gt;")
      .replace(/"/g,"&quot;")
      .replace(/'/g,"&#039;");
  }}

  function parseJsRegex(inputStr) {{
    const s = (inputStr||"").trim();
    if (!s) return null;

    if (s.startsWith("/") && s.lastIndexOf("/") > 0) {{
      const last = s.lastIndexOf("/");
      const pat = s.slice(1, last);
      const flags = s.slice(last+1) || "";
      try {{
        return new RegExp(pat, flags);
      }} catch(e) {{
        return null;
      }}
    }}
    try {{
      return new RegExp(s, "i");
    }} catch(e) {{
      return null;
    }}
  }}

  function collectMatches(text, rx, cls, label) {{
    if (!rx) return [];
    const out = [];

    const flags = rx.flags.includes("g") ? rx.flags : (rx.flags + "g");
    const rg = new RegExp(rx.source, flags);

    let m;
    while ((m = rg.exec(text)) !== null) {{
      if (m.index === undefined) break;
      const start = m.index;
      const end = start + (m[0] ? m[0].length : 0);
      if (end > start) {{
        out.push({{start, end, cls, label, value: m[0]}});
      }}
      if (m[0] === "") rg.lastIndex++;
    }}
    return out;
  }}







