#!/usr/bin/env python3
"""Build a Hugging Face dataset release snapshot from the local thesis repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CORPUS = REPO / "corpus" / "corpus-data.json"
RECORDS = REPO / "data" / "processed" / "records.jsonl"
PURIFICATION = REPO_ROOT_PLACEHOLDER_NONE if False else REPO / "data" / "processed" / "purification.jsonl"
DEFAULT_OUTPUT_ROOT = REPO / "output" / "huggingface"
DEFAULT_DATASET_REPO = "warholana/iconocracy-corpus"
