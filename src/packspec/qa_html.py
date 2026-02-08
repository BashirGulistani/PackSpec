from __future__ import annotations
import json
import html
from pathlib import Path
from typing import Any, Optional
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE


def _h(x: Any) -> str:
    return html.escape("" if x is None else str(x))




def _pyre_to_js_literal(rx: re.Pattern) -> str:
    """
    Convert a Python compiled regex to a "best effort" JS regex literal string.
    We keep it simple: pattern + 'i' flag if IGNORECASE. JS does not support all
    Python features, but our patterns are simple enough.
    """
    pat = rx.pattern.replace("\\", "\\\\").replace("/", "\\/")
    flags = "i" if (rx.flags & re.IGNORECASE) else ""
    return f"/{pat}/{flags}"







