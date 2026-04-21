#!/usr/bin/env bash
# vault-lint.sh — Obsidian vault health checker for obsidian-vault-keeper
# Usage: vault-lint.sh [--quiet] [--json] [vault-path]
# Compatible with bash 3.2+ (macOS default)

set -uo pipefail

# ─── Defaults ────────────────────────────────────────────────────────────────
QUIET=false
JSON=false
VAULT_PATH=""

# ─── Argument Parsing ─────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --quiet) QUIET=true ;;
    --json)  JSON=true  ;;
    -*)      echo "Unknown flag: $arg" >&2; exit 2 ;;
    *)       VAULT_PATH="$arg" ;;
  esac
done

VAULT_PATH="${VAULT_PATH:-.}"
VAULT_PATH="$(cd "$VAULT_PATH" 2>/dev/null && pwd)" || { echo "ERROR: Vault path not found: $VAULT_PATH" >&2; exit 2; }

# ─── Content Directories ─────────────────────────────────────────────────────
# Using parallel arrays (bash 3.2 compatible — no declare -A)
CONTENT_DIRS=(entities concepts sources synthesis events)

# Required fields per directory (space-separated, matching CONTENT_DIRS order)
DIR_FIELDS_entities="type title created updated"
DIR_FIELDS_concepts="type title created updated"
DIR_FIELDS_sources="type title source_file date_ingested created updated"
DIR_FIELDS_synthesis="type title synthesis_type created updated"
DIR_FIELDS_events="type title event_date event_type created updated"

MOC_NAME_entities="Entities MOC.md"
MOC_NAME_concepts="Concepts MOC.md"
MOC_NAME_sources="Sources MOC.md"
MOC_NAME_synthesis="Synthesis MOC.md"
MOC_NAME_events="Events MOC.md"

get_dir_fields() {
  local dir="$1"
  case "$dir" in
    entities)  echo "$DIR_FIELDS_entities" ;;
    concepts)  echo "$DIR_FIELDS_concepts" ;;
    sources)   echo "$DIR_FIELDS_sources" ;;
    synthesis) echo "$DIR_FIELDS_synthesis" ;;
    events)    echo "$DIR_FIELDS_events" ;;
    *)         echo "" ;;
  esac
}

get_moc_name() {
  local dir="$1"
  case "$dir" in
    entities)  echo "$MOC_NAME_entities" ;;
    concepts)  echo "$MOC_NAME_concepts" ;;
    sources)   echo "$MOC_NAME_sources" ;;
    synthesis) echo "$MOC_NAME_synthesis" ;;
    events)    echo "$MOC_NAME_events" ;;
    *)         echo "" ;;
  esac
}

# ─── Counters ─────────────────────────────────────────────────────────────────
fm_pass=0
fm_fail=0
orphan_count=0
broken_count=0
index_gap_count=0
missing_moc_count=0
total_pages=0

# ─── Output Buffers (newline-delimited strings) ────────────────────────────────
fm_out=""
orphan_out=""
broken_out=""
index_out=""
moc_out=""

append_line() {
  # append_line varname "text"
  local var="$1"
  local text="$2"
  eval "${var}=\"\${${var}}\${${var}:+$'\n'}${text}\""
}

# ─── Helper: is a file a MOC or index? ───────────────────────────────────────
is_navigation_file() {
  local filename
  filename="$(basename "$1")"
  [[ "$filename" == "index.md" ]] && return 0
  [[ "$filename" == *" MOC.md" ]] && return 0
  return 1
}

# ─── Helper: check frontmatter presence and required fields ──────────────────
check_frontmatter() {
  local file="$1"
  local dir="$2"
  local rel="${file#"$VAULT_PATH/"}"

  local first_line
  first_line="$(head -1 "$file" 2>/dev/null)"
  if [[ "$first_line" != "---" ]]; then
    append_line fm_out "✗ $rel: missing frontmatter"
    fm_fail=$(( fm_fail + 1 ))
    return
  fi

  # Extract frontmatter block (lines between first --- and second ---)
  local fm_block
  fm_block="$(awk '/^---/{if(found){exit}else{found=1;next}} found{print}' "$file")"

  local required
  required="$(get_dir_fields "$dir")"
  local file_ok=true

  for field in $required; do
    if ! echo "$fm_block" | grep -qE "^${field}[[:space:]]*:"; then
      append_line fm_out "✗ $rel: missing field '${field}'"
      fm_fail=$(( fm_fail + 1 ))
      file_ok=false
    fi
  done

  if $file_ok; then
    append_line fm_out "✓ $rel"
    fm_pass=$(( fm_pass + 1 ))
  fi
}

