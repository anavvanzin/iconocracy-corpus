#!/usr/bin/env bash
# abnt-precommit regex gate
# Usage: check.sh [file1.md file2.md ...]
#   No args → scan staged .md in vault/tese/ + tese/manuscrito/
#   Exit 0 = clean, 1 = violations found

set -u
ERRS=0
BIB_PATHS=("vault/tese/references.bib" "tese/manuscrito/references.bib")
BIB=""
for p in "${BIB_PATHS[@]}"; do
  [[ -f "$p" ]] && BIB="$p" && break
done

# Collect targets
if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  mapfile -t FILES < <(git diff --cached --name-only --diff-filter=ACM 2>/dev/null \
    | grep -E '(vault/tese|tese/manuscrito)/.*\.md$' || true)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "abnt-precommit: no thesis .md files to check"
  exit 0
fi

# Extract defined BibTeX keys once
DEFINED_KEYS=""
if [[ -n "$BIB" ]]; then
  DEFINED_KEYS=$(grep -E '^@[a-zA-Z]+\{' "$BIB" | sed -E 's/@[a-zA-Z]+\{([^,]+),.*/\1/' | sort -u)
fi

report() {
  local file=$1 line=$2 rule=$3 msg=$4
  printf "  %s:%s [%s] %s\n" "$file" "$line" "$rule" "$msg"
  ERRS=$((ERRS + 1))
}

for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || { echo "skip: $f not found"; continue; }
  echo "→ $f"

  # Rule 1: orphan [@key] not in references.bib
  if [[ -n "$DEFINED_KEYS" ]]; then
    while IFS=: read -r lineno keymatch; do
      key=$(echo "$keymatch" | sed -E 's/.*\[@([a-zA-Z0-9_-]+)\].*/\1/')
      if ! grep -qxF "$key" <<< "$DEFINED_KEYS"; then
        report "$f" "$lineno" "ORPHAN_KEY" "@$key not in $BIB"
      fi
    done < <(grep -nEo '\[@[a-zA-Z0-9_-]+\]' "$f" || true)
  fi

  # Rule 2: italic titles in reference list (ABNT 2025 wants bold)
  awk '/^#+ *Referências|^#+ *Bibliografia/{r=1} r && /\*[^*]+\*[^*]/{print NR":"$0}' "$f" \
    | while IFS=: read -r lineno _; do
        report "$f" "$lineno" "ITALIC_REF" "italic in ref list — ABNT 2025 uses bold"
      done

  # Rule 3: URL ref missing "Acesso em:"
  while IFS=: read -r lineno content; do
    if ! grep -qE 'Acesso em:' <<< "$content"; then
      # Check surrounding 3 lines too
      ctx=$(sed -n "$((lineno - 1)),$((lineno + 3))p" "$f")
      if ! grep -qE 'Acesso em:' <<< "$ctx"; then
        report "$f" "$lineno" "MISSING_ACESSO" "URL ref sem 'Acesso em: dd mmm. aaaa'"
      fi
    fi
  done < <(grep -nE 'Disponível em:' "$f" || true)

  # Rule 4: block quote (>) paragraph missing page ref
  # Heuristic: consecutive > lines totaling >3 lines without p. \d+ in the block
  awk -v file="$f" '
    /^> / { buf = buf "\n" $0; count++; start = start ? start : NR; next }
    !/^> / {
      if (count > 3 && buf !~ /p\. [0-9]/) {
        printf "  %s:%d [QUOTE_NO_PAGE] direct quote (>3 linhas) sem p. N\n", file, start
        exit_code = 1
      }
      buf=""; count=0; start=0
    }
    END {
      if (count > 3 && buf !~ /p\. [0-9]/) {
        printf "  %s:%d [QUOTE_NO_PAGE] direct quote (>3 linhas) sem p. N\n", file, start
        exit_code = 1
      }
      exit exit_code
    }
  ' "$f" && : || ERRS=$((ERRS + 1))

  # Rule 5: malformed in-text — lowercase SURNAME in parens
  while IFS=: read -r lineno content; do
    report "$f" "$lineno" "LOWERCASE_AUTHOR" "autor em parênteses deve ser CAIXA ALTA"
  done < <(grep -nE '\([a-zà-ÿ]+, [0-9]{4}' "$f" || true)
done

echo
if [[ $ERRS -eq 0 ]]; then
  echo "abnt-precommit: ✓ clean (${#FILES[@]} files)"
  exit 0
else
  echo "abnt-precommit: ✗ $ERRS violations"
  echo "Hint: invoke 'abnt-checker' agent for semantic review, or fix and re-run."
  exit 1
fi
