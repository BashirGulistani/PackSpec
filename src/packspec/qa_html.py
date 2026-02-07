from __future__ import annotations
import json
import html
from pathlib import Path
from typing import Any


def _h(x: Any) -> str:
    return html.escape("" if x is None else str(x))








