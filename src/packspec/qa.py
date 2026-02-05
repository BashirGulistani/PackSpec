from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import random



@dataclass(frozen=True)
class QAConfig:
    low_conf_threshold: float = 0.45
    sample_size: int = 50


def build_review_queue(rows: list[dict], *, conf_col: str = "confidence", cfg: QAConfig | None = None) -> dict:
    cfg = cfg or QAConfig()
    low = [r for r in rows if float(r.get(conf_col) or 0) <= cfg.low_conf_threshold]

    sample_pool = rows[:]
    random.shuffle(sample_pool)
    sample = sample_pool[: min(cfg.sample_size, len(sample_pool))]

    return {
        "low_conf_rows": low,
        "sample_rows": sample,
        "low_conf_count": len(low),
        "sample_count": len(sample),
    }
