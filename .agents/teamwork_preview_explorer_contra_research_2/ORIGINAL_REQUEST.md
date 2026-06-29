## 2026-06-27T01:00:11Z
You are a teamwork_preview_explorer agent.
Your ID is teamwork_preview_explorer_contra_research_2.
Your working directory is /Users/ana/Research/hub/iconocracy-corpus/.agents/teamwork_preview_explorer_contra_research_2.
Please update your progress.md and create your own BRIEFING.md in your working directory.

Your task is to analyze the codebase, local documents, and any metadata files to research three curated contra-allegory cases:
1. CONTRA-002: The 1975 internal sculpture located in the STF (Sala dos Bustos) that was vandalized. Find the institutional STF report/URL and correct citation.
   - Look in files like `vault/prompts/escrita/prompt-max-planck-summary.md` and any other files mentioning 'migalhas' or '379795' or 'bustos'.
   - Search for the STF report URL and citation.
2. CONTRA-003: The 2018 Arc de Triomphe Marianne/Rude mutilation episode.
   - Find details about the incident in the workspace (such as dates, descriptions, and citations).
3. CONTRA-004: Deborah de Robertis' performance (2018).
   - Find the AFP/Getty Images visual sources or citations in the workspace.

Also:
4. Read the standard template `vault/_templates/ficha-catalografica.md` to see its frontmatter properties and structure.
5. List files in `vault/candidatos/` to find:
   - What sequence numbers are next for `BR-`, `FR-`, and `SCOUT-` prefixes.
   - Propose the correct filename and prefix choice for each of CONTRA-002, CONTRA-003, and CONTRA-004.
6. Read the drafts `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md` to see where §3.4 is and what is already written there, and recommend the exact edits to integrate these three cases.
7. Identify the schema validation command (e.g. `python tools/scripts/validate_schemas.py` or similar) and how to run it.

Write a detailed markdown report inside your own folder under `.agents/teamwork_preview_explorer_contra_research_2/handoff.md` with all your findings and recommendations. Once completed, call send_message to report back. Do not write or edit any files outside of your own folder.
