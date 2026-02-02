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







