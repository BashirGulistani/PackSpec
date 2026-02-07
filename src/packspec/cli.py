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









