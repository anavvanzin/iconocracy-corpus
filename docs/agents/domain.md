# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (this repo's layout):

```
/
├── CONTEXT.md                              ← created lazily by /grill-with-docs
├── docs/adr/
│   ├── 001-drive-as-raw-store.md
│   ├── 002-notion-as-index.md
│   ├── 003-jsonl-as-canonical.md
│   ├── 004-vault-as-index.md
│   └── 005-github-and-hf-release-surfaces.md
└── (corpus/, vault/, tese/, tools/, deploy/, …)
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root) — not used here:

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

For this thesis project specifically: the canonical terms (**endurecimento**, **Purificação Clássica**, **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual**, **Pathosformel**, **Zwischenraum**, **Nachleben**) are non-negotiable — see the *Mandatory Terminology* table in `CLAUDE.md`.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-001 (Drive as raw store) — but worth reopening because…_
