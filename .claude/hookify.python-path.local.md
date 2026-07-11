---
name: python-path-version-agnostic
enabled: true
event: bash
pattern: 'python3\.\d{1,2}\b'
action: warn
---
Version-pinned Python path detected. Use `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python` (version-agnostic) instead — pin-paths break on version bumps.
