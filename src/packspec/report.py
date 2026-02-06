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



