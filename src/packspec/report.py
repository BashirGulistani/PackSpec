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













