from __future__ import annotations
import csv
import html
import json
from pathlib import Path
from typing import Any, Dict, List

from .normalize import normalize_packaging


def write_json(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")





def normalize_csv(input_csv: str, text_col: str, out_csv: str) -> dict:
    rows_out: List[dict] = []
    with open(input_csv, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row.get(text_col, "") or ""
            norm = normalize_packaging(raw).to_dict()
            merged = dict(row)
            merged["case_pack_qty"] = norm.get("case_pack_qty")
            merged["inner_pack_qty"] = norm.get("inner_pack_qty")
            dims = norm.get("case_dims") or {}
            merged["case_dim_l"] = dims.get("l")
            merged["case_dim_w"] = dims.get("w")
            merged["case_dim_h"] = dims.get("h")
            merged["case_dim_unit"] = dims.get("unit")
            w = norm.get("case_weight") or {}
            merged["case_weight_value"] = w.get("value")
            merged["case_weight_unit"] = w.get("unit")
            merged["packaging_type"] = norm.get("packaging_type")
            merged["confidence"] = norm.get("confidence")
            merged["notes"] = ";".join(norm.get("notes", []))
            rows_out.append(merged)

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows_out[0].keys()) if rows_out else []
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows_out:
            writer.writerow(r)

    confs = [float(r.get("confidence") or 0) for r in rows_out]
    avg = sum(confs) / len(confs) if confs else 0.0
    high = sum(1 for c in confs if c >= 0.7)
    low = sum(1 for c in confs if c <= 0.3)

    return {"rows": len(rows_out), "avg_confidence": round(avg, 3), "high_confidence": high, "low_confidence": low}





def write_html_report(path: str, summary: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    def h(x: Any) -> str:
        return html.escape("" if x is None else str(x))

    html_text = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>PackSpec Report</title>

<style>
  body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;margin:24px;background:#0b0b0b;color:#eee}}
  .card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:14px;margin:12px 0}}
  h1{{margin:0 0 6px;font-size:22px}}
  .muted{{color:#b9b9b9;font-size:13px}}
  .grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}}
  @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
  .pill{{display:inline-block;padding:4px 8px;border-radius:999px;border:1px solid rgba(255,255,255,.16);font-size:12px;color:#ddd}}
</style>
</head>
<body>
<h1>PackSpec</h1>
<div class="muted">Packaging normalization run summary</div>

<div class="card">
  <div class="grid">
    <div><span class="pill">rows</span><div>{h(summary.get("rows"))}</div></div>
    <div><span class="pill">avg confidence</span><div>{h(summary.get("avg_confidence"))}</div></div>
    <div><span class="pill">high confidence</span><div>{h(summary.get("high_confidence"))}</div></div>
    <div><span class="pill">low confidence</span><div>{h(summary.get("low_confidence"))}</div></div>
  </div>
</div>

</body></html>
"""
    p.write_text(html_text, encoding="utf-8")






