from __future__ import annotations
from pathlib import Path

from .io_csv import read_csv, write_csv
from .normalize import normalize_packaging
from .rules import load_rulepacks, pick_rulepack
from .enrich import enrich
from .validate import validate_and_score
from .qa import build_review_queue, QAConfig
from .qa_html import write_interactive_qa_html





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

    extra = [
        "case_pack_qty","inner_pack_qty",
        "case_dim_l","case_dim_w","case_dim_h","case_dim_unit",
        "case_weight_value","case_weight_unit",
        "packaging_type","confidence","notes","rule_applied",
        "case_volume_cuin","case_volume_cc","dim_weight_lb","dim_weight_kg",
    ]
    fieldnames = cols[:]
    for c in extra:
        if c not in fieldnames:
            fieldnames.append(c)

    write_csv(out_csv, fieldnames, out_rows)

    qa = build_review_queue(out_rows, cfg=qa_cfg or QAConfig())
    outd = Path(out_dir)
    outd.mkdir(parents=True, exist_ok=True)

    review_path = str(outd / "review_queue.csv")
    sample_path = str(outd / "sample.csv")
    write_csv(review_path, fieldnames, qa["low_conf_rows"])
    write_csv(sample_path, fieldnames, qa["sample_rows"])

    confs = [float(r.get("confidence") or 0) for r in out_rows]
    avg = sum(confs) / len(confs) if confs else 0.0
    high = sum(1 for c in confs if c >= 0.7)
    low = sum(1 for c in confs if c <= (qa_cfg.low_conf_threshold if qa_cfg else 0.45))


    qa_html_path = str(outd / "qa_report.html")
    write_interactive_qa_html(
        qa_html_path,
        rows=out_rows,
        text_col=text_col,
        supplier_col=supplier_col,
        title="PackSpec QA Report",
        default_low_threshold=(qa_cfg.low_conf_threshold if qa_cfg else 0.45),
        max_rows=5000,
    )


    return {
        "rows": len(out_rows),
        "avg_confidence": round(avg, 3),
        "high_confidence": high,
        "low_confidence": low,
        "review_queue_count": qa["low_conf_count"],
        "sample_count": qa["sample_count"],
        "out_csv": out_csv,
        "review_queue_csv": review_path,
        "sample_csv": sample_path,
        "qa_report_html": qa_html_path,

    }

