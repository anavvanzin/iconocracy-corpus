# Notion Capture Draft - 2026-03-31

This draft packages the current Codex conversation into Notion-ready pages.
It was prepared locally because direct Notion write access was not available in
this session.

Source conversation date: 2026-03-31
Source context: current Codex thread in `/Users/ana/iconocracy-corpus`

## Delivery Notes

- Notion MCP resources/tools were not exposed in this session.
- `codex mcp list` shows `notion` configured, but authentication is not usable here.
- `tools/scripts/notion_sync.py` exists only as scaffolding and does not implement push/create yet.
- No `NOTION_API_KEY` or `NOTION_CORPUS_DB_ID` environment variables were available.

## Suggested Page 1 - Documentation

### Database

General Documentation Database

### Properties

- Title: Conversation Capture - Notion Knowledge Capture Request
- Type: Reference
- Category: Operations
- Tags: notion, codex, knowledge-capture, iconocracy-corpus
- Status: Draft
- Owner: leave blank unless mapped to the correct Notion user
- Last Reviewed: 2026-03-31

### Content

# Conversation Capture - Notion Knowledge Capture Request

## Summary

This thread requested the capture of the current conversation into structured
Notion pages with decisions, action items, and owners when known, using the
`notion-knowledge-capture` workflow.

## Context

- The request was made on 2026-03-31 in the `iconocracy-corpus` workspace.
- The skill instructions point to a Notion-first workflow: identify the correct
  destination database, search/fetch existing pages, create or update pages, and
  link follow-up tasks.
- In this session, direct Notion tool access was not available, so the content
  was structured locally as a Notion-ready draft instead of being published.

## Key Facts

- The repository includes a public research hub link in the README:
  `https://www.notion.so/322158101a0581568e58cfc997b7b727`.
- The local repository includes a Notion sync scaffold at
  `tools/scripts/notion_sync.py`, but the script currently prints placeholder
  messages and does not create or update pages.
- The project documentation states that Notion acts as a cataloging/index
  surface, not as the canonical source of record for the corpus.

## Decisions Captured

1. Use the `notion-knowledge-capture` workflow as the intended method for
   converting the thread into structured documentation.
2. Do not report a successful Notion write when the session lacks usable Notion
   access.
3. Produce a Notion-ready local draft so the conversation can still be captured
   without losing structure or traceability.

## Action Items

| Action | Owner | Status | Notes |
|---|---|---|---|
| Enable usable Notion access for Codex in this environment | Ana Vanzin (inferred) | Pending | Requires a working Notion MCP session or API-based workflow |
| Re-run the conversation capture after Notion access is available | Codex + Ana Vanzin (inferred) | Pending | Use this draft as the source of truth for page creation |
| Decide the destination Notion database for conversation-level documentation | Ana Vanzin (inferred) | Pending | Recommended: General Documentation Database unless a dedicated decision/wiki DB already exists |

## Related Artifacts

- `/Users/ana/iconocracy-corpus/tools/scripts/notion_sync.py`
- `/Users/ana/iconocracy-corpus/docs/notion-schema.md`
- `/Users/ana/iconocracy-corpus/README.md`

## Suggested Page 2 - Decision Record

### Database

Decision Log Database

### Properties

- Decision: Use the notion-knowledge-capture workflow for this thread and fall back to a local draft if direct Notion write is unavailable
- Date: 2026-03-31
- Status: Accepted
- Domain: Operations
- Impact: Medium
- Deciders: Ana Vanzin (inferred from repository/workspace ownership)
- Stakeholders: ICONOCRACY research workspace users

### Content

# Use the notion-knowledge-capture workflow for this thread

## Context

The conversation requested a structured capture into Notion pages, explicitly
calling the `notion-knowledge-capture` skill. The expected output included
decisions, action items, and owners when known.

At execution time, the session did not expose usable Notion create/update tool
calls. Local inspection confirmed that:

- the `notion` MCP server is configured in Codex,
- active Notion resources were not visible in this session,
- the repository's `notion_sync.py` integration is still scaffolding, and
- no Notion API environment variables were available for a direct API fallback.

## Decision

Use the `notion-knowledge-capture` workflow as the primary method for the task,
but produce a local Notion-ready draft instead of claiming successful page
creation when direct Notion access is unavailable.

## Rationale

- This preserves fidelity to the requested workflow.
- It avoids a false success state.
- It keeps the conversation structured and ready for publication as soon as
  access is restored.

## Options Considered

### Option A - Claim capture completed without verification

Rejected. This would be inaccurate.

### Option B - Return only a chat summary

Rejected. This would lose the page structure requested by the user.

### Option C - Produce a Notion-ready draft locally

Accepted. This preserves structure and allows a later one-step transfer into
Notion.

## Consequences

### Positive

- The conversation is already normalized into reusable pages.
- Decisions and action items are preserved with dates and inferred ownership.
- The next successful Notion session can create the pages quickly.

### Negative

- The pages still need to be created in Notion.
- Owners in people fields may need manual mapping to actual Notion users.

## Implementation

1. Prepare a local draft with properties and page bodies.
2. Restore usable Notion access in Codex.
3. Create the documentation page and decision page in the chosen database(s).
4. Link the resulting pages from the relevant hub or workspace pages.

## Suggested Page 3 - Action Tracker

### Database

General Documentation Database or a task database if one already exists

### Properties

- Title: Follow-up Actions - Notion Capture for 2026-03-31 Thread
- Type: Reference
- Category: Operations
- Tags: notion, follow-up, codex
- Status: Draft
- Owner: leave blank unless mapped to the correct Notion user
- Last Reviewed: 2026-03-31

### Content

# Follow-up Actions - Notion Capture for 2026-03-31 Thread

| Action Item | Owner | Priority | Status | Rationale |
|---|---|---|---|---|
| Enable usable Notion MCP access for Codex | Ana Vanzin (inferred) | High | Pending | Required for direct page creation from Codex |
| Authenticate or reauthenticate the `notion` MCP server if needed | Ana Vanzin (inferred) | High | Pending | The server is configured but not usable in this session |
| Re-run conversation capture and publish the draft pages | Codex | Medium | Blocked | Depends on the previous step |
| Confirm the preferred destination database for future conversation captures | Ana Vanzin (inferred) | Medium | Pending | Recommended default is a general documentation database |

## Minimal Next Step

Once Notion access is working, create:

1. the documentation page from "Suggested Page 1"
2. the decision record from "Suggested Page 2"
3. the action tracker from "Suggested Page 3" if a dedicated tasks database is not preferred