# ─── Check 1: Frontmatter ─────────────────────────────────────────────────────
for dir in "${CONTENT_DIRS[@]}"; do
  dir_path="$VAULT_PATH/$dir"
  [[ -d "$dir_path" ]] || continue
  while IFS= read -r -d '' file; do
    total_pages=$(( total_pages + 1 ))
    check_frontmatter "$file" "$dir"
  done < <(find "$dir_path" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
done

# ─── Check 2: Orphan Pages ────────────────────────────────────────────────────
all_links_tmp="$(mktemp)"

# Collect all [[...]] link targets (stripping aliases and anchors)
find "$VAULT_PATH" -name "*.md" -print0 2>/dev/null | \
  xargs -0 grep -ohE '\[\[[^\]]+\]\]' 2>/dev/null | \
  sed 's/^\[\[//;s/\]\]$//' | \
  sed 's/|.*//' | \
  sed 's/#.*//' | \
  sort -u > "$all_links_tmp" || true

for dir in "${CONTENT_DIRS[@]}"; do
  dir_path="$VAULT_PATH/$dir"
  [[ -d "$dir_path" ]] || continue
  while IFS= read -r -d '' file; do
    is_navigation_file "$file" && continue
    local_name="$(basename "$file" .md)"
    if ! grep -qxF "$local_name" "$all_links_tmp" 2>/dev/null; then
      rel="${file#"$VAULT_PATH/"}"
      append_line orphan_out "! $rel: no inbound links"
      orphan_count=$(( orphan_count + 1 ))
    fi
  done < <(find "$dir_path" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
done

# ─── Check 3: Broken Wikilinks ────────────────────────────────────────────────
all_pages_tmp="$(mktemp)"

find "$VAULT_PATH" -name "*.md" -print0 2>/dev/null | \
  xargs -0 -I{} basename {} .md 2>/dev/null | \
  sort -u > "$all_pages_tmp" || true

# Cleanup temp files on exit
trap 'rm -f "$all_links_tmp" "$all_pages_tmp"' EXIT

while IFS= read -r -d '' file; do
  rel="${file#"$VAULT_PATH/"}"
  line_num=0
  while IFS= read -r line; do
    line_num=$(( line_num + 1 ))
    # Extract [[...]] wikilinks from this line
    extracted="$(echo "$line" | grep -ohE '\[\[[^\]]+\]\]' | sed 's/^\[\[//;s/\]\]$//' 2>/dev/null || true)"
    [[ -z "$extracted" ]] && continue
    while IFS= read -r link; do
      [[ -z "$link" ]] && continue
      target="$(echo "$link" | sed 's/|.*//;s/#.*//')"
      [[ -z "$target" ]] && continue
      if ! grep -qxF "$target" "$all_pages_tmp" 2>/dev/null; then
        append_line broken_out "! $rel:${line_num}: broken link [[$link]]"
        broken_count=$(( broken_count + 1 ))
      fi
    done <<< "$extracted"
  done < "$file"
done < <(find "$VAULT_PATH" -name "*.md" -print0 2>/dev/null)

# ─── Check 4: Index Completeness ─────────────────────────────────────────────
index_file="$VAULT_PATH/index.md"
if [[ -f "$index_file" ]]; then
  for dir in "${CONTENT_DIRS[@]}"; do
    dir_path="$VAULT_PATH/$dir"
    [[ -d "$dir_path" ]] || continue
    while IFS= read -r -d '' file; do
      is_navigation_file "$file" && continue
      local_name="$(basename "$file" .md)"
      rel="${file#"$VAULT_PATH/"}"
      if ! grep -qF "[[$local_name]]" "$index_file" 2>/dev/null && \
         ! grep -qF "[[$local_name|" "$index_file" 2>/dev/null; then
        append_line index_out "! $rel: not in index.md"
        index_gap_count=$(( index_gap_count + 1 ))
      fi
    done < <(find "$dir_path" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
  done
else
  append_line index_out "✗ index.md: file not found"
  index_gap_count=$(( index_gap_count + 1 ))
fi

# ─── Check 5: MOC Existence ──────────────────────────────────────────────────
for dir in "${CONTENT_DIRS[@]}"; do
  moc_name="$(get_moc_name "$dir")"
  moc_file="$VAULT_PATH/$dir/$moc_name"
  if [[ -f "$moc_file" ]]; then
    append_line moc_out "✓ $dir/$moc_name exists"
  else
    append_line moc_out "✗ $dir/$moc_name: missing"
    missing_moc_count=$(( missing_moc_count + 1 ))
  fi
done

# ─── Totals ───────────────────────────────────────────────────────────────────
total_issues=$(( fm_fail + orphan_count + broken_count + index_gap_count + missing_moc_count ))
exit_code=0
[ "$total_issues" -gt 0 ] && exit_code=1

# ─── JSON Output ──────────────────────────────────────────────────────────────
if $JSON; then
  printf '{\n'
  printf '  "vault": "%s",\n' "$VAULT_PATH"
  printf '  "date": "%s",\n' "$(date +%Y-%m-%d)"
  printf '  "summary": {\n'
  printf '    "total_pages": %d,\n' "$total_pages"
  printf '    "total_issues": %d,\n' "$total_issues"
  printf '    "frontmatter_failures": %d,\n' "$fm_fail"
  printf '    "orphans": %d,\n' "$orphan_count"
  printf '    "broken_links": %d,\n' "$broken_count"
  printf '    "index_gaps": %d,\n' "$index_gap_count"
  printf '    "missing_mocs": %d\n' "$missing_moc_count"
  printf '  },\n'

  emit_json_array() {
    local label="$1"
    local content="$2"
    printf '  "%s": [\n' "$label"
    if [[ -z "$content" ]]; then
      printf '  ]'
      return
    fi
    local first=true
    while IFS= read -r item; do
      escaped="${item//\\/\\\\}"
      escaped="${escaped//\"/\\\"}"
      if $first; then
        first=false
      else
        printf ',\n'
      fi
      printf '    "%s"' "$escaped"
    done <<< "$content"
    printf '\n  ]'
  }

  emit_json_array "frontmatter" "$fm_out"; printf ',\n'
  emit_json_array "orphans" "$orphan_out"; printf ',\n'
  emit_json_array "broken_links" "$broken_out"; printf ',\n'
  emit_json_array "index_gaps" "$index_out"; printf ',\n'
  emit_json_array "moc_checks" "$moc_out"; printf '\n'
  printf '}\n'
  exit $exit_code
fi

# ─── Human-Readable Output ────────────────────────────────────────────────────
if ! $QUIET; then
  echo "=== Vault Lint Report ==="
  echo "Vault: $VAULT_PATH"
  echo "Date:  $(date +%Y-%m-%d)"
  echo ""

  echo "--- Frontmatter Checks ---"
  if [[ -z "$fm_out" ]]; then
    echo "(no content pages found)"
  else
    echo "$fm_out"
  fi
  echo ""

  echo "--- Orphan Pages ---"
  if [[ -z "$orphan_out" ]]; then
    echo "(none)"
  else
    echo "$orphan_out"
  fi
  echo ""

  echo "--- Broken Wikilinks ---"
  if [[ -z "$broken_out" ]]; then
    echo "(none)"
  else
    echo "$broken_out"
  fi
  echo ""

  echo "--- Index Completeness ---"
  if [[ -z "$index_out" ]]; then
    echo "(all pages indexed)"
  else
    echo "$index_out"
  fi
  echo ""

  echo "--- MOC Check ---"
  if [[ -z "$moc_out" ]]; then
    echo "(no content directories found)"
  else
    echo "$moc_out"
  fi
  echo ""
fi

echo "=== Summary ==="
echo "Total pages:  $total_pages"
echo "Issues found: $total_issues"
echo "- Frontmatter:  $fm_fail"
echo "- Orphans:      $orphan_count"
echo "- Broken links: $broken_count"
echo "- Index gaps:   $index_gap_count"
echo "- Missing MOCs: $missing_moc_count"

exit $exit_code
