/**
 * Tropical Atlas — Cloudflare Pages Function
 * Handles all /api/* routes via Hono
 */
import { Hono } from "hono";
import { cors } from "hono/cors";

interface Env {
  CORPUS_DB: D1Database;
  CORPUS_IMAGES?: R2Bucket;
}

const app = new Hono<{ Bindings: Env }>();

app.use("/api/*", cors());

// ── Utility ─────────────────────────────────────────────────────────────────

function parseCSV(text: string): Record<string, string>[] {
  const lines = text.split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return [];
  const headers = parseCSVLine(lines[0]);
  return lines
    .slice(1)
    .map((line) => {
      const vals = parseCSVLine(line);
      const row: Record<string, string> = {};
      headers.forEach((h, i) => {
        row[h.trim()] = (vals[i] ?? "").trim();
      });
      return row;
    })
    .filter((row) => Object.values(row).some(Boolean));
}

function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === "," && !inQuotes) {
      result.push(current);
      current = "";
    } else {
      current += ch;
    }
  }
  result.push(current);
  return result;
}

function rowToEntry(row: Record<string, string>): Record<string, unknown> {
  const entry: Record<string, unknown> = {};
  const fields = [
    "id","title","date","year","period","period_norm","creator",
    "country","country_pt","medium","medium_norm","support","source_archive",
    "url","thumbnail_url","description","citation_abnt","motif_str","tags_str",
    "scope_note","coded_by","coded_at","notes",
  ];
  fields.forEach((f) => {
    if (row[f] !== undefined) entry[f] = row[f] || null;
  });
  // Numerics
  entry.year = row.year ? parseInt(row.year) || null : null;
  entry.in_scope = row.in_scope === "False" ? 0 : 1;
  const scores = [
    "desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
    "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
    "monocromatizacao","serialidade","inscricao_estatal","purificacao_composto",
  ];
  scores.forEach((s) => {
    entry[s] = row[s] ? parseFloat(row[s]) || null : null;
  });
  entry.regime_iconocratico = row.regime_iconocratico || null;
  return entry;
}

function buildWhereClause(
  params: Record<string, string>
): { sql: string; bindings: unknown[] } {
  const conditions: string[] = ["in_scope = 1"];
  const bindings: unknown[] = [];
  if (params.country && params.country !== "all") {
    conditions.push("country_pt = ?");
    bindings.push(params.country);
  }
  if (params.medium && params.medium !== "all") {
    conditions.push("medium_norm = ?");
    bindings.push(params.medium);
  }
  if (params.regime && params.regime !== "all") {
    conditions.push("regime_iconocratico = ?");
    bindings.push(params.regime);
  }
  if (params.period && params.period !== "all") {
    conditions.push("period_norm = ?");
    bindings.push(params.period);
  }
  if (params.figure && params.figure !== "all") {
    conditions.push("motif_str LIKE ?");
    bindings.push(`%${params.figure}%`);
  }
  if (params.q) {
    conditions.push("(title LIKE ? OR description LIKE ? OR motif_str LIKE ?)");
    const term = `%${params.q}%`;
    bindings.push(term, term, term);
  }
  return {
    sql: conditions.length ? `WHERE ${conditions.join(" AND ")}` : "",
    bindings,
  };
}

// ── Routes ───────────────────────────────────────────────────────────────────

// GET /api/entries — list with filters
app.get("/api/entries", async (c) => {
  const params = Object.fromEntries(new URL(c.req.url).searchParams.entries());
  const { sql, bindings } = buildWhereClause(params);
  const limit = Math.min(parseInt(params.limit ?? "200"), 500);
  const offset = parseInt(params.offset ?? "0");

  const query = `
    SELECT id, title, country_pt, medium_norm, regime_iconocratico,
           period_norm, motif_str, thumbnail_url, url, year, description,
           citation_abnt, creator, source_archive, purificacao_composto
    FROM atlas_entries ${sql}
    ORDER BY year ASC, id ASC
    LIMIT ${limit} OFFSET ${offset}
  `;

  try {
    const { results } = await c.env.CORPUS_DB.prepare(query)
      .bind(...bindings)
      .all();
    const countResult = await c.env.CORPUS_DB.prepare(
      `SELECT COUNT(*) as n FROM atlas_entries ${sql}`
    )
      .bind(...bindings)
      .first<{ n: number }>();

    return c.json({ entries: results, total: countResult?.n ?? 0, limit, offset });
  } catch (err: unknown) {
    return c.json({ error: String(err) }, 500);
  }
});

