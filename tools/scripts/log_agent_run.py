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

def load_runs():
    if os.path.exists(RUNS_FILE):
        with open(RUNS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_runs(runs):
    os.makedirs(os.path.dirname(RUNS_FILE), exist_ok=True)
    with open(RUNS_FILE, 'w', encoding='utf-8') as f:
        json.dump(runs, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Log an agent run')
    parser.add_argument('--agent', required=True, choices=['validate', 'scout', 'iconocode', 'sync', 'lacunas', 'download', 'refresh', 'purification'])
    parser.add_argument('--status', required=True, choices=['success', 'error', 'warning'])
    parser.add_argument('--items', type=int, default=0, help='Number of items affected')
    parser.add_argument('--duration', type=int, default=0, help='Duration in seconds')
    parser.add_argument('--details', type=str, default='', help='Run details')
    args = parser.parse_args()

    runs = load_runs()
    entry = {
        'timestamp': datetime.now(timezone.utc).isoformat()[:19] + 'Z',
        'agent': args.agent,
        'status': args.status,
        'items_affected': args.items,
        'duration_s': args.duration,
        'details': args.details
    }
    runs.insert(0, entry)

    # Keep last 500 runs max
    runs = runs[:500]
    save_runs(runs)
    print(f"Logged: {args.agent} [{args.status}] — {args.details}")
    return {'status': 'success', 'summary': f'Logged {args.agent} run', 'next_actions': [], 'artifacts': [RUNS_FILE]}

if __name__ == '__main__':
    main()
