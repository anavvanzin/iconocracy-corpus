import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tools.scripts.run_iconocracy_eval_openrouter import build_messages, load_jsonl, parse_response, run_prompt


class OpenRouterEvalRunnerTests(unittest.TestCase):
    def test_build_messages_uses_system_and_user_roles(self):
        messages = build_messages("Explique QUAN→QUAL.")
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("endurecimento", messages[0]["content"])
        self.assertEqual(messages[1]["content"], "Explique QUAN→QUAL.")

    def test_load_jsonl_reads_prompt_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "prompts.jsonl"
            path.write_text(
                json.dumps({"id": "p1", "prompt": "A"}, ensure_ascii=False) + "\n"
                + json.dumps({"id": "p2", "prompt": "B"}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            rows = load_jsonl(path)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], "p1")
        self.assertEqual(rows[1]["prompt"], "B")

    def test_parse_response_handles_string_content(self):
        payload = {"choices": [{"message": {"content": "Resposta final"}}]}
        self.assertEqual(parse_response(payload), "Resposta final")

    def test_parse_response_handles_chunked_content(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": [
                            {"type": "text", "text": "Parte 1 "},
                            {"type": "text", "text": "Parte 2"},
                        ]
                    }
                }
            ]
        }
        self.assertEqual(parse_response(payload), "Parte 1 Parte 2")

    @patch("tools.scripts.run_iconocracy_eval_openrouter.requests.post")
    def test_run_prompt_calls_openrouter_and_returns_response(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "model": "openai/gpt-4.1-mini",
            "choices": [{"message": {"content": "Resposta modelo"}}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 8},
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = run_prompt(
            model="openai/gpt-4.1-mini",
            prompt_text="Explique a cadeia de rastreabilidade.",
            api_key="test-key",
            max_tokens=120,
            temperature=0.2,
            top_p=0.95,
            timeout=30,
            site_url="https://example.org",
            site_name="ICONOCRACY Eval",
        )

        self.assertEqual(result["response"], "Resposta modelo")
        self.assertEqual(result["raw_model_id"], "openai/gpt-4.1-mini")
        self.assertEqual(result["usage"]["prompt_tokens"], 12)
        self.assertIn("latency_ms", result)

        call_args, kwargs = mock_post.call_args
        self.assertEqual(call_args[0], "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(kwargs["headers"]["HTTP-Referer"], "https://example.org")
        self.assertEqual(kwargs["headers"]["X-Title"], "ICONOCRACY Eval")
        self.assertEqual(kwargs["json"]["model"], "openai/gpt-4.1-mini")
        self.assertEqual(kwargs["json"]["messages"][1]["content"], "Explique a cadeia de rastreabilidade.")


if __name__ == "__main__":
    unittest.main()
