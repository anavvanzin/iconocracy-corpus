#!/usr/bin/env python3
import time
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INBOX_DIR = REPO_ROOT / "inbox" / "audio"
PROCESSED_DIR = INBOX_DIR / "processed"

def check_for_audio():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    for file_path in INBOX_DIR.glob("*"):
        if file_path.suffix.lower() in (".mp3", ".wav", ".m4a"):
            print(f"Found voice memo: {file_path.name}")
            transcribe(file_path)

def transcribe(file_path):
    output_txt = file_path.with_suffix(".txt")
    
    # Run whisper CLI (or other tools depending on system config)
    cmd = ["whisper", str(file_path), "--output_dir", str(INBOX_DIR), "--model", "base"]
    print(f"Executing: {' '.join(cmd)}")
    try:
        # Run with timeout to prevent locking the daemon
        subprocess.run(cmd, check=True, timeout=120)
        # Move processed audio out of the scanner
        file_path.rename(PROCESSED_DIR / file_path.name)
        print(f"Transcription complete: {output_txt.name}")
    except FileNotFoundError:
        # Fallback if Whisper is not globally installed
        print("Warning: 'whisper' CLI tool not found in PATH. Writing mock transcription...")
        output_txt.write_text(f"Mock transcription for {file_path.name}\n(Whisper CLI was not installed at execution time)", encoding="utf-8")
        file_path.rename(PROCESSED_DIR / file_path.name)
    except subprocess.TimeoutExpired:
        print(f"Error: Transcription timed out for {file_path.name}")
    except Exception as e:
        print(f"Failed to transcribe {file_path.name}: {e}")

if __name__ == "__main__":
    print(f"Watching {INBOX_DIR} for audio input...")
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        check_for_audio()
    else:
        try:
            while True:
                check_for_audio()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nWatcher stopped.")
