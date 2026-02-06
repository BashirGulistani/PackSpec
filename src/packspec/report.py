from __future__ import annotations
from pathlib import Path

from .io_csv import read_csv, write_csv
from .normalize import normalize_packaging
from .rules import load_rulepacks, pick_rulepack
from .enrich import enrich
from .validate import validate_and_score
from .qa import build_review_queue, QAConfig





def normalize_csv_pipeline(
    input_csv: str,
    *,
    text_col: str,
    supplier_col: str | None = None,
    rules_path: str | None = None,
    out_csv: str,
    out_dir: str = ".packspec-out",
    qa_cfg: QAConfig | None = None,
) -> dict:
    cols, rows = read_csv(input_csv)
    rulepacks = load_rulepacks(rules_path) if rules_path else []

    out_rows = []
    for row in rows:
        raw = row.get(text_col, "") or ""
        supplier = (row.get(supplier_col) if supplier_col else None) or None
        rp = pick_rulepack(rulepacks, supplier)

        r = normalize_packaging(raw, supplier=supplier, rulepack=rp)
        r = enrich(r)
        r = validate_and_score(r)
        d = r.to_dict()

        merged = dict(row)
        merged["case_pack_qty"] = d.get("case_pack_qty")
        merged["inner_pack_qty"] = d.get("inner_pack_qty")

        dims = d.get("case_dims") or {}
        merged["case_dim_l"] = dims.get("l")
        merged["case_dim_w"] = dims.get("w")
        merged["case_dim_h"] = dims.get("h")
        merged["case_dim_unit"] = dims.get("unit")

        w = d.get("case_weight") or {}
        merged["case_weight_value"] = w.get("value")
        merged["case_weight_unit"] = w.get("unit")

        merged["packaging_type"] = d.get("packaging_type")
        merged["confidence"] = d.get("confidence")
        merged["notes"] = ";".join(d.get("notes", []))
        merged["rule_applied"] = d.get("rule_applied")

        merged["case_volume_cuin"] = d.get("case_volume_cuin")
        merged["case_volume_cc"] = d.get("case_volume_cc")
        merged["dim_weight_lb"] = d.get("dim_weight_lb")
        merged["dim_weight_kg"] = d.get("dim_weight_kg")

        out_rows.append(merged)