// GET /api/entries/:id — single entry with all LPAI scores
app.get("/api/entries/:id", async (c) => {
  const id = c.req.param("id");
  const row = await c.env.CORPUS_DB.prepare(
    "SELECT * FROM atlas_entries WHERE id = ?"
  )
    .bind(id)
    .first();
  if (!row) return c.json({ error: "Not found" }, 404);
  return c.json(row);
});

// GET /api/filters — distinct filter values for the UI dropdowns
app.get("/api/filters", async (c) => {
  const [countries, mediums, regimes, periods] = await Promise.all([
    c.env.CORPUS_DB.prepare(
      "SELECT DISTINCT country_pt as v FROM atlas_entries WHERE in_scope=1 AND country_pt IS NOT NULL ORDER BY country_pt"
    ).all<{ v: string }>(),
    c.env.CORPUS_DB.prepare(
      "SELECT DISTINCT medium_norm as v FROM atlas_entries WHERE in_scope=1 AND medium_norm IS NOT NULL ORDER BY medium_norm"
    ).all<{ v: string }>(),
    c.env.CORPUS_DB.prepare(
      "SELECT DISTINCT regime_iconocratico as v FROM atlas_entries WHERE in_scope=1 AND regime_iconocratico IS NOT NULL ORDER BY regime_iconocratico"
    ).all<{ v: string }>(),
    c.env.CORPUS_DB.prepare(
      "SELECT DISTINCT period_norm as v FROM atlas_entries WHERE in_scope=1 AND period_norm IS NOT NULL ORDER BY year ASC"
    ).all<{ v: string }>(),
  ]);
  return c.json({
    countries: countries.results.map((r) => r.v),
    mediums: mediums.results.map((r) => r.v),
    regimes: regimes.results.map((r) => r.v),
    periods: periods.results.map((r) => r.v),
  });
});

// POST /api/import/preview — parse CSV, return first 10 rows + errors
app.post("/api/import/preview", async (c) => {
  const body = await c.req.formData();
  const file = body.get("file") as File | null;
  if (!file) return c.json({ error: "No file" }, 400);
  const text = await file.text();
  const rows = parseCSV(text);
  const errors: string[] = [];
  const mapped = rows.slice(0, 10).map((row, i) => {
    const e = rowToEntry(row);
    if (!e.id) errors.push(`Linha ${i + 2}: campo 'id' ausente`);
    if (!e.title) errors.push(`Linha ${i + 2}: campo 'title' ausente`);
    return e;
  });
  return c.json({ preview: mapped, total: rows.length, errors });
});

// POST /api/import/commit — insert CSV rows into D1
app.post("/api/import/commit", async (c) => {
  const body = await c.req.formData();
  const file = body.get("file") as File | null;
  const mode = (body.get("mode") as string) ?? "append"; // append | replace
  if (!file) return c.json({ error: "No file" }, 400);
  const text = await file.text();
  const rows = parseCSV(text);

  if (mode === "replace") {
    await c.env.CORPUS_DB.prepare("DELETE FROM atlas_entries").run();
  }

  const cols = [
    "id","title","date","year","period","period_norm","creator","country","country_pt",
    "medium","medium_norm","support","source_archive","url","thumbnail_url","description",
    "citation_abnt","motif_str","tags_str","in_scope","scope_note",
    "desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
    "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
    "monocromatizacao","serialidade","inscricao_estatal","purificacao_composto",
    "regime_iconocratico","coded_by","coded_at","notes","source_file",
  ];
  const placeholders = cols.map(() => "?").join(",");
  const upsertSQL = `INSERT OR REPLACE INTO atlas_entries (${cols.join(",")}) VALUES (${placeholders})`;

  let imported = 0;
  const errs: string[] = [];
  const now = new Date().toISOString();
  const filename = file.name;

  // Batch in groups of 50
  for (let i = 0; i < rows.length; i += 50) {
    const batch = rows.slice(i, i + 50);
    const statements = batch
      .map((row, j) => {
        const e = rowToEntry(row);
        if (!e.id || !e.title) {
          errs.push(`Linha ${i + j + 2}: id ou title ausente`);
          return null;
        }
        e.source_file = filename;
        const vals = cols.map((c) =>
          c === "imported_at" ? now : (e[c] ?? null)
        );
        return c.env.CORPUS_DB.prepare(upsertSQL).bind(...vals);
      })
      .filter(Boolean) as D1PreparedStatement[];

    if (statements.length) {
      try {
        await c.env.CORPUS_DB.batch(statements);
        imported += statements.length;
      } catch (err: unknown) {
        errs.push(`Batch erro em linha ~${i + 2}: ${String(err)}`);
      }
    }
  }
  return c.json({ imported, skipped: rows.length - imported, errors: errs.slice(0, 20) });
});

