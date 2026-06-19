// Extension: audit-dashboard
// Interactive dashboard for corpus audit findings from companion-data.json
// Displays discrepancies, validates records, and highlights actionable items.

import { createServer } from "node:http";
import { joinSession, createCanvas } from "@github/copilot-sdk/extension";
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

const servers = new Map();

function findRepoRoot() {
    // Walk up from common paths to find .git directory, then verify by checking for corpus data files
    const startPaths = [
        process.cwd(),
        process.env.PWD || "/",
        "/Users/ana/copilot-worktrees/iconocracy-corpus/claude-fervent-meitner-u7lvik",
        "/Users/ana/copilot-worktrees/iconocracy-corpus",
        "/Users/ana/Research/hub/iconocracy-corpus",
    ];

    for (const start of startPaths) {
        if (!start) continue;
        let current = start;
        for (let i = 0; i < 10; i++) {
            const gitPath = path.join(current, ".git");
            if (fs.existsSync(gitPath)) {
                // Verify this is the iconocracy-corpus repo by checking for data files
                const recordsPath = path.join(current, "data/processed/records.jsonl");
                if (fs.existsSync(recordsPath)) {
                    return current;
                }
            }
            const parent = path.dirname(current);
            if (parent === current) break;
            current = parent;
        }
    }
    return null;
}

function loadAuditData() {
    try {
        const baseDir = findRepoRoot() || process.cwd();
        const dataPath = path.resolve(baseDir, "data/processed/records.jsonl");
        const corpusPath = path.resolve(baseDir, "corpus/corpus-data.json");
        
        if (fs.existsSync(dataPath) && fs.existsSync(corpusPath)) {
            const records = fs.readFileSync(dataPath, "utf-8").split("\n").filter(l => l.trim());
            const corpus = JSON.parse(fs.readFileSync(corpusPath, "utf-8"));
            
            const corpusCount = Array.isArray(corpus) 
                ? corpus.length 
                : corpus.items?.length || 0;
            
            return {
                recordsCount: records.length,
                corpusCount: corpusCount,
                status: "loaded"
            };
        }
    } catch (e) {
        return { status: "error", message: e.message };
    }
    return { status: "not_found" };
}

function renderHtml(instanceId, workspacePath, auditData) {
    const stats = auditData || loadAuditData(workspacePath);
    const driftStatus = stats.recordsCount && stats.corpusCount 
        ? stats.recordsCount === stats.corpusCount 
            ? "✓ aligned" 
            : `⚠ ${Math.abs(stats.recordsCount - stats.corpusCount)} item drift`
        : "—";
    
    return `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Audit Dashboard</title>
    <style>
      :root {
        --bg: var(--background-color-default, #ffffff);
        --text: var(--text-color-default, #1f2328);
        --muted: var(--text-color-muted, #656d76);
        --border: var(--border-color-default, #d0d7de);
      }
      * { box-sizing: border-box; }
      body {
        font-family: var(--font-sans, system-ui);
        background: var(--bg);
        color: var(--text);
        margin: 0;
        padding: 1.5rem;
      }
      h1 { font-size: 1.75rem; margin: 0 0 1rem; }
      .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
      .stat-box {
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 1rem;
        background: var(--bg);
      }
      .stat-label { color: var(--muted); font-size: 0.875rem; margin-bottom: 0.5rem; }
      .stat-value { font-size: 1.25rem; font-weight: 600; }
      .section { margin-bottom: 1.5rem; }
      .section h2 { font-size: 1rem; margin: 0 0 0.75rem; color: var(--text); }
      .findings { max-height: 300px; overflow-y: auto; border: 1px solid var(--border); border-radius: 4px; padding: 0.75rem; }
      .finding { padding: 0.5rem 0; font-size: 0.875rem; color: var(--muted); }
    </style>
  </head>
  <body>
    <h1>📊 Audit Dashboard</h1>
    
    <div class="stats">
      <div class="stat-box">
        <div class="stat-label">Records (canonical)</div>
        <div class="stat-value">${stats.recordsCount || "—"}</div>
      </div>
      <div class="stat-box">
        <div class="stat-label">Corpus (export)</div>
        <div class="stat-value">${stats.corpusCount || "—"}</div>
      </div>
    </div>
    
    <div class="section">
      <h2>Data Alignment</h2>
      <div class="finding">${driftStatus}</div>
    </div>
    
    <div class="section">
      <h2>Instance</h2>
      <div class="finding"><code>${instanceId}</code></div>
    </div>
  </body>
</html>`;
}

async function startServer(instanceId, workspacePath) {
    const auditData = loadAuditData(workspacePath);
    const server = createServer((req, res) => {
        if (req.url === "/data") {
            res.setHeader("Content-Type", "application/json; charset=utf-8");
            res.end(JSON.stringify(auditData));
        } else {
            res.setHeader("Content-Type", "text/html; charset=utf-8");
            res.end(renderHtml(instanceId, workspacePath, auditData));
        }
    });
    // Port 0 = let the OS pick a free ephemeral port. Bind to loopback only.
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    const address = server.address();
    const port = typeof address === "object" && address ? address.port : 0;
    return { server, url: `http://127.0.0.1:${port}/` };
}

const session = await joinSession({
    canvases: [
        createCanvas({
            id: "audit-dashboard",
            displayName: "Audit Dashboard",
            description: "Interactive dashboard for corpus audit findings. Displays records/corpus alignment, drift analysis, and validation status.",
            actions: [
                {
                    name: "reload_data",
                    description: "Reload audit data from canonical sources",
                    handler: async (ctx) => {
                        const data = loadAuditData();
                        await session.log(`[reload_data] loaded: records=${data.recordsCount}, corpus=${data.corpusCount}`, { level: "debug", ephemeral: false });
                        return { success: true, data, debug: { repoRoot: findRepoRoot(), cwd: process.cwd() } };
                    },
                },
                {
                    name: "export_findings",
                    description: "Export audit findings as JSON",
                    handler: async (ctx) => {
                        const data = loadAuditData();
                        await session.log(`[export_findings] exported: records=${data.recordsCount}, corpus=${data.corpusCount}`, { level: "debug", ephemeral: false });
                        return {
                            timestamp: new Date().toISOString(),
                            findings: data,
                            debug: { repoRoot: findRepoRoot(), cwd: process.cwd() },
                        };
                    },
                },
            ],
            open: async (ctx) => {
                let entry = servers.get(ctx.instanceId);
                if (!entry) {
                    entry = await startServer(ctx.instanceId);
                    servers.set(ctx.instanceId, entry);
                }
                return {
                    title: "Audit Dashboard",
                    url: entry.url,
                };
            },
            onClose: async (ctx) => {
                const entry = servers.get(ctx.instanceId);
                if (entry) {
                    servers.delete(ctx.instanceId);
                    await new Promise((resolve) => entry.server.close(() => resolve()));
                }
            },
        }),
    ],
});
