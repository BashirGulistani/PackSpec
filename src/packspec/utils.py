from __future__ import annotations
import re
from typing import Optional


_WS = re.compile(r"\s+")
_NUM = re.compile(r"^[+-]?\d+(\.\d+)?$")


def clean_text(s: str) -> str:
    s = (s or "").strip()
    s = s.replace("×", "x")
    s = _WS.sub(" ", s)
    return s

def safe_int(s: str) -> Optional[int]:
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    s = re.sub(r"[^\d\-+]", "", s)
    if not s:
        return None
    try:
        return int(s)
    except Exception:
        return None

def safe_float(s: str) -> Optional[float]:
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    s = s.replace(",", "")
    s = re.sub(r"[^0-9\.\-+eE]", "", s)
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def clamp01(x: float) -> float:
    if x < 0:
        return 0.0
    if x > 1:
        return 1.0
    return float(x)






