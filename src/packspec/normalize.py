from __future__ import annotations
from typing import Optional, List
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE, PACKAGING_HINTS
from .units import Dim, Weight
from .types import PackSpecResult
from .utils import clean_text, safe_int, safe_float, clamp01
from .rules import RulePack



