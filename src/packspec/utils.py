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








