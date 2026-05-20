# Design Spec: Repo Maintainer (Interactive Auditor)

**Date**: 2026-05-20
**Status**: Draft (Approved in Concept)
**Target**: `iconocracy-corpus` Research Repository

## 1. Problem Statement
The `iconocracy-corpus` repository suffers from a "triple-threat" of conflicts:
1.  **Structural Redundancy**: Files are duplicated or split across `Text/`, `docs/`, `vault/`, and `wiki/`.
2.  **Data Inconsistency**: Core research data (like `corpus-data.json`) has drifted from local modifications.
3.  **Git Desync**: The branch is 6 commits ahead of origin with a massive pile of unstaged changes.

## 2. Goals
- Consolidate research files into a canonical structure.
- Resolve data drift between scripts and datasets.
- Align the local git state with the intended repository structure.
- Minimize user effort through an interactive, visual dashboard.

## 3. Architecture

### 3.1 Core Engine (Scanner & Clusterer)
The backend engine (Python-based) will perform the following:
- **Fuzzy Scanner**: Scans for filename collisions and path overlaps.
- **Identity Resolver**: Uses SHA-256 checksums to detect byte-identical duplicates.
- **Git State Auditor**: Analyzes the diff between `HEAD`, `origin/main`, and the working directory.
- **Action Set Clustering**: Groups conflicts into logical "Concern Clusters" to avoid user fatigue.

### 3.2 Visual Dashboard (Visual Companion)
A web-based interface (via the Interactions API / Visual Companion) that provides:
- **Global Overview**: Summary of all identified Action Sets.
- **Side-by-Side Comparison**: Snippets and metadata for conflicting files.
- **Resolution UI**: Interactive buttons for `Keep`, `Delete`, `Merge`, and `Stash`.

### 3.3 Execution & Git Lifecycle
- **Safe Execution**: All deletions are preceded by a temporary backup in `.maintainer_backup/`.
- **Atomic Commits**: Each resolved cluster results in a specific git commit.
- **Post-Action Validation**: Runs existing repository tests (e.g., `tests/argos/`) to ensure no breaking changes.

## 4. Components

### `repo_maintainer.py` (CLI / API)
- `scan()`: Traverses the repo and builds the conflict graph.
- `cluster()`: Runs the grouping algorithm.
- `resolve(action_set_id, strategy)`: Applies the chosen strategy.

### `dashboard.html` (UI)
- A responsive HTML/JS interface that communicates with the scanner via JSON payloads.

## 5. Success Criteria
- [ ] No redundant files across `Text/`, `docs/`, and `vault/`.
- [ ] `git status` shows a clean working directory (or a structured set of intended changes).
- [ ] All repository tests pass.
- [ ] `corpus-data.json` is validated against the consolidated filesystem.

## 6. Risk Assessment
- **Accidental Deletion**: Mitigated by `.maintainer_backup/` and git's ability to revert.
- **Over-Clustering**: Mitigated by allowing the user to "Unpack" a cluster if it's too broad.
