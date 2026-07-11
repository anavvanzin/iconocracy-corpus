#!/usr/bin/env python3
"""
Migrates and registers the 4 core jobs + 2 creative suite jobs
directly into Ana's default Hermes profile's jobs.json.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_JOBS_FILE = Path("/Users/ana/.hermes/cron/jobs.json")

# Core 4 + Creative Suite 2 Job Configurations
NEW_JOBS_SPEC = [
    {
        "name": "corpus-validation",
        "script": "iconocracy_corpus_validation.py",
        "schedule_expr": "0 9 * * 1,4",
        "prompt": "You are Aurelius, Ana's research supervisor agent. Analyze the JSON output of the corpus validation script:\n{stdout}\n\nFollow these strict decision tree rules in order:\n1. IF the status is \"error\": Create a highly visible ALERT notification. List the specific validation failures or execution exceptions, and explain which records are invalid or what crashed.\n2. IF the status is \"ok\" AND changed is true: Output a concise, friendly report summarizing that records.jsonl has been successfully validated. Highlight the new total item count.\n3. IF the status is \"ok\" AND changed is false: Output exactly \"[SILENT]\" and nothing else. No preamble, no explanation.\n\nThis is a cost-aware cron job — respect these rules to prevent alert fatigue."
    },
    {
        "name": "thesis-progress",
        "script": "iconocracy_thesis_progress.py",
        "schedule_expr": "0 20 * * 0",
        "prompt": "You are Aurelius, Ana's supportive writing coach. Analyze the JSON output of the thesis progress script:\n{stdout}\n\nThis job runs weekly on Sunday evening to provide a gentle thesis compass update.\nFollow these rules to construct your response:\n1. IF the status is \"error\": Alert Ana to the error and the path issue.\n2. IF the status is \"ok\":\n   Draft a warm, narrative-style milestone message. Celebrating her writing velocity!\n   - Highlight the total word count and her progress (weekly_velocity) compared to her target_weekly.\n   - Use supportive, scholarly tone. Refrain from boring cold tables; weave the stats into encouraging, fluent paragraphs.\n   - Suggest she bake some brownies or listen to some lo-fi/pluggnb music to reward herself.\n   - Keep the briefing in English (as per profile preference)."
    },
    {
        "name": "sync-safeguard",
        "script": "iconocracy_sync_safeguard.py",
        "schedule_expr": "0 8 * * *",
        "prompt": "You are Aurelius, Ana's local infrastructure supervisor. Analyze the JSON output of the sync safeguard check:\n{stdout}\n\nThis job runs daily at 08:00 to keep her workspace clean and safe.\nFollow these strict decision tree rules in order:\n1. IF the status is \"error\": Alert her about the execution error with details.\n2. IF there are active warnings (e.g., uncommitted changes exist, or last commit is > 24 hours ago, or backup drive is not mounted):\n   Draft a gentle, friendly, and precise reminder. Mention the current active branch she is working on and list the top modified files. Remind her to commit her progress and mount her backup SSD (/Volumes/ICONOCRACIA) if appropriate.\n3. IF there are no warnings AND the workspace is fully clean:\n   Output exactly \"[SILENT]\" and nothing else. No preamble, no confirmation. We stay quiet to respect her attention."
    },
    {
        "name": "iconocode-backfill",
        "script": "iconocracy_iconocode_backfill.py",
        "schedule_expr": "0 2 * * 5",
        "prompt": "You are Aurelius, Ana's iconographic research scout. Analyze the JSON output of the iconocode backfill check:\n{stdout}\n\nThis job runs weekly on Friday early morning to identify candidates needing integration.\nFollow these strict decision tree rules in order:\n1. IF the status is \"error\": Report the execution error.\n2. IF there are unmapped candidates (total_unmapped_count > 0):\n   Create a neat, encouraging summary of how many new candidates have been gathered in the `vault/candidatos/` folder but are not yet catalogued in the main ledger (total_unmapped_count).\n   List the first few candidate files (unmapped_candidates) as high-signal integration opportunities for her next research session.\n3. IF there are zero unmapped candidates:\n   Output exactly \"[SILENT]\" and nothing else. No comments, no congratulations."
    },
    {
        "name": "trechos-oracle",
        "script": "iconocracy_trechos_oracle.py",
        "schedule_expr": "0 9 * * 2,4",
        "prompt": "You are Aurelius, Ana's reflective supervisor. Analyze the JSON output of the Trechos Oracle:\n{stdout}\n\nFollow these strict decision tree rules in order:\n1. IF the status is \"error\": Report the execution error.\n2. IF the status is \"ok\":\n   Draft a beautiful, mindful, and highly editorial report.\n   - Present her curated literary quote and its author prominently in styled markdown.\n   - Add a short, personalized, and deep philosophical prompt (\"Aurelius Nudge\") that helps her reflect on her writing sprint, academic alignment, or personal gratitude. Keep the tone warm, intellectual, and quiet. No corporate cheerfulness.\n   - Keep the notification brief (1-2 small paragraphs). Deliver in English (profile preference)."
    },
    {
        "name": "zwischenraum-generator",
        "script": "iconocracy_zwischenraum_generator.py",
        "schedule_expr": "0 8 * * 3",
        "prompt": "You are Aurelius, Ana's Warburgian research companion. Analyze the JSON output of the Zwischenraum Associative Engine:\n{stdout}\n\nFollow these strict decision tree rules in order:\n1. IF the status is \"error\": Report the execution error.\n2. IF the status is \"ok\":\n   Draft a neat, deeply intellectual and imaginative Warburgian reflection prompt (an associative \"Zwischenraum\").\n   - Present the selected corpus item and the selected literary quote.\n   - Synthesize a creative tension or visual friction between them. How does the literal imagery or historical weight of the legal iconography interact with the existential/philosophical depth of the quote?\n   - Challenge her to draft a brief 1-paragraph associative note in her Zettelkasten or reflect on this friction during her day.\n   - Keep the tone highly academic, artistic, and evocative."
    }
]

def generate_job_id(name: str) -> str:
    """Generate a deterministic 12-char hex id based on job name."""
    import hashlib
    return hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]

def main():
    if not DEFAULT_JOBS_FILE.exists():
        print(f"Error: Default profile's jobs.json not found at {DEFAULT_JOBS_FILE}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(DEFAULT_JOBS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading jobs.json: {e}", file=sys.stderr)
        sys.exit(1)

    existing_jobs = data.setdefault("jobs", [])
    
    # Track existing names to replace or add
    existing_by_name = {job["name"]: idx for idx, job in enumerate(existing_jobs)}
    
    added_count = 0
    updated_count = 0

    for spec in NEW_JOBS_SPEC:
        name = spec["name"]
        job_id = generate_job_id(name)
        
        job_data = {
            "id": job_id,
            "name": name,
            "prompt": spec["prompt"],
            "skills": [],
            "skill": None,
            "model": None,
            "provider": None,
            "provider_snapshot": "gemini",
            "model_snapshot": "gemini-3.5-flash",
            "base_url": None,
            "script": spec["script"],
            "no_agent": False,
            "context_from": None,
            "schedule": {
                "kind": "cron",
                "expr": spec["schedule_expr"],
                "display": spec["schedule_expr"]
            },
            "schedule_display": spec["schedule_expr"],
            "repeat": {
                "times": None,
                "completed": 0
            },
            "enabled": True,
            "state": "scheduled",
            "paused_at": None,
            "paused_reason": None,
            "created_at": datetime.now().isoformat() + "-03:00",
            "next_run_at": datetime.now().isoformat() + "-03:00",  # scheduler recalculates this
            "last_run_at": None,
            "last_status": None,
            "last_error": None,
            "last_delivery_error": None,
            "deliver": "all",
            "origin": None,
            "enabled_toolsets": None,
            "workdir": None
        }

        # Python json.dumps serializes None as null, which is correct
        if name in existing_by_name:
            # Update existing job definition preserving execution state
            idx = existing_by_name[name]
            existing_job = existing_jobs[idx]
            
            # Preserve state and historical counters
            job_data["id"] = existing_job.get("id", job_id)
            job_data["created_at"] = existing_job.get("created_at", job_data["created_at"])
            job_data["repeat"]["completed"] = existing_job.get("repeat", {}).get("completed", 0)
            job_data["last_run_at"] = existing_job.get("last_run_at")
            job_data["last_status"] = existing_job.get("last_status")
            job_data["last_error"] = existing_job.get("last_error")
            job_data["last_delivery_error"] = existing_job.get("last_delivery_error")
            
            existing_jobs[idx] = job_data
            updated_count += 1
        else:
            # Append as new
            existing_jobs.append(job_data)
            added_count += 1

    # Save atomically
    temp_file = DEFAULT_JOBS_FILE.with_suffix(".tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        temp_file.replace(DEFAULT_JOBS_FILE)
        print(f"Successfully updated default jobs.json: {added_count} added, {updated_count} updated.")
    except Exception as e:
        print(f"Error saving jobs.json: {e}", file=sys.stderr)
        if temp_file.exists():
            temp_file.unlink()
        sys.exit(1)

if __name__ == "__main__":
    main()
