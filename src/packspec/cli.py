from __future__ import annotations
import argparse
import json
from pathlib import Path

from .normalize import normalize_packaging
from .rules import load_rulepacks, pick_rulepack
from .report import normalize_csv_pipeline
from .enrich import enrich
from .validate import validate_and_score
from .qa import QAConfig