// DELETE /api/entries/:id
app.delete("/api/entries/:id", async (c) => {
  await c.env.CORPUS_DB.prepare("DELETE FROM atlas_entries WHERE id = ?")
    .bind(c.req.param("id"))
    .run();
  return c.json({ ok: true });
});

// GET /api/export — CSV download of all entries
app.get("/api/export", async (c) => {
  const { results } = await c.env.CORPUS_DB.prepare(
    "SELECT * FROM atlas_entries WHERE in_scope=1 ORDER BY year ASC, id ASC"
  ).all();
  const cols = results.length ? Object.keys(results[0]) : [];
  const header = cols.join(",");
  const escapeCSV = (v: unknown) => {
    if (v === null || v === undefined) return "";
    const s = String(v);
    return s.includes(",") || s.includes('"') || s.includes("\n")
      ? `"${s.replace(/"/g, '""')}"`
      : s;
  };
  const rows = results.map((r) => cols.map((c) => escapeCSV((r as Record<string, unknown>)[c])).join(","));
  const csv = [header, ...rows].join("\n");
  return new Response(csv, {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": 'attachment; filename="iconocracy-corpus.csv"',
    },
  });
});

// GET /api/template — blank CSV template with headers
app.get("/api/template", async (c) => {
  const cols = [
    "id","title","date","year","period","period_norm","creator","country","country_pt",
    "medium","medium_norm","support","source_archive","url","thumbnail_url","description",
    "citation_abnt","motif_str","tags_str","in_scope","scope_note",
    "desincorporacao","rigidez_postural","dessexualizacao","uniformizacao_facial",
    "heraldizacao","enquadramento_arquitetonico","apagamento_narrativo",
    "monocromatizacao","serialidade","inscricao_estatal","purificacao_composto",
    "regime_iconocratico","coded_by","coded_at","notes",
  ];
  return new Response(cols.join(",") + "\n", {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": 'attachment; filename="iconocracy-template.csv"',
    },
  });
});

// GET /api/stats — summary counts
app.get("/api/stats", async (c) => {
  const [total, byRegime, byCountry, byMedium] = await Promise.all([
    c.env.CORPUS_DB.prepare("SELECT COUNT(*) as n FROM atlas_entries WHERE in_scope=1").first<{ n: number }>(),
    c.env.CORPUS_DB.prepare(
      "SELECT regime_iconocratico as regime, COUNT(*) as n FROM atlas_entries WHERE in_scope=1 GROUP BY regime_iconocratico ORDER BY n DESC"
    ).all(),
    c.env.CORPUS_DB.prepare(
      "SELECT country_pt as country, COUNT(*) as n FROM atlas_entries WHERE in_scope=1 GROUP BY country_pt ORDER BY n DESC LIMIT 10"
    ).all(),
    c.env.CORPUS_DB.prepare(
      "SELECT medium_norm as medium, COUNT(*) as n FROM atlas_entries WHERE in_scope=1 GROUP BY medium_norm ORDER BY n DESC"
    ).all(),
  ]);
  return c.json({
    total: total?.n ?? 0,
    byRegime: byRegime.results,
    byCountry: byCountry.results,
    byMedium: byMedium.results,
  });
});

export const onRequest = app.fetch;
