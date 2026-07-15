---
name: archive-inbox
description: triage, normalize, deduplicate, name, tag, and route mixed research materials. use when the user provides links, screenshots, images, pdfs, citations, loose notes, downloads, or batches that need to be organized across google drive, dropbox, github, anavanzin.com, iconocracia.com, or the mnemosyne research workflow.
---

# Archive Inbox

Turn an unruly intake pile into a traceable research queue. Preserve originals, expose uncertainty, and recommend the best destination instead of treating every file system as interchangeable.

## Core workflow

1. Inventory every item before moving, renaming, or publishing anything.
2. Identify the material type: source image, document, working note, citation, dataset, code/content file, publication asset, or unresolved fragment.
3. Extract only observable or documented metadata. Mark guessed fields as unresolved.
4. Search authorized sources for duplicates, earlier versions, related records, and existing project taxonomy.
5. Assign a destination using `references/destination-matrix.md`.
6. Propose a normalized filename and stable record using `references/metadata-schema.md` and `references/naming-and-dedup.md`.
7. Separate actions into:
   - safe now: inventory, metadata extraction, duplicate comparison, destination recommendation;
   - requires authorization: rename, move, delete, overwrite, commit, publish, or merge.
8. Execute authorized actions through available connectors. Never claim an action succeeded without tool confirmation.
9. Hand research-ready items to Mnemosyne Research Atelier with provenance intact.
10. Report unresolved items and the smallest next action that would clarify them.

## Destination logic

- Prefer Google Drive for active writing, research notes, chapter drafts, fichamentos, spreadsheets, and collaborative working documents.
- Prefer Dropbox for original media, high-resolution images, scans, large archival files, exports, and versioned binaries.
- Prefer GitHub for code, structured content, schemas, taxonomies, manifests, public-site assets, and files that benefit from diffs and review.
- Treat anavanzin.com and iconocracia.com as publication surfaces, not raw storage. Route only publication-ready material there through the relevant repository or editorial workflow.
- When two destinations are plausible, recommend one primary home and one linked reference. Do not create uncontrolled duplicates.

## Intake modes

### Quick capture

Use for one to five items. Return a compact intake table, destination recommendation, filename, tags, and next action.

### Full triage

Use for mixed or ambiguous material. Return the complete record template below and explain conflicts.

### Batch audit

Use for folders or large collections. Group by duplicate families, metadata gaps, project relevance, and recommended destination. Surface risky moves before performing them.

## Default output

# Intake report

## Summary
State item count, likely duplicates, urgent risks, and recommended routing.

## Item records
For each item include:
- intake id;
- current name or url;
- material type;
- title or provisional title;
- creator or source;
- date or date range;
- provenance;
- rights or access note;
- project relation;
- controlled tags;
- duplicate or version status;
- recommended filename;
- recommended destination and folder;
- confidence: high, medium, or low;
- next action.

## Actions
Separate completed actions from proposed actions and blocked actions.

## Research handoff
List items ready for Mnemosyne Research Atelier and the question each item could support.

## Non-negotiable rules

- Preserve the original file or source reference until the user authorizes deletion.
- Never manufacture dates, authors, archive names, rights statements, or source chains.
- Do not rename files solely for aesthetic consistency when the old name carries archival evidence.
- Do not deduplicate by visual similarity alone. Compare source, dimensions, checksum when available, metadata, and content.
- Do not move an item merely because a folder name sounds relevant.
- Use the user's language for the report. Preserve original-language titles and provide translations separately.
- Cite connector and web evidence when factual claims depend on it.

## Resources

- Read `references/destination-matrix.md` when choosing storage or publication destinations.
- Read `references/metadata-schema.md` when producing full records or manifests.
- Read `references/naming-and-dedup.md` when renaming files or assessing duplicates.
- Copy `assets/intake-manifest.csv` when the user needs a reusable batch manifest.
- Copy `assets/intake-record.md` when the user needs a human-readable record template.
