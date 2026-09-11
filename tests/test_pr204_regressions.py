import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.scripts.compute_irr import (
    load_rater2_results,
    make_bootstrap_sample_units,
)
from tools.scripts.e1_pathosformel_batch import collect_pending_records
from tools.scripts.irr_rater2_batch import resolve_sample_image_path
from tools.scripts.irr_sample import adjust_allocation_to_target


class PR204RegressionTests(unittest.TestCase):
    def test_load_rater2_results_skips_dry_run_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results_path = Path(tmpdir) / "rater2_results.jsonl"
            results_path.write_text(
                "\n".join(
                    [
                        '{"item_id":"A","dry_run":true,"coded_by":"dry-run-mock-anthropic-claude-sonnet-4"}',
                        '{"item_id":"B","coded_by":"rater2-anthropic-claude-sonnet-4"}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            loaded = load_rater2_results(results_path)

        self.assertEqual(set(loaded), {"B"})

    def test_make_bootstrap_sample_units_preserves_duplicate_draws(self):
        paired = {
            "ITEM-1": [{"coded_by": "r1", "desincorporacao": 1}, {"coded_by": "r2", "desincorporacao": 1}],
            "ITEM-2": [{"coded_by": "r1", "desincorporacao": 2}, {"coded_by": "r2", "desincorporacao": 2}],
            "ITEM-3": [{"coded_by": "r1", "desincorporacao": 3}, {"coded_by": "r2", "desincorporacao": 3}],
        }

        units = make_bootstrap_sample_units(paired, [0, 0, 2])

        self.assertEqual(
            [unit_id for unit_id, _ in units],
            ["ITEM-1__draw0", "ITEM-1__draw1", "ITEM-3__draw2"],
        )
        self.assertEqual(len(units), 3)

    def test_adjust_allocation_to_target_can_reduce_overshoot(self):
        strata = {
            "fundacional": [{}] * 8,
            "normativo": [{}] * 8,
            "militar": [{}] * 8,
            "contra-alegoria": [{}] * 8,
        }
        allocation = {
            "fundacional": 8,
            "normativo": 8,
            "militar": 8,
            "contra-alegoria": 8,
        }

        adjusted = adjust_allocation_to_target(allocation, strata, target=30)

        self.assertEqual(sum(adjusted.values()), 30)
        self.assertEqual(sorted(adjusted.values()), [7, 7, 8, 8])

    def test_collect_pending_records_excludes_existing_output_ids(self):
        records = [
            {"item_id": "A", "purificacao": {"purificacao_composto": None}},
            {"item_id": "B", "purificacao": {"purificacao_composto": -1}},
            {"item_id": "C", "purificacao": {"purificacao_composto": 1.7}},
        ]

        pending = collect_pending_records(records, {"B"})

        self.assertEqual([record["item_id"] for record in pending], ["A"])

    def test_resolve_sample_image_path_uses_exported_sample_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir) / "repo"
            sample_dir = repo_root / "data" / "processed" / "irr_re_run" / "sample"
            sample_dir.mkdir(parents=True)
            exported = sample_dir / "01_item.jpg"
            exported.write_bytes(b"fake-image")
            sample_path = repo_root / "data" / "processed" / "irr_re_run" / "sample_metadata.jsonl"

            with mock.patch("tools.scripts.irr_rater2_batch.REPO_ROOT", repo_root):
                resolved = resolve_sample_image_path(
                    {
                        "item_id": "ITEM-1",
                        "image_file": "01_item.jpg",
                        "image_path": "data/processed/irr_re_run/sample/01_item.jpg",
                    },
                    sample_path,
                )

        self.assertEqual(resolved, exported)


if __name__ == "__main__":
    unittest.main()
