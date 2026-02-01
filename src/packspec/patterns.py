from __future__ import annotations
import re

CASE_PACK_RE = re.compile(
    r"\b(?:case\s*pack|casepack|carton\s*qty|carton|master\s*carton|ctn|qty\s*/\s*ctn)\b"
    r"[:\s\-]*([0-9]{1,5})\b",
    re.IGNORECASE,
)





