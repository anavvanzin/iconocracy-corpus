"""Coherence regression test for Task T2.

Asserts that the two canonical corpus stores stay aligned:

  1. ``data/processed/records.jsonl``   (operational canonical ledger, UUID ids)
  2. ``corpus/corpus-data.json``        (public-facing export, human ids)

This test freezes the "0 divergences" state established at T2 commit time
against future drift. If it fails, run the reconciliation scripts locally:

    python tools/scripts/reconcile_data.py
    python tools/scripts/records_to_corpus.py --diff
    python tools/scripts/records_to_corpus.py --merge   # safe merge

The test shells out to the two CLI scripts rather than importing them, so
it exercises the exact contract any human operator would use.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
RECONCILE = REPO_ROOT / "tools" / "scripts" / "reconcile_data.py"
RECORDS_TO_CORPUS = REPO_ROOT / "tools" / "scripts" / "records_to_corpus.py"
RECORDS_JSONL = REPO_ROOT / "data" / "processed" / "records.jsonl"
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(scope="module")
def reconcile_summary() -> dict:
    """Parsed JSON summary from reconcile_data.py --json."""
    proc = _run([sys.executable, str(RECONCILE), "--json"])
    assert proc.returncode == 0, (
        f"reconcile_data.py exited {proc.returncode}\n"
        f"stdout={proc.stdout!r}\nstderr={proc.stderr!r}"
    )
    data = json.loads(proc.stdout)
    return data


@pytest.fixture(scope="module")
def records_to_corpus_diff() -> str:
    proc = _run([sys.executable, str(RECORDS_TO_CORPUS), "--diff"])
    assert proc.returncode == 0, (
        f"records_to_corpus.py --diff exited {proc.returncode}\n"
        f"stdout={proc.stdout!r}\nstderr={proc.stderr!r}"
    )
    return proc.stdout


# ---- Source-of-truth files must exist ------------------------------------


def test_canonical_files_exist():
    assert RECORDS_JSONL.exists(), f"missing canonical ledger: {RECORDS_JSONL}"
    assert CORPUS_JSON.exists(), f"missing public export: {CORPUS_JSON}"


# ---- reconcile_data.py assertions ----------------------------------------


def test_reconcile_counts_match(reconcile_summary):
    s = reconcile_summary["summary"]
    assert s["corpus_total"] == s["records_total"], (
        f"store sizes diverged: corpus={s['corpus_total']} "
        f"records={s['records_total']}"
    )


def test_reconcile_no_orphans(reconcile_summary):
    s = reconcile_summary["summary"]
    assert s["orphans_corpus"] == 0, (
        f"{s['orphans_corpus']} corpus items without a records.jsonl match: "
        f"{reconcile_summary.get('orphans_corpus', [])[:5]}"
    )
    assert s["orphans_records"] == 0, (
        f"{s['orphans_records']} records without a corpus-data.json match: "
        f"{reconcile_summary.get('orphans_records', [])[:5]}"
    )


def test_reconcile_all_items_matched(reconcile_summary):
    s = reconcile_summary["summary"]
    assert s["matched"] == s["corpus_total"] == s["records_total"]


def test_reconcile_no_field_divergences(reconcile_summary):
    s = reconcile_summary["summary"]
    assert s["divergent_pairs"] == 0, (
        f"{s['divergent_pairs']} matched pairs with field-level divergences: "
        f"first few = {reconcile_summary.get('divergences', [])[:3]}"
    )


# ---- records_to_corpus.py --diff assertions ------------------------------


def test_records_to_corpus_diff_reports_sync(records_to_corpus_diff):
    """`records_to_corpus.py --diff` prints 'Em sincronização' when aligned."""
    assert "Em sincronização" in records_to_corpus_diff, (
        "records_to_corpus.py --diff did not report sync:\n"
        + records_to_corpus_diff
    )
    assert "Only in records.jsonl" not in records_to_corpus_diff
    assert "Only in corpus-data.json" not in records_to_corpus_diff
