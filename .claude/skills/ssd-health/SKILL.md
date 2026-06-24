---
name: ssd-health
description: >
  Verify /media/ana/SSD_DATA SSD mount, symlink integrity for data/raw/{BR,FR,UK,DE,US,BE},
  optionally ingest new images from the SSD drop zone into corpus/imagens/, and run
  the SSD backup script. Use when the user says "ssd", "mount check", "verificar ssd",
  "ingest drive", "backup iconocracia", "sync ssd", or before any corpus operation that
  reads or writes to data/raw/.
user-invocable: true
---

Verifies SSD infrastructure for the ICONOCRACIA corpus. Does NOT touch JSON ledgers
(that is `sync-corpus`). Concerns: mount state, symlink health, ingest from drop zone,
and backup invocation.

## Host

Linux (Debian). The SSD is partition `sdb1`, filesystem label `SSD_DATA`, and
auto-mounts at `/media/ana/SSD_DATA`. Mac-era paths (`/Volumes/Iconocracia`,
`/Volumes/ICONOCRACIA`) are stale and no longer resolve — do not use them.

## Phase 1 — Mount check

```bash
MOUNT=/media/ana/SSD_DATA

if [ -d "$MOUNT" ]; then
  echo "SSD montado em $MOUNT"
else
  echo "SSD AUSENTE — verifique se sdb1 (label SSD_DATA) está montado; abortar"
  exit 1
fi
```

If the drive is connected but not mounted, report it and let the user mount it
(e.g. via the file manager or `udisksctl mount -b /dev/sdb1`). Do not auto-mount.

## Phase 2 — Symlink integrity

For each country in BR FR UK DE US BE, verify `$REPO/data/raw/$C` is a symlink
pointing into `$MOUNT/corpus/imagens/$C`. Report broken or missing links.

```bash
REPO="$CLAUDE_PROJECT_DIR"
for C in BR FR UK DE US BE; do
  LINK="$REPO/data/raw/$C"
  if [ -L "$LINK" ]; then
    TARGET=$(readlink "$LINK")
    [ -d "$LINK" ] && echo "OK  $C → $TARGET" || echo "BROKEN $C → $TARGET"
  else
    echo "MISSING $C (not a symlink)"
  fi
done
```

## Phase 3 — Ingest (optional, on user request)

Process `$MOUNT/iconocracy-ingest/`:

1. List files. Require SCOUT-NNN prefix with country code. Reject unnamed files
   and flag them `#revisar-nome`.
2. For each valid file, move to `$MOUNT/corpus/imagens/<COUNTRY>/` based on
   the country code in the filename.
3. Append to `$REPO/data/raw/drive-manifest.json`. Each entry shape:
   `{ "item_id": "SCOUT-NNN", "sha256": "<hex>", "origin_url": "<url>" }`.
4. Log to `$REPO/vault/sessoes/ingest-YYYY-MM-DD.md` (ISO date).

Prefer existing Python tooling if available:
```bash
conda run -n iconocracy python "$REPO/tools/scripts/ingest_from_ssd.py" --dry-run
```

If the script does not exist, stop and report the gap — do not invent an
ingest script ad hoc. User decides whether to scaffold it.

## Phase 4 — Backup runner

Wrapper around existing script:
```bash
bash "$MOUNT/backups/backup-iconocracia.sh"
```

Runs only when user explicitly requests backup. Confirms before execution
(destructive-adjacent: rsync + git mirror push).

## Report format

```
| Passo              | Status | Detalhe                               |
|--------------------|--------|---------------------------------------|
| Mount              | OK     | /media/ana/SSD_DATA                   |
| Symlinks           | OK     | 6/6 válidos                           |
| Ingest             | SKIP   | não solicitado                        |
| Backup             | SKIP   | não solicitado                        |
```

## When NOT to use

- Corpus data drift, schema validation → use `sync-corpus`
- New candidate dedupe → use `scout-dedupe`
- Public release → use `release-gate`
