# Zotero CLI - Quick Reference

**Status:** ✅ Globally installed at `~/.local/bin/`
**Deployed:** 2026-01-27
**Full Docs:** `~/.local/lib/zotero-cli/README.md`

---

## Quick Start

```bash
# Verify credentials work
zotero-verify-api

# Import paper (most common)
zotero-import-doi 10.1234/example --collection "Research" --tags "topic"

# Search library
zotero-search-items "search term"

# List collections
zotero-list-collections
```

---

## All Available Commands

### Read Operations (Search & Browse)
- `zotero-list-collections` - Show all collections
- `zotero-search-items QUERY` - Search by title/author/keywords
- `zotero-get-item ITEMKEY` - View item details
- `zotero-get-citekey ITEMKEY` - Get Better BibTeX citation key
- `zotero-list-tags` - Browse all tags
- `zotero-get-collection-items COLLECTION` - View collection contents
- `zotero-find-by-doi DOI` - Find paper by DOI
- `zotero-export-annotations ITEMKEY` - Export paper annotations

### Write Operations (Add & Manage)
- `zotero-verify-api` - Test API credentials
- `zotero-import-doi DOI` - Add paper from DOI (RECOMMENDED)
- `zotero-add-item --type TYPE` - Manual item entry (complex)
- `zotero-add-tags ITEMKEY tag1 tag2` - Tag items
- `zotero-update-item ITEMKEY` - Update metadata
- `zotero-create-parent ITEMKEY` - Create parent for standalone PDFs
- `zotero-add-pdf ITEMKEY PATH` - Attach PDF to item

### Collection Management
- `zotero-create-collection NAME` - Create collection
- `zotero-rename-collection OLD NEW` - Rename
- `zotero-move-collection NAME --parent PARENT` - Move/nest
- `zotero-delete-collection NAME` - Delete (cascades)

### Duplicate Management
- `zotero-find-duplicates` - Find DOI-based duplicates
- `zotero-merge-duplicates` - Interactive merge
- `zotero-delete-item ITEMKEY` - Delete item

### PDF Operations
- `zotero-analyze-pdf PATH` - Extract text from PDF
- `zotero-search-annotations ITEMKEY` - Search PDF highlights
- `zotero-create-note-from-annotations ITEMKEY` - Generate note from highlights

---

## Common Workflows

### Add a Paper to Library
```bash
# 1. Find DOI (Google Scholar, ResearchGate, journal site)
# 2. Import with collection and tags
zotero-import-doi 10.1038/nature12373 \
  --collection "Manufacturing SWOT" \
  --tags "manufacturing,whatcom-county,peer-analysis"

# 3. Verify it was added
zotero-search-items "paper title"
```

### Organize Papers by Topic
```bash
# Create collections for each research phase
zotero-create-collection "Phase 1 - Research"
zotero-create-collection "Phase 2 - Analysis"
zotero-create-collection "Phase 3 - Synthesis"

# Move papers to appropriate collections
# (Note: zotero-cli doesn't have move-item command, do in Zotero desktop)
```

### Tag for Cross-Reference
```bash
# Tag paper with multiple relevant topics
zotero-add-tags ABC123XYZ manufacturing strengths-opportunities

# Search by tag later
zotero-search-items "tag:manufacturing"
```

### Extract Annotations from PDF
```bash
# Export highlights/notes from paper
zotero-export-annotations ABC123XYZ

# Or create note from annotations
zotero-create-note-from-annotations ABC123XYZ
```

### Find Duplicate Papers
```bash
# Detect duplicate entries
zotero-find-duplicates

# Merge duplicates interactively
zotero-merge-duplicates
```

---

## Syntax Reference

### Flags
- `--collection NAME` - Specify collection (creates if needed)
- `--tags "tag1,tag2"` - Comma-separated tags
- `--parent COLLECTION` - Parent for subcollections
- `--type TYPE` - Item type (journalArticle, book, webpage, etc.)

### Help
```bash
zotero-import-doi --help      # Show options for specific command
zotero-verify-api --help      # Help for any command
```

### Library Stats
```bash
zotero-verify-api            # Shows: item count, collection count
```

---

## Environment Setup

**Required for all commands:**
```bash
export ZOTERO_API_KEY="your_key_from_zotero.org/settings/keys"
export ZOTERO_USER_ID="your_numeric_user_id"
```

Add to `~/.zshrc` or `~/.bash_profile` and run `source ~/.zshrc`

**Get credentials:**
https://www.zotero.org/settings/keys → Create new API key

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "ZOTERO_API_KEY not found" | Add to `~/.zshrc` and `source ~/.zshrc` |
| "command not found: zotero-*" | Run `zotero-verify-api` to check installation, or reinstall from template project |
| DOI import fails | Verify DOI is correct, check network, may be rate limited |
| "Item not found" | Verify ITEMKEY is correct (check with `zotero-search-items`) |

---

## Integration with Citation Workflows

**For research projects using @citekey citations:**

1. Import paper → generates Zotero item key
2. Paper appears in Zotero desktop
3. Get citation key: `zotero-get-citekey ITEMKEY`
4. Use in markdown: `[@smithManufacturingTrends2024]`
5. Pandoc generates bibliography with `--citeproc`

---

## Reference

| Metric | Value |
|--------|-------|
| Installation Date | 2026-01-27 |
| Location | ~/.local/lib/zotero-cli/ |
| Commands | 23 available |
| Python Version | 3.13+ |
| Package Manager | uv |
| Full Docs | ~/.local/lib/zotero-cli/README.md |

Last updated: 2026-01-27
