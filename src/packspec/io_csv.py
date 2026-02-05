from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict, List, Iterable


def read_csv(path: str) -> tuple[list[str], list[dict]]:
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames or []
    return cols, rows



