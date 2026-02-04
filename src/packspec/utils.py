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







