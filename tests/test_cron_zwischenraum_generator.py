import json
from pathlib import Path
from tools.scripts.cron_zwischenraum_generator import pair_quote_with_record

def test_pair_quote_with_record(tmp_path):
    corpus_file = tmp_path / "corpus-data.json"
    corpus_file.write_text(json.dumps([{"id": "FR-013", "title": "Declaration"}]), encoding="utf-8")
    quotes_file = tmp_path / "forum-data.json"
    quotes_file.write_text(json.dumps({"posts": [{"bodyText": "“Silence”", "position": 1}]}), encoding="utf-8")
    
    record, quote = pair_quote_with_record(corpus_file, quotes_file)
    assert record["id"] == "FR-013"
    assert "Silence" in quote["bodyText"]
