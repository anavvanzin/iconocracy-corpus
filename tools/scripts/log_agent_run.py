#!/usr/bin/env python3
"""Log an agent run to corpus/agent-runs.json.

Usage:
    python tools/scripts/log_agent_run.py --agent validate --status success --items 145 --duration 12 --details "Schema OK"
    python tools/scripts/log_agent_run.py --agent scout --status error --items 0 --duration 45 --details "Gallica API timeout"
"""
import argparse
import json
import os
from datetime import datetime, timezone

RUNS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'corpus', 'agent-runs.json')
AGENT_CHOICES = ['validate', 'scout', 'iconocode', 'sync', 'lacunas', 'download', 'refresh', 'purification', 'argos']
STATUS_CHOICES = ['success', 'error', 'warning']


def load_runs():
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_runs(runs):
    os.makedirs(os.path.dirname(RUNS_FILE), exist_ok=True)
    with open(RUNS_FILE, 'w', encoding='utf-8') as f:
        json.dump(runs, f, ensure_ascii=False, indent=2)


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
