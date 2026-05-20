#!/usr/bin/env python3
"""Log an agent run to corpus/agent-runs.json.

Usage:
    python tools/scripts/log_agent_run.py --agent validate --status success --items 145 --duration 12 --details "Schema OK"
    python tools/scripts/log_agent_run.py --agent scout --status error --items 0 --duration 45 --details "Gallica API timeout"
"""
import argparse
import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone

RUNS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'corpus', 'agent-runs.json')
AGENT_CHOICES = ['validate', 'scout', 'iconocode', 'sync', 'lacunas', 'download', 'refresh', 'purification', 'argos']
STATUS_CHOICES = ['success', 'error', 'warning']


def load_runs():
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _lock_path() -> str:
    return os.path.join(os.path.dirname(RUNS_FILE), 'agent-runs.lock')


def _write_atomic(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    fd, tmp_path = tempfile.mkstemp(prefix='agent-runs-', suffix='.tmp', dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(serialized)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def save_runs(runs):
    _write_atomic(RUNS_FILE, runs)


def build_entry(*, agent, status, items=0, duration=0, details=''):
    return {
        'timestamp': datetime.now(timezone.utc).isoformat()[:19] + 'Z',
        'agent': agent,
        'status': status,
        'items_affected': items,
        'duration_s': duration,
        'details': details,
    }


def log_run(*, agent, status, items=0, duration=0, details=''):
    os.makedirs(os.path.dirname(_lock_path()), exist_ok=True)
    with open(_lock_path(), 'a+', encoding='utf-8') as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        runs = load_runs()
        entry = build_entry(agent=agent, status=status, items=items, duration=duration, details=details)
        runs.insert(0, entry)
        runs = runs[:500]
        save_runs(runs)
    return entry


def main():
    parser = argparse.ArgumentParser(description='Log an agent run')
    parser.add_argument('--agent', required=True, choices=AGENT_CHOICES)
    parser.add_argument('--status', required=True, choices=STATUS_CHOICES)
    parser.add_argument('--items', type=int, default=0, help='Number of items affected')
    parser.add_argument('--duration', type=int, default=0, help='Duration in seconds')
    parser.add_argument('--details', type=str, default='', help='Run details')
    args = parser.parse_args()

    log_run(agent=args.agent, status=args.status, items=args.items, duration=args.duration, details=args.details)
    print(f"Logged: {args.agent} [{args.status}] — {args.details}")
    return {'status': 'success', 'summary': f'Logged {args.agent} run', 'next_actions': [], 'artifacts': [RUNS_FILE]}


if __name__ == '__main__':
    main()
