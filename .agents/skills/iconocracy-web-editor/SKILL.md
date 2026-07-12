---
name: iconocracy-web-editor
description: audit, write, edit, and publish bilingual research content for iconocracia.com and anavanzin.com through their github repositories and connected source materials. use when the user asks to create or revise object pages, atlas panels, essays, project pages, metadata, navigation, seo, alt text, content schemas, or direct repository changes and deployments.
---

# Iconocracy Web Editor

Translate rigorous research into public digital form without flattening it into generic cultural copy. Inspect the actual repository and content model before proposing or editing pages.

## First decision

Determine the requested mode:

1. Audit only: inspect site, repository, content model, and editorial gaps without changing files.
2. Prepare changes: create publication-ready files or patches for review.
3. Direct edit: modify the GitHub repository after authorization.
4. Publish or deploy: merge, release, or trigger deployment only after explicit authorization and successful validation.

## Repository workflow

1. Locate the authoritative repository and confirm the target site, branch, framework, content directories, and deployment path.
2. Read local contributor instructions, schemas, components, and recent examples before editing.
3. Search Google Drive and Dropbox only for source material relevant to the requested page. Treat anavanzin.com and iconocracia.com as public references for current voice and architecture.
4. Preserve the repository's existing content model unless there is a documented reason to change it.
5. For direct edits, default to a new branch and a focused pull request. Push directly to the default branch only when the user explicitly authorizes that exact action.
6. Keep commits narrow and descriptive. Do not mix unrelated design, dependency, and editorial changes.
7. Run available formatting, linting, tests, builds, link checks, and content validation.
8. Report changed files, validation results, remaining risks, and the review or deployment state.

## Editorial workflow

1. Identify the content type using `references/content-schema.md`.
2. Verify every factual claim, object identifier, date, quotation, and image credit.
3. Separate public narrative from internal scholarly notes. Do not publish uncertainty as fact.
4. Write Portuguese and English as parallel editorial texts, not mechanical translations.
5. Provide accessible alt text, useful metadata, and restrained search optimization using `references/bilingual-seo.md`.
6. Preserve research provenance in frontmatter, source notes, or linked records as the repository permits.
7. Apply the voice rules in `references/editorial-style.md`.

## Default output for content work

# Editorial change set

## Purpose
State audience, page type, and the public question the page answers.

## Source basis
List repository files and research sources used. Mark unresolved evidence.

## Content
Deliver the requested page, entry, or revision in the repository's actual format.

## Metadata
Include title, description, slug, language relation, dates, credits, tags, alt text, and source references as supported by the schema.

## Repository changes
List files created, modified, moved, or deleted.

## Validation
Report commands or checks run and their results. Never claim a build passed without evidence.

## Publication state
State whether changes are draft, committed to a branch, in a pull request, merged, deployed, or blocked.

## Editorial principles

- Avoid academic jargon when a precise ordinary phrase exists.
- Do not replace complexity with vague poetic language.
- Keep the project's slightly nocturnal visual intelligence without gothic cosplay.
- Do not overuse Justice, Marianne, haunted archives, ruins, shadows, ghosts, or the gaze as automatic metaphors.
- Let objects and evidence lead the page.
- Make bilingual text equally authored, while preserving necessary differences in cultural context.
- Never expose private drafts, restricted archival material, personal data, secrets, tokens, or licensed high-resolution files.
- Respect image rights and document uncertainty.

## Direct-edit safety

- Inspect before editing.
- Never overwrite user work without reading it.
- Never delete, force-push, merge, publish, or deploy without the required authorization.
- Never commit credentials or connector exports.
- Prefer reversible changes and branches.
- If the repository is unavailable, prepare a clearly labeled patch or content file instead of pretending to have edited it.

## Handoffs

- Request object research from Mnemosyne Research Atelier.
- Request panel composition from Atlas Panel Composer.
- Request chapter-derived structure from Thesis Chapter Architect.
- Run Intellectual Tastekeeper before publication when the text is conceptually important.

## Resources

- Read `references/content-schema.md` to choose fields and page structure.
- Read `references/editorial-style.md` before writing public copy.
- Read `references/github-workflow.md` before repository changes.
- Read `references/bilingual-seo.md` for metadata, translation, and accessibility.
- Use templates in `assets/` only when compatible with the repository's actual schema.
