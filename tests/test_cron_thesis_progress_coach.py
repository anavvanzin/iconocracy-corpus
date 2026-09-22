from pathlib import Path
from tools.scripts.cron_thesis_progress_coach import count_manuscript_words

def test_count_manuscript_words(tmp_path):
    manuscript_dir = tmp_path / "manuscrito"
    manuscript_dir.mkdir()
    (manuscript_dir / "chapter1.md").write_text("This has exactly five words.", encoding="utf-8")
    
    count = count_manuscript_words(manuscript_dir)
    assert count == 5
