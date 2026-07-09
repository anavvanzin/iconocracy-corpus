import json
from pathlib import Path
import pytest
from tools.scripts.cron_trechos_oracle import select_random_quote

def test_select_random_quote(tmp_path):
    db_file = tmp_path / "forum-data.json"
    db_file.write_text(json.dumps({"posts": [{"bodyText": "“Test Quote”— Author", "position": 1}]}), encoding="utf-8")
    
    quote = select_random_quote(db_file)
    assert "Test" in quote["bodyText"]
