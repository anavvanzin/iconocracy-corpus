# GitHub Repositories Blueprint — ICONOCRACIA

This codemap details the repository architecture for Ana Vanzin's doctoral thesis **"Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"** (PPGD/UFSC).

The workspace is organized as a **Meta-Workspace** (`Research/`) containing sibling git repositories (remotes are managed independently, ignored by the parent).

```
/Users/ana/Research/                       ← [1] anavvanzin/Research
├── cowork/
├── docs/
├── hub/
│   ├── iconocracy-corpus/                 ← [2] anavvanzin/iconocracy-corpus
│   └── mnemosyne-scout/
├── apps/
│   ├── iconocracia-companion/             ← [3] anavvanzin/iconocracia-companion
│   ├── iconocracia-space/                 ← [4] anavvanzin/iconocracia-space
│   └── atlaslab/
├── labs/
│   └── iurisvision/                       ← [5] anavvanzin/iurisvision
└── vida-os/                               ← [6] anavvanzin/vida-os
```

---

## 1. Meta-Workspace: `anavvanzin/Research`
* **Local Directory:** `/Users/ana/Research`
* **Remote URL:** `https://github.com/anavvanzin/Research.git`
* **Tracking Policy:** Tracks only cowork summaries (`cowork/`), research notes/documentation (`docs/`), custom agent skills (`.claude/skills/`), and automation plans (`plans/`). Sub-repositories are untracked nested folders.
* **Role:** Orchestrates the multi-agent workspaces, cross-project session states, and overall timeline management for the thesis project.

---

## 2. Thesis Monorepo: `anavvanzin/iconocracy-corpus`
* **Local Directory:** `/Users/ana/Research/hub/iconocracy-corpus` (symlinked from `/Users/ana/iconocracy-corpus`)
* **Remote URLs:**
  - `origin`: `git@github.com:anavvanzin/iconocracy-corpus.git`
  - `ssd-mirror`: `/Volumes/ICONOCRACIA/git-mirrors/iconocracy-corpus.git` (external SSD backup mirror)
* **Role:** The **canonical heart of the thesis**. It contains:
  - `data/processed/records.jsonl` — the master canonical ledger.
  - `corpus/corpus-data.json` — the public export file.
  - `tese/manuscrito/` — compiled LaTeX/Markdown manuscript chapters.
  - `tools/scripts/` — python automation pipelines (reconciliation, validation, acquisition, analysis).
  - `notebooks/` — OLS regressions, Kruskal-Wallis tests, temporal analysis, and clustering.

---

## 3. Companion App: `anavvanzin/iconocracia-companion`
* **Local Directory:** `/Users/ana/Research/apps/iconocracia-companion`
* **Remote URL:** `https://github.com/anavvanzin/iconocracia-companion.git`
* **Role:** React / Next.js web application providing a rich user interface (corpus explorer, index visualizer, and indicators dashboard) to interactively explore the dataset.

---

## 4. HF Space: `anavvanzin/iconocracia-space`
* **Local Directory:** `/Users/ana/Research/apps/iconocracia-space`
* **Remote URL:** `https://github.com/anavvanzin/iconocracia-space.git`
* **Role:** Deployment package targeting Hugging Face Spaces, serving as the public cloud-hosted interface for the Iconocracy dataset search.

---

## 5. Visual Lab: `anavvanzin/iurisvision`
* **Local Directory:** `/Users/ana/Research/labs/iurisvision`
* **Remote URL:** `https://github.com/anavvanzin/iurisvision.git`
* **Role:** Codebase, visual legal culture datasets, and tools focused on courtroom visual analysis (e.g., video-based research for the blindfolded Justice STF courtroom case study).

---

## 6. Personal OS: `anavvanzin/vida-os`
* **Local Directory:** `/Users/ana/Research/vida-os`
* **Remote URL:** `git@github.com:anavvanzin/vida-os.git`
* **Role:** Personal productivity environment, daily tracking mechanisms, shell configs, and task dashboards.

---

## Shared Integrations
- **Data Storage:** Binaries and high-resolution TIFFs are quarentened on Google Drive and an external SSD to satisfy ADR-001 (git metadata-only).
- **Zotero:** Academic citation catalog integrated via Zotero Web API.
- **Hugging Face Hub:** Dataset releases and models are pushed directly to the Hugging Face organization space.
