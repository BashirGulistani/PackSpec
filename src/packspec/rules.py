from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from pathlib import Path
import json
import re

try:
    import yaml
except Exception:
    yaml = None

@dataclass
class RulePack:
    name: str
    supplier: Optional[str] = None
    preprocess: List[dict] = field(default_factory=list)
    case_pack_regex: Optional[str] = None
    inner_pack_regex: Optional[str] = None
    dims_regex: Optional[str] = None
    weight_regex: Optional[str] = None

    packaging_type: Optional[str] = None

    def apply_preprocess(self, text: str) -> str:
        out = text
        for r in self.preprocess:
            pat = r.get("pattern")
            repl = r.get("repl", "")
            if pat:
                out = re.sub(pat, repl, out, flags=re.IGNORECASE)
        return out


def load_rulepacks(path: str) -> list[RulePack]:
    p = Path(path)
    if not p.exists():
        return []

    raw: Any
    if p.suffix.lower() in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("PyYAML not installed. Run: pip install pyyaml")
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    else:
        raw = json.loads(p.read_text(encoding="utf-8"))

    packs = []
    for item in (raw.get("rulepacks") if isinstance(raw, dict) else raw) or []:
        packs.append(
            RulePack(
                name=str(item.get("name", "unnamed")),
                supplier=item.get("supplier"),







