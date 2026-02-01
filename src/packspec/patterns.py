from __future__ import annotations
import re

CASE_PACK_RE = re.compile(
    r"\b(?:case\s*pack|casepack|carton\s*qty|carton|master\s*carton|ctn|qty\s*/\s*ctn)\b"
    r"[:\s\-]*([0-9]{1,5})\b",
    re.IGNORECASE,
)


INNER_PACK_RE = re.compile(
    r"\b(?:inner\s*pack|innerpack|inner)\b[:\s\-]*([0-9]{1,5})\b",
    re.IGNORECASE,
)


WEIGHT_RE = re.compile(
    r"\b([0-9]+(?:\.[0-9]+)?)\s*(lb|lbs|pound|pounds|kg|kgs|kilogram|kilograms)\b",
    re.IGNORECASE,
)


DIMS_RE = re.compile(
    r"\b([0-9]+(?:\.[0-9]+)?)\s*([x\*×])\s*([0-9]+(?:\.[0-9]+)?)\s*([x\*×])\s*([0-9]+(?:\.[0-9]+)?)"
    r"\s*(in|inch|inches|\"|cm|centimeter|centimeters)\b",
    re.IGNORECASE,
)

PACKAGING_HINTS = {
    "polybag": re.compile(r"\bpoly\s*bag|polybag\b", re.IGNORECASE),
    "gift_box": re.compile(r"\bgift\s*box|presentation\s*box\b", re.IGNORECASE),
    "bulk": re.compile(r"\bbulk\b", re.IGNORECASE),
    "retail_box": re.compile(r"\bretail\s*box\b", re.IGNORECASE),
    "shrink_wrap": re.compile(r"\bshrink\s*wrap|shrinkwrapped\b", re.IGNORECASE),
    "drawstring_bag": re.compile(r"\bdrawstring\s*bag\b", re.IGNORECASE),
}


