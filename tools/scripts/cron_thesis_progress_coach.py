import sys
from pathlib import Path
from datetime import datetime
import yaml

def count_manuscript_words(manuscript_path: Path) -> int:
    count = 0
    if not manuscript_path.exists():
        return 0
    for md_file in manuscript_path.rglob("*.md"):
        if any(part.startswith(".") for part in md_file.parts):
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            count += len(content.split())
        except Exception:
            pass
    return count

def update_cache_and_get_velocity(current_words: int) -> tuple[int, int]:
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            state = yaml.safe_load(f) or {}
    else:
        state = {}
        
    if "jobs" not in state:
        state["jobs"] = {}
        
    progress_state = state["jobs"].get("thesis-progress", {})
    baseline = progress_state.get("current_words", 0)
    
    if baseline == 0:
        baseline = current_words
        
    velocity = current_words - baseline
    
    state["jobs"]["thesis-progress"] = {
        "last_run": datetime.now().isoformat(),
        "baseline_words": baseline,
        "current_words": current_words,
        "weekly_velocity": velocity,
        "target_weekly": progress_state.get("target_weekly", 1000),
        "last_status": "ok"
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)
        
    return baseline, velocity

def main():
    repo_root = Path(__file__).resolve().parent.parent.parent
    manuscript_path = repo_root / "tese" / "manuscrito"
    
    if not manuscript_path.exists():
        print(f"Error: Manuscript directory not found at {manuscript_path}", file=sys.stderr)
        return
        
    current_words = count_manuscript_words(manuscript_path)
    baseline, velocity = update_cache_and_get_velocity(current_words)
    
    print(f"## Thesis Progress Coach\n")
    print(f"**Current word count:** {current_words:,} words (Baseline: {baseline:,})\n")
    
    if velocity > 0:
        print(f"🎉 **Weekly Velocity:** +{velocity:,} words written this week!")
        print(f"You made wonderful progress toward your qualitative milestones. Time to put the glass down, put on some lo-fi or pluggnb, and celebrate—perhaps with a freshly baked batch of brownies! 🍫")
    elif velocity == 0:
        print(f"⚓ **Weekly Velocity:** Stable week at {current_words:,} words.")
        print(f"A stable baseline is the solid foundation of any rigorous investigation. Take this moment to rest and reflect on your conceptual frameworks before the next sprint.")
    else:
        print(f"🧹 **Weekly Velocity:** {velocity:,} words (purification/refactoring session).")
        print(f"You purified your text by removing {abs(velocity):,} words! This is true classical pruning—less is more in legal iconography.")

if __name__ == "__main__":
    main()
