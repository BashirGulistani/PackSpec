from __future__ import annotations
import argparse
import json
from pathlib import Path

from .normalize import normalize_packaging
from .rules import load_rulepacks, pick_rulepack
from .report import normalize_csv_pipeline
from .enrich import enrich
from .validate import validate_and_score
from .qa import QAConfig







def main() -> None:
    ap = argparse.ArgumentParser(
        prog="packspec",
        description="Normalize messy packaging specs into structured case pack / dims / weight (+ rules, QA queue).",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_one = sub.add_parser("one", help="Normalize a single packaging spec string")
    p_one.add_argument("text", help="Raw packaging spec text")
    p_one.add_argument("--supplier", default=None, help="Supplier name (optional)")
    p_one.add_argument("--rules", default=None, help="Path to rulepacks.yml/json (optional)")


    p_csv = sub.add_parser("csv", help="Normalize a CSV column containing packaging text (pipeline mode)")
    p_csv.add_argument("--in", dest="inp", required=True, help="Input CSV")
    p_csv.add_argument("--col", required=True, help="Column name containing packaging text")
    p_csv.add_argument("--supplier-col", default=None, help="Column name containing supplier (optional)")
    p_csv.add_argument("--rules", default=None, help="Path to rulepacks.yml/json (optional)")
    p_csv.add_argument("--out", dest="out_csv", required=True, help="Output CSV")
    p_csv.add_argument("--out-dir", default=".packspec-out", help="Output dir for QA outputs")
    p_csv.add_argument("--low-conf", type=float, default=0.45, help="Low confidence threshold (default 0.45)")
    p_csv.add_argument("--sample", type=int, default=50, help="Sample size for QA (default 50)")

    p_rules = sub.add_parser("rules", help="List loaded rulepacks")
    p_rules.add_argument("--rules", required=True, help="Path to rulepacks.yml/json")

    args = ap.parse_args()

    if args.cmd == "rules":
        packs = load_rulepacks(args.rules)
        print(json.dumps([{"name": p.name, "supplier": p.supplier} for p in packs], indent=2))
        return


    if args.cmd == "one":
        packs = load_rulepacks(args.rules) if args.rules else []
        rp = pick_rulepack(packs, args.supplier)

        r = normalize_packaging(args.text, supplier=args.supplier, rulepack=rp)
        r = enrich(r)
        r = validate_and_score(r)
        print(json.dumps(r.to_dict(), indent=2))
        return







