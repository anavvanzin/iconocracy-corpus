import json
import tempfile
import unittest
from pathlib import Path

from tools.scripts.compare_iconocracy_eval_runs import collect_rows, render_markdown


class CompareIconocracyEvalRunsTests(unittest.TestCase):
    def test_collect_rows_groups_runs_by_prompt_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path_a = Path(tmpdir) / "a.jsonl"
            path_b = Path(tmpdir) / "b.jsonl"
            path_a.write_text(
                json.dumps({
                    "id": "guardrails-1",
                    "category": "guardrails",
                    "prompt": "Pergunta A",
                    "expectations": ["Não traduzir endurecimento"],
                    "model": "model-a",
                    "adapter": None,
                    "response": "Resposta A",
                }, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
            path_b.write_text(
                json.dumps({
                    "id": "guardrails-1",
                    "category": "guardrails",
                    "prompt": "Pergunta A",
                    "expectations": ["Não traduzir endurecimento"],
                    "model": "model-b",
                    "adapter": "/tmp/adapter",
                    "response": "Resposta B",
                    "provider": "openrouter",
                }, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
            grouped = collect_rows([path_a, path_b])

        self.assertIn("guardrails-1", grouped)
        self.assertEqual(grouped["guardrails-1"]["category"], "guardrails")
        self.assertEqual(len(grouped["guardrails-1"]["runs"]), 2)

    def test_render_markdown_includes_prompt_and_models(self):
        grouped = {
            "guardrails-1": {
                "prompt": "Pergunta A",
                "category": "guardrails",
                "expectations": ["Não traduzir endurecimento"],
                "runs": [
                    {
                        "model": "model-a",
                        "adapter": None,
                        "provider": None,
                        "response": "Resposta A",
                        "source_file": "a.jsonl",
                    },
                    {
                        "model": "openrouter:model-b",
                        "adapter": "/tmp/adapter",
                        "provider": "openrouter",
                        "response": "Resposta B",
                        "source_file": "b.jsonl",
                    },
                ],
            }
        }

        markdown = render_markdown(grouped)

        self.assertIn("# ICONOCRACY eval run comparison", markdown)
        self.assertIn("## guardrails-1", markdown)
        self.assertIn("Pergunta A", markdown)
        self.assertIn("#### model-a", markdown)
        self.assertIn("#### openrouter:model-b + adapter=/tmp/adapter", markdown)
        self.assertIn("Não traduzir endurecimento", markdown)
        self.assertIn("Resposta B", markdown)


if __name__ == "__main__":
    unittest.main()
