#!/usr/bin/env python3
"""env-check — verify ICONOCRACY credential hygiene without exposing secrets.

Checks ~/Research/hub/iconocracy-corpus/.env against macOS Keychain,
then reports presence by name only. No values are printed.

Exit codes:
  0 all ok
  1 missing entries
  2 .env parse error or not found
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENV_FILE = REPO / ".env"
KEYCHAIN_SERVICE = "iconocracy-env"

DEFAULT_KEYS = [
    "OPENROUTER_API_KEY",
    "OPENAI_API_KEY",
    "ZOTERO_API_KEY",
    "HF_TOKEN",
    "GALLICA_TOKEN",
    "GOOGLE_DRIVE_TOKEN",
    "SCOPUS_API_KEY",
]


def parse_env_keys(path: Path) -> list[str]:
    keys: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"env-check: cannot read .env: {exc}", file=sys.stderr)
        return []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k = line.split("=", 1)[0].strip()
        if k:
            keys.append(k)
    return keys


def keychain_has(service: str, name: str) -> bool:
    cmd = [
        "security",
        "find-generic-password",
        "-s",
        service,
        "-a",
        name,
    ]
    proc = subprocess.run(cmd, capture_output=True)
    return proc.returncode == 0


def main() -> int:
    keys = DEFAULT_KEYS
    if ENV_FILE.exists():
        env_keys = parse_env_keys(ENV_FILE)
        if env_keys:
            keys = sorted(set(env_keys) & set(keys)) or keys
    else:
        print("env-check: .env not found; using default keyset.")
    if not keys:
        print("env-check: no keys to check.")
        return 2

    rows = []
    for name in keys:
        env_ok = ENV_FILE.exists() and name in parse_env_keys(ENV_FILE)
        kc_ok = keychain_has(KEYCHAIN_SERVICE, name)
        rows.append((name, env_ok, kc_ok))

    print(f"env-check: {ENV_FILE} + keychain:{KEYCHAIN_SERVICE}")
    print(f"{'KEY':<28} {'ENV':>5} {'KC':>5}  STATUS")
    print("-" * 60)
    bad = []
    for name, env_ok, kc_ok in rows:
        status = "ok" if (env_ok or kc_ok) else "MISSING"
        if status == "MISSING":
            bad.append(name)
        print(f"{name:<28} {'yes' if env_ok else 'no':>5} {'yes' if kc_ok else 'no':>5}  {status}")

    if bad:
        print(f"\nMissing: {' '.join(bad)}")
        for name in bad:
            print(f"  security add-generic-password -s {shlex.quote(KEYCHAIN_SERVICE)} -a {shlex.quote(name)} -w '<VALUE>'")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
