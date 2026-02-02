from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, Tuple, List
import re

from .patterns import CASE_PACK_RE, INNER_PACK_RE, WEIGHT_RE, DIMS_RE, PACKAGING_HINTS
from .units import Dim, Weight






