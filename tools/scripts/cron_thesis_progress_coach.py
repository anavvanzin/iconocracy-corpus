import sys
from pathlib import Path
import yaml
from datetime import datetime

def count_manuscript_words(manuscript_path: Path) -> int:
    count = 0
    # Canonical active manuscript patterns
    for md_file in manuscript_path.glob("*.md"):
        filename = md_file.name
        # Exclude original versions, pre-consolidation backups, notes, and readmes
        if "_original" in filename or "v1pre-" in filename or "NOTAS" in filename or filename == "LEIAME.md" or filename == "sumario_iconocracia.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            # Simple word count by split
            words = content.split()
            count += len(words)
        except Exception as e:
            print(f"Warning: Failed to read {filename}: {e}", file=sys.stderr)
    return count

def main():
    manuscript_path = Path("tese/manuscrito")
    cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()

    if not manuscript_path.exists():
        print("Error: tese/manuscrito/ not found.")
        return

    current_words = count_manuscript_words(manuscript_path)

    # Read previous cache state
    baseline_words = 0
    weekly_velocity = 0
    target_weekly = 1000

    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                state = yaml.safe_load(f) or {}
            
            progress_state = state.get("jobs", {}).get("thesis-progress", {})
            baseline_words = progress_state.get("baseline_words", current_words)
            target_weekly = progress_state.get("target_weekly", 1000)
            
            # Compute weekly velocity
            weekly_velocity = current_words - baseline_words
        except Exception as e:
            print(f"Warning: Failed to read cache: {e}", file=sys.stderr)

    # Print supportive milestone message
    print(f"## Thesis Progress Compass 🧭\n")
    print(f"Your thesis manuscript currently stands at **{current_words:,} words**.")
    
    if weekly_velocity > 0:
        print(f"You wrote **{weekly_velocity:,} words** this week! (Weekly Target: {target_weekly:,} words)")
        if weekly_velocity >= target_weekly:
            print(f"\n🎉 **Incredible work, Ana!** You smashed your target of {target_weekly:,} words. Go bake some fresh brownies to celebrate!")
        else:
            print(f"\n🌱 **Steady progress!** Every single word brings you closer to the defense. Keep moving forward.")
    else:
        print(f"\n☕ Keep taking care of yourself! The next writing sprint will perfect the ideas.")

    # Update state cache
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                state = yaml.safe_load(f) or {}
            
            if "jobs" not in state:
                state["jobs"] = {}
            if "thesis-progress" not in state["jobs"]:
                state["jobs"]["thesis-progress"] = {}

            state["jobs"]["thesis-progress"]["last_run"] = datetime.now().isoformat()
            state["jobs"]["thesis-progress"]["current_words"] = current_words
            state["jobs"]["thesis-progress"]["weekly_velocity"] = weekly_velocity
            state["jobs"]["thesis-progress"]["last_status"] = "ok"

            with open(cache_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(state, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Warning: Failed to update cache: {e}")

if __name__ == "__main__":
    main()
