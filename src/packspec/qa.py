from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import random



@dataclass(frozen=True)
class QAConfig:
    low_conf_threshold: float = 0.45
    sample_size: int = 50


