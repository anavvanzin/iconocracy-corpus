import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { extname, resolve } from "node:path";

const appRoot = resolve(import.meta.dirname, "..");
const repoRoot = resolve(appRoot, "../..");
const analysisRoot = "docs/research/huggingface/regime-coverage-2026-08-13";
const outputDir = resolve(appRoot, "dist/server");

const files = new Map([
  ["/", resolve(appRoot, "site/index.html")],
  ["/index.html", resolve(appRoot, "site/index.html")],
  ["/og.png", resolve(appRoot, "public/og.png")],
  ["/sun-seal.svg", resolve(appRoot, "public/sun-seal.svg")],
  ["/pixel-justitia-sky.png", resolve(appRoot, "public/pixel-justitia-sky.png")],
  ["/project-banner.png", resolve(appRoot, "public/project-banner.png")],
  [
    "/analysis/huggingface-regime-coverage-2026-08-13/README.md",
    resolve(repoRoot, analysisRoot, "README.md"),
  ],
  [
    "/analysis/huggingface-regime-coverage-2026-08-13/coverage.csv",
    resolve(repoRoot, analysisRoot, "coverage.csv"),
  ],
  [
    "/analysis/huggingface-regime-coverage-2026-08-13/coverage.svg",
    resolve(repoRoot, analysisRoot, "coverage.svg"),
  ],
  [
    "/analysis/huggingface-regime-coverage-2026-08-13/query.sql",
    resolve(repoRoot, analysisRoot, "query.sql"),
  ],
  [
    "/analysis/huggingface-regime-coverage-2026-08-13/render_coverage.py",
    resolve(repoRoot, analysisRoot, "render_coverage.py"),
  ],
]);

const contentTypes = {
  ".csv": "text/csv; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".png": "image/png",
  ".py": "text/plain; charset=utf-8",
  ".sql": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml; charset=utf-8",
};

const assets = Object.fromEntries(
  [...files].map(([route, source]) => {
    const body = readFileSync(source).toString("base64");
    const type = contentTypes[extname(source)] ?? "application/octet-stream";
    return [route, { body, type }];
  }),
);

const worker = `const assets = ${JSON.stringify(assets)};

function decodeBase64(value) {
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return bytes;
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const asset = assets[url.pathname];
    if (!asset) {
      return new Response("Not found", { status: 404 });
    }

    let body = decodeBase64(asset.body);
    if (asset.type.startsWith("text/html")) {
      body = new TextDecoder()
        .decode(body)
        .replaceAll("__SITE_ORIGIN__", url.origin);
    }

    return new Response(body, {
      headers: {
        "Content-Type": asset.type,
        "Cache-Control": asset.type.startsWith("text/html")
          ? "public, max-age=0, must-revalidate"
          : "public, max-age=3600",
        "X-Content-Type-Options": "nosniff",
      },
    });
  },
};
`;

rmSync(resolve(appRoot, "dist"), { force: true, recursive: true });
mkdirSync(outputDir, { recursive: true });
writeFileSync(resolve(outputDir, "index.js"), worker);
console.log(`Built ICONOCRACIA-CV Sites Worker with ${files.size} routes.`);
