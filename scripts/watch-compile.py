from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = REPO / "vault/tese/manuscrito"
INTERVAL_SECONDS = 4


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_make(target: str = "docx") -> None:
    cmd = ["make", "-C", str(REPO / "vault/tese"), target]
    print(f"[watch-compile] make target={target} -> {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[watch-compile] make {target} failed:\n{proc.stdout}{proc.stderr}")
    else:
        out = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip().splitlines() else "ok"
        print(f"[watch-compile] make {target} done: {out}")


def discover_md_files(root: Path) -> list[Path]:
    if not root.exists():
        raise SystemExit(f"target not found: {root}")
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def snapshot(files: list[Path]) -> dict[str, str]:
    state: dict[str, str] = {}
    for path in files:
        try:
            state[str(path)] = sha256_file(path)
        except FileNotFoundError:
            state[str(path)] = ""
    return state


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TARGET
    print(f"[watch-compile] watching: {target}")
    print("[watch-compile] Ctrl-C to stop")
    files = discover_md_files(target)
    state = snapshot(files)

    while True:
        time.sleep(INTERVAL_SECONDS)
        try:
            new_state = snapshot(files)
        except Exception as exc:
            print(f"[watch-compile] snapshot error: {exc}")
            continue
        if new_state != state:
            state = new_state
            run_make("docx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
