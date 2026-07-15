from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.scripts import build_hf_release


class BuildHfReleaseTests(unittest.TestCase):
    def test_compute_stats_uses_fallback_support_fields_and_calculates_mean(self):
        corpus = [
            {"country": "BR", "regime": "fundacional", "support": "coin", "endurecimento_score": 2.0},
            {"country": "BR", "regime": "fundacional", "medium_norm": "stamp", "endurecimento_score": 1.0},
            {"country": "FR", "regime": "normativo", "medium": "poster", "endurecimento_score": "not-a-number"},
        ]
        records = [
            {"master_record_version": "1.0"},
            {"master_record_version": "1.1"},
        ]
        purification = [{"id": "BR-001"}, {"id": "BR-001"}, {"id": "FR-001"}]

        stats = build_hf_release.compute_stats(corpus, records, purification)

        self.assertEqual(stats["corpus_items"], 3)
        self.assertEqual(stats["records_items"], 2)
        self.assertEqual(stats["purification_rows"], 3)
        self.assertEqual(stats["coded_items"], 2)
        self.assertEqual(stats["schema_versions"], ["1.0", "1.1"])
        self.assertEqual(stats["top_supports"]["coin"], 1)
        self.assertEqual(stats["top_supports"]["stamp"], 1)
        self.assertEqual(stats["top_supports"]["poster"], 1)
        self.assertEqual(stats["mean_endurecimento"], 1.5)
        self.assertEqual(stats["corpus_records_delta"], 1)

    def test_ensure_hf_auth_fails_when_hf_cli_missing(self):
        with mock.patch("tools.scripts.build_hf_release.shutil.which", return_value=None):
            with self.assertRaisesRegex(SystemExit, "hf CLI not found on PATH"):
                build_hf_release.ensure_hf_auth()

    def test_ensure_hf_auth_fails_when_not_authenticated(self):
        result = mock.Mock(returncode=1)
        with mock.patch("tools.scripts.build_hf_release.shutil.which", return_value="/usr/bin/hf"), mock.patch(
            "tools.scripts.build_hf_release.subprocess.run", return_value=result
        ):
            with self.assertRaisesRegex(SystemExit, "hf CLI is not authenticated"):
                build_hf_release.ensure_hf_auth()

    def test_validate_local_contract_rejects_corpus_records_drift(self):
        with mock.patch("tools.scripts.build_hf_release.subprocess.run") as run_mock, mock.patch(
            "tools.scripts.build_hf_release.load_json", return_value=[{"id": "1"}, {"id": "2"}]
        ), mock.patch(
            "tools.scripts.build_hf_release.load_jsonl",
            side_effect=[[{"item_id": "only-one"}], [{"id": "P-001"}]],
        ):
            with self.assertRaisesRegex(SystemExit, "drift detected"):
                build_hf_release.validate_local_contract()

        self.assertEqual(run_mock.call_count, 2)
        first_args, first_kwargs = run_mock.call_args_list[0]
        second_args, second_kwargs = run_mock.call_args_list[1]
        self.assertIn("validate_schemas.py", str(first_args[0][1]))
        self.assertIn("validate_schemas.py", str(second_args[0][1]))
        self.assertTrue(first_kwargs["check"])
        self.assertTrue(second_kwargs["check"])

    def test_write_sha256sums_writes_all_expected_entries(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            snapshot = Path(tmp_dir)
            file_payloads = {
                "corpus-data.json": b"corpus",
                "records.jsonl": b"records",
                "purification.jsonl": b"purif",
                "release.json": b"release",
                "CHANGELOG.md": b"changelog",
                "README.md": b"readme",
            }
            for name, payload in file_payloads.items():
                (snapshot / name).write_bytes(payload)

            build_hf_release.write_sha256sums(snapshot)

            sums = (snapshot / "SHA256SUMS.txt").read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(sums), 6)
            expected_line = f"{hashlib.sha256(b'corpus').hexdigest()}  corpus-data.json"
            self.assertIn(expected_line, sums)


if __name__ == "__main__":
    unittest.main()
