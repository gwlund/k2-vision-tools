# Zotero CLI

Python CLI scripts for read and write operations to Zotero libraries via the Zotero Web API.

## Overview

These scripts enable Claude Code to browse collections, search items, and manage your Zotero library during research workflows. Includes both read operations (list, search, view) and write operations (create, import, update).

## Quick Start

### 1. Setup

Requires Python 3.13+ and uv package manager.

```bash
cd scripts/zotero-cli

# Install dependencies with uv
uv sync

# Verify setup
uv run bin/zotero-verify-api
```

### 2. Development

All scripts run via `uv run` from the project directory:

```bash
cd scripts/zotero-cli
uv run bin/zotero-import-doi 10.1234/example --tags "test"
```

### 3. Deployment

Install to `~/.local/bin` for global access:

```bash
cd scripts/zotero-cli
./install.sh
```

After installation, scripts are globally available:

```bash
zotero-verify-api
zotero-import-doi 10.1234/example --tags "test"
```

## Prerequisites

### Environment Variables

Set in `~/.zshrc` or `~/.bash_profile`:

```bash
export ZOTERO_API_KEY=your_api_key_here
export ZOTERO_USER_ID=your_user_id_here
```

Get credentials at: https://www.zotero.org/settings/keys

### PATH Configuration

After running `install.sh`, ensure `~/.local/bin` is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Read Operations

### zotero-list-collections

List all collections with tree or table view.

```bash
# Tree view (default)
uv run bin/zotero-list-collections

# Table view
uv run bin/zotero-list-collections --format table

# Keys only (for scripting)
uv run bin/zotero-list-collections --keys-only
```

### zotero-search-items

Search library for items.

```bash
# Search with query
uv run bin/zotero-search-items "climate change"

# List all items
uv run bin/zotero-search-items

# Search within collection
uv run bin/zotero-search-items "policy" --collection "Research"

# Recursive search through subcollections
uv run bin/zotero-search-items "policy" --collection "Research" --recursive

# Full details
uv run bin/zotero-search-items "test" --full
```

### zotero-get-item

Get detailed information about a specific item. Automatically includes Better BibTeX citation key if available.

```bash
# Display format (includes citation key)
uv run bin/zotero-get-item ITEM_KEY

# Table format
uv run bin/zotero-get-item ITEM_KEY --format table

# JSON format
uv run bin/zotero-get-item ITEM_KEY --format json
```

### zotero-get-citekey

Get Better BibTeX citation key for a specific item.

```bash
# Get citation key (text output for scripting)
uv run bin/zotero-get-citekey ITEM_KEY

# JSON format with metadata
uv run bin/zotero-get-citekey ITEM_KEY --format json
```

**Note:** Requires Better BibTeX installed in Zotero desktop. Falls back to parsing citation keys from the `extra` field if Better BibTeX is not available.

### zotero-list-tags

List all tags in library.

```bash
# List all tags
uv run bin/zotero-list-tags

# Tags from collection
uv run bin/zotero-list-tags --collection "Research"

# Filter by usage
uv run bin/zotero-list-tags --min-count 5

# Names only
uv run bin/zotero-list-tags --names-only
```

### zotero-get-collection-items

List items in a specific collection. Optionally include Better BibTeX citation keys.

```bash
# Table view
uv run bin/zotero-get-collection-items "Research Papers"

# Include citation keys (adds citation key column)
uv run bin/zotero-get-collection-items "Research Papers" --include-citekey

# Full details with citation keys
uv run bin/zotero-get-collection-items "Research Papers" --format full --include-citekey

# Count only
uv run bin/zotero-get-collection-items "Research Papers" --count
```

## Write Operations

### zotero-verify-api

Verify API credentials and test connection.

```bash
uv run bin/zotero-verify-api
```

### zotero-create-collection

Create new collection or subcollection.

```bash
# Top-level collection
uv run bin/zotero-create-collection "My Research Project"

# Subcollection
uv run bin/zotero-create-collection "Chapter 1" --parent "My Research Project"
```

### zotero-add-item

Add item with full metadata. Includes automatic duplicate detection.

```bash
# Add item (checks for duplicates by DOI or title)
uv run bin/zotero-add-item --type journalArticle \
  --title "Paper Title" \
  --authors "Smith, John; Doe, Jane" \
  --year 2024 \
  --publication "Nature" \
  --doi "10.1234/example" \
  --collection "My Project" \
  --tags "climate,policy"

# Force adding even if duplicate exists
uv run bin/zotero-add-item --type book \
  --title "Existing Book" \
  --authors "Doe, Jane" \
  --year 2024 \
  --force
```

**Duplicate Detection:**
- Automatically checks for duplicates before adding
- First checks by DOI if provided
- Falls back to exact title match (case-insensitive)
- Shows existing item details and exits with error
- Use `--force` flag to bypass duplicate checking

Supported types: `journalArticle`, `book`, `webpage`, `report`, `conferencePaper`

### zotero-import-doi

Import from DOI with automatic metadata fetch.

```bash
uv run bin/zotero-import-doi 10.1234/example --collection "Papers" --tags "to-read"
```

### zotero-add-tags

Add tags to existing item.

```bash
uv run bin/zotero-add-tags ITEM_KEY important reviewed to-cite
```

### zotero-update-item

Update item metadata with extensive field support.

```bash
# Basic fields
uv run bin/zotero-update-item ITEM_KEY --title "New Title" --year 2025

# Authors/creators (semicolon-separated)
uv run bin/zotero-update-item ITEM_KEY --author "Smith, John; Doe, Jane"
uv run bin/zotero-update-item ITEM_KEY --author "World Health Organization"

# Report-specific fields
uv run bin/zotero-update-item ITEM_KEY --institution "WHO" --place "Geneva" --report-type "Technical Report"

# Book fields
uv run bin/zotero-update-item ITEM_KEY --publisher "MIT Press" --place "Cambridge, MA" --series "AI Series"
```

**Supported Fields:**
- `--title` - Item title
- `--year` - Publication year
- `--author` / `--creator` - Authors (semicolon-separated)
- `--abstract` - Abstract text
- `--url` - URL
- `--doi` - DOI
- `--publication` - Journal/publication name
- `--institution` - Institution (reports)
- `--report-type` - Type of report
- `--place` - Publication place/location
- `--publisher` - Publisher name
- `--series` - Series name

**Author Format:**
- Individual: "Lastname, Firstname" or "Firstname Lastname"
- Organizational: "Organization Name" (no comma)
- Multiple: Separate with semicolons

### zotero-create-parent

Create parent bibliographic item for standalone PDF attachments. Equivalent to Zotero GUI's "Create Parent Item" feature.

```bash
# Interactive mode for single PDF
uv run bin/zotero-create-parent ABC123

# Non-interactive with metadata
uv run bin/zotero-create-parent ABC123 \
  --title "Climate Report 2024" \
  --author "IPCC" \
  --year 2024 \
  --institution "United Nations"

# Batch mode - process all standalone PDFs
uv run bin/zotero-create-parent --batch
```

**Options:**
- `--item-type` - Parent item type (default: report)
- `--title` - Item title
- `--author` - Authors (semicolon-separated)
- `--year` - Publication year
- `--institution` - Institution
- `--place` - Publication place
- `--batch` - Process all standalone PDFs interactively

**Behavior:**
1. Creates new bibliographic entry with specified metadata
2. Links existing PDF as child attachment
3. Preserves PDF file and any existing PDF annotations
4. PDF title is used as default for parent title

## Collection Management

### zotero-rename-collection

Rename a collection.

```bash
# By name
uv run bin/zotero-rename-collection "Old Name" "New Name"

# By key
uv run bin/zotero-rename-collection ABC123 "New Name"

# By path
uv run bin/zotero-rename-collection "Research/Papers" "Articles"
```

### zotero-move-collection

Move a collection to a different parent or to top level.

```bash
# Move to different parent
uv run bin/zotero-move-collection "Chapter 1" --parent "Dissertation"

# Move to top level
uv run bin/zotero-move-collection "Temp Collection"

# Using paths
uv run bin/zotero-move-collection "Research/Old Papers" --parent "Archive"
```

### zotero-delete-collection

Delete a collection and all its subcollections (items are preserved).

```bash
# Delete with confirmation
uv run bin/zotero-delete-collection "Old Project"

# Delete without confirmation
uv run bin/zotero-delete-collection "Old Project" --force

# Using path
uv run bin/zotero-delete-collection "Research/Archived" --force
```

**Note:** Deleting a collection removes all subcollections recursively but preserves items in your library.

## PDF Management & Annotations

Complete workflow for managing PDFs, creating annotations via LLM analysis, and exporting to Obsidian.

### ⚠️ CRITICAL: Annotations Are Invisible in Zotero

**Annotations created by these tools are COMPLETELY INVISIBLE in all Zotero interfaces.**

They will:
- ✅ Export to markdown/JSON via API with all text, comments, and page numbers
- ✅ Work in API-based search and retrieval
- ✅ Generate notes via API
- ❌ **NOT appear in Zotero Desktop app**
- ❌ **NOT appear in Zotero PDF reader**
- ❌ **NOT appear in Zotero Web interface**
- ❌ **NOT be visible in any Zotero UI**

**Use Case:** These tools are for **immediate export workflows** - create annotations via API and immediately export to Obsidian/markdown. Do NOT expect to view them in Zotero.

For annotations visible in Zotero, create them manually in Zotero's PDF reader. See:
- `ANNOTATION_LIMITATIONS.md` for technical details
- `docs/API-ANNOTATION-AREA-ISSUE.md` for investigation of the display issue

### zotero-export-annotations

Export annotations to Obsidian-compatible markdown.

```bash
# Export single item
zotero-export-annotations ITEM_KEY --output notes/research.md

# Export with template
zotero-export-annotations ITEM_KEY \
  --output notes/ceds-report.md \
  --template lib/templates/obsidian-ceds.md

# Export entire collection
zotero-export-annotations --collection "CEDS Reports" \
  --output-dir notes/

# Export annotations by tag (cross-document)
zotero-export-annotations --tag "tourism" \
  --output notes/tourism-themes.md

# Filter exported annotations by tag
zotero-export-annotations ITEM_KEY \
  --output notes/reviewed.md \
  --tag-filter "reviewed"
```

**Output format:**
- YAML frontmatter (title, creator, date, tags, zotero_key)
- Zotero deep links (`zotero://select/items/ITEM_KEY`)
- Annotations grouped by page
- Highlighted text in blockquotes
- Comments in italics

### zotero-search-annotations

Full-text search across all annotations.

```bash
# Search all annotations
zotero-search-annotations "manufacturing"

# Search within collection
zotero-search-annotations "population data" --collection "CEDS Reports"

# Search with tag filter
zotero-search-annotations "tourism" --tag "reviewed"

# JSON output for scripting
zotero-search-annotations "economic development" --format json

# Show context around matches
zotero-search-annotations "strategies" --context 2
```

### zotero-create-note-from-annotations

Create Zotero note from filtered annotations.

```bash
# Create note from all annotations
zotero-create-note-from-annotations ITEM_KEY

# Create note from reviewed annotations only
zotero-create-note-from-annotations ITEM_KEY --tag-filter "reviewed"

# Custom note title
zotero-create-note-from-annotations ITEM_KEY --title "Research Summary"
```

**Note:** Mimics Zotero's native "Create Note from Annotations" feature.

### zotero-analyze-pdf

Analyze PDF with LLM and create highlights (requires API key).

```bash
# Quick analysis with topics
zotero-analyze-pdf ITEM_KEY --topics "tourism,manufacturing,population"

# Deep analysis with research context
zotero-analyze-pdf ITEM_KEY --mode deep \
  --context "Find demographic data and economic strategies for mid-size regions"

# Specify LLM provider
zotero-analyze-pdf ITEM_KEY --topics "economic" --llm claude

# Dry run (show what would be highlighted)
zotero-analyze-pdf ITEM_KEY --topics "tourism" --dry-run

# Custom tag for highlights
zotero-analyze-pdf ITEM_KEY --topics "manufacturing" --tag "ai-generated"
```

**Requirements:**
- `ANTHROPIC_API_KEY` environment variable (for Claude)
- OR `OPENAI_API_KEY` (for GPT-4)
- OR Ollama running locally (for open models)

**LLM providers:**
- `claude` - Anthropic Claude (default, most accurate)
- `openai` - OpenAI GPT-4
- `ollama` - Local Ollama models

### Complete Workflow Example

```bash
# 1. Export annotations to Obsidian
zotero-export-annotations ABC123 \
  --output ~/Documents/Obsidian/Research/Portland-CEDS.md \
  --template lib/templates/obsidian-ceds.md

# 2. Search for specific themes across collection
zotero-search-annotations "manufacturing" \
  --collection "CEDS Reports" \
  --format json > manufacturing-refs.json

# 3. Create summary note from reviewed annotations
zotero-create-note-from-annotations ABC123 \
  --tag-filter "reviewed" \
  --title "Key Findings: Portland CEDS"

# 4. Analyze new PDF for tourism content
zotero-analyze-pdf XYZ789 \
  --topics "tourism,hospitality,visitor economy" \
  --tag "tourism-analysis"
```

### Templates

Obsidian templates in `lib/templates/`:
- `obsidian-ceds.md` - For CEDS reports with structured sections

Create custom templates with variables:
- `{{title}}` - Item title
- `{{creator}}` - Creator/organization
- `{{date}}` - Publication date
- `{{place}}` - Location
- `{{tags}}` - Comma-separated tags
- `{{zotero_key}}` - Item key for deep links
- `{{annotations}}` - Formatted annotations

See `lib/templates/obsidian-ceds.md` for example structure.

## Testing

Run integration tests:

```bash
cd scripts/zotero-cli
./tests/test-integration.sh
```

Clean up test items in Zotero desktop after testing.

## Better BibTeX Integration

This CLI includes support for Better BibTeX citation keys, enabling dual-linking workflows for academic writing with Obsidian + Pandoc.

### Requirements

- **Zotero Desktop** with **Better BibTeX plugin** installed and running
- Better BibTeX JSON-RPC API enabled (default: `http://127.0.0.1:23119`)

### Features

1. **Automatic Citation Key Display**: `zotero-get-item` shows citation keys automatically
2. **Collection Export with Keys**: `--include-citekey` flag adds citation key column
3. **Dedicated Citation Key Lookup**: `zotero-get-citekey` for scripting workflows
4. **Fallback Support**: Parses citation keys from `extra` field if Better BibTeX unavailable

### Citation Key Fallback

If Better BibTeX is not running, the CLI will attempt to parse citation keys from the Zotero item's `extra` field. Supported patterns:

```
Citation Key: meadowsLeveragePointsPlaces1997
bibtex: meadowsLeveragePointsPlaces1997
tex.citationkey: meadowsLeveragePointsPlaces1997
```

### Example Workflow: Dual Linking

Generate markdown with both Zotero URIs and @citekey references:

```bash
# Get items with citation keys
uv run bin/zotero-get-collection-items "My Research" --include-citekey --format full

# Get just the citation key for scripting
CITEKEY=$(uv run bin/zotero-get-citekey ANJNQC8P)
echo "Citation: @$CITEKEY"
echo "Zotero Link: zotero://select/items/@ANJNQC8P"
```

**Output:**
```
Citation: @meadowsLeveragePointsPlaces1997
Zotero Link: zotero://select/items/@ANJNQC8P
```

This enables:
- **Pandoc citations**: Use `@meadowsLeveragePointsPlaces1997` in markdown
- **Zotero deep links**: Click `zotero://select/items/@ANJNQC8P` to open in Zotero
- **Stable references**: Both identifiers remain valid even if item metadata changes

### Use Cases

- **Literature Notes**: Auto-populate Obsidian templates with both link types
- **Bibliography Validation**: Verify all @citekeys in documents exist in Zotero
- **Citation Mapping**: Generate lookup tables for cross-referencing
- **Batch Processing**: Export collections with citation keys for analysis

### Example Scripts

See `examples/citation-key-examples.sh` for complete working examples including:

- Single citation key lookup
- JSON format parsing
- Generating markdown literature notes with dual linking
- Batch exporting collections to CSV with citation keys
- Integration with Obsidian and Pandoc workflows

Run examples: `./examples/citation-key-examples.sh`

### Better BibTeX Resources

- **Plugin**: https://retorque.re/zotero-better-bibtex/
- **Citation Key Patterns**: https://retorque.re/zotero-better-bibtex/citing/
- **JSON-RPC API**: https://retorque.re/zotero-better-bibtex/exporting/json-rpc/

## Duplicate Detection & Management

This CLI includes comprehensive duplicate detection, prevention, and cleanup tools to maintain a clean Zotero library.

### Features

1. **Duplicate Prevention**: All write commands check for duplicates before adding
   - `zotero-add-item`: Checks by DOI or exact title match
   - `zotero-import-doi`: Checks by DOI with interactive options
2. **DOI Lookup**: Quick search to find items by DOI
3. **Duplicate Detection**: Scan library for items with duplicate DOIs
4. **Smart Merging**: Intelligently merge duplicates while preserving all data

### DOI Lookup

Find items in your library by DOI:

```bash
# Quick lookup (returns item key)
uv run bin/zotero-find-by-doi 10.1234/example

# With details
uv run bin/zotero-find-by-doi 10.1234/example --show-details

# JSON format for scripting
uv run bin/zotero-find-by-doi 10.1234/example --format json
```

**Search scope**: Checks DOI field, URL field, and Extra field

### Duplicate Prevention

The enhanced `zotero-import-doi` command now checks for duplicates before importing:

```bash
# Interactive mode (prompts if duplicate found)
uv run bin/zotero-import-doi 10.1234/example --collection "Research"

# Skip if exists (returns existing item key)
uv run bin/zotero-import-doi 10.1234/example --skip-existing

# Update existing item's metadata
uv run bin/zotero-import-doi 10.1234/example --update-existing

# Add to collection even if exists
uv run bin/zotero-import-doi 10.1234/example --collection "New Project" --add-to-collection
```

**Interactive options when duplicate found:**
1. Skip import (use existing item)
2. Update metadata from CrossRef
3. Add to specified collection
4. Cancel operation

### Finding Existing Duplicates

Scan your library for items with duplicate DOIs:

```bash
# Find all duplicates
uv run bin/zotero-find-duplicates

# JSON output
uv run bin/zotero-find-duplicates --format json
```

**Output includes**:
- DOI for each duplicate group
- Item details (title, authors, year)
- Collections and tags
- Citation keys
- Quality scores

### Merging Duplicates

Interactively resolve duplicates with smart merging:

```bash
# Interactive merge
uv run bin/zotero-merge-duplicates

# Preview without making changes
uv run bin/zotero-merge-duplicates --dry-run

# Auto-merge with smart defaults
uv run bin/zotero-merge-duplicates --auto
```

**Merge behavior:**
- **Primary item**: Kept with original metadata
- **Secondary items**: Collections, tags, and notes merged into primary
- **Citation keys**: User chooses which to keep when conflicts exist
- **Deletion**: Secondary items deleted after successful merge
- **Quality scoring**: Recommends best item to keep based on:
  - Has Better BibTeX citation key
  - More collections and tags
  - More complete metadata
  - Has notes or attachments

### Manual Deletion

Delete items from library:

```bash
# Delete single item
uv run bin/zotero-delete-item ABC123

# Delete multiple items
uv run bin/zotero-delete-item ABC123 XYZ789

# Force delete without confirmation
uv run bin/zotero-delete-item ABC123 --force
```

### Complete Workflow Examples

#### Scenario 1: Manual Entry with Duplicate Prevention

```bash
# Add item manually - checks for duplicates automatically
uv run bin/zotero-add-item --type journalArticle \
  --title "Climate Adaptation Strategies" \
  --authors "Smith, John; Doe, Jane" \
  --year 2024 \
  --doi "10.1234/example" \
  --collection "Research Papers"

# If duplicate exists, you'll see:
# ⚠ Duplicate item found
# Title: Climate Adaptation Strategies
# Authors: Smith, John; Doe, Jane
# Year: 2024
# Item key: ABC123
# ✗ Item already exists. Use --force to add anyway.

# Force adding if you really need the duplicate
uv run bin/zotero-add-item --type journalArticle \
  --title "Climate Adaptation Strategies" \
  --authors "Smith, John; Doe, Jane" \
  --year 2024 \
  --force
```

#### Scenario 2: DOI Import with Duplicate Prevention

```bash
# Import DOI - automatically checks for duplicates
uv run bin/zotero-import-doi 10.1038/nature12345 --collection "Climate Research"

# If duplicate exists, you'll be prompted:
# [1] Skip import (use existing item)
# [2] Update metadata from CrossRef
# [3] Add to collection "Climate Research"
# [4] Cancel operation
```

#### Scenario 3: Check Before Import

```bash
# Check if you already have this paper
ITEM_KEY=$(uv run bin/zotero-find-by-doi 10.1038/nature12345 2>/dev/null)

if [ $? -eq 0 ]; then
  echo "Already in library: $ITEM_KEY"
  # Add to new collection
  uv run bin/zotero-import-doi 10.1038/nature12345 --collection "New Project" --add-to-collection
else
  echo "Not found - importing..."
  uv run bin/zotero-import-doi 10.1038/nature12345 --collection "New Project" --tags "to-read"
fi
```

#### Scenario 4: Clean Up Existing Duplicates

```bash
# Step 1: Find duplicates
uv run bin/zotero-find-duplicates

# Step 2: Preview merge (no changes)
uv run bin/zotero-merge-duplicates --dry-run

# Step 3: Interactively merge
uv run bin/zotero-merge-duplicates
```

#### Scenario 5: Bulk Import with Safety

```bash
# Import list of DOIs without creating duplicates
while read doi; do
  echo "Processing: $doi"
  uv run bin/zotero-import-doi "$doi" --skip-existing --collection "Bulk Import" --tags "bulk"
done < dois.txt
```

### New Commands Summary

| Command | Purpose |
|---------|---------|
| `zotero-find-by-doi` | Search library for specific DOI |
| `zotero-import-doi` (enhanced) | Import with duplicate detection |
| `zotero-find-duplicates` | Scan library for all duplicates |
| `zotero-merge-duplicates` | Interactively merge duplicates |
| `zotero-delete-item` | Delete items from library |

## Project Structure

```
scripts/zotero-cli/
├── bin/                              # Executable scripts
│   # Read operations
│   ├── zotero-list-collections       # Browse collection hierarchy
│   ├── zotero-search-items           # Search and list items (--recursive)
│   ├── zotero-get-item               # View detailed item info (includes citation key)
│   ├── zotero-get-citekey            # Get Better BibTeX citation key
│   ├── zotero-list-tags              # List and filter tags
│   ├── zotero-get-collection-items   # View collection contents (--include-citekey)
│   ├── zotero-find-by-doi            # Find item by DOI
│   # Write operations
│   ├── zotero-verify-api             # Test API credentials
│   ├── zotero-create-collection      # Create collections
│   ├── zotero-add-item               # Add items manually
│   ├── zotero-import-doi             # Import from DOI (with duplicate detection)
│   ├── zotero-add-tags               # Add tags to items
│   ├── zotero-update-item            # Update item metadata (extended fields)
│   ├── zotero-create-parent          # Create parent for standalone PDFs
│   # Collection management
│   ├── zotero-rename-collection      # Rename collections
│   ├── zotero-move-collection        # Move collections to different parents
│   ├── zotero-delete-collection      # Delete collections and subcollections
│   # Duplicate management
│   ├── zotero-find-duplicates        # Find DOI-based duplicates
│   ├── zotero-merge-duplicates       # Interactively merge duplicates
│   └── zotero-delete-item            # Delete items from library
├── lib/                              # Shared library
│   ├── zotero_api.py                 # API wrapper
│   ├── parsers.py                    # Parsing utilities (includes creator parsing)
│   ├── validation.py                 # Metadata validation utilities
│   └── templates.py                  # Item templates
├── tests/                            # Integration tests
│   └── test-integration.sh
├── install.sh                        # Deployment script
├── pyproject.toml                    # uv project config
└── README.md                         # This file
```

## Claude Code Integration

When using with Claude Code, scripts are called via Bash tool:

**User**: "Add this paper to my library: DOI 10.1234/example, tags climate"

**Claude**: Runs `zotero-import-doi 10.1234/example --tags "climate"` and confirms addition

## Troubleshooting

### "ZOTERO_API_KEY not found"

Add to `~/.zshrc` and run `source ~/.zshrc`

### "command not found: zotero-*"

Either:
1. Run via `uv run bin/script-name` from project directory
2. Run `./install.sh` to deploy globally

### DOI import fails

- Check DOI validity
- Verify network connection
- May be rate limited by CrossRef API

## References

- **Zotero Web API**: https://www.zotero.org/support/dev/web_api/v3/start
- **pyzotero**: https://pyzotero.readthedocs.io/
- **CrossRef API**: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

## License

MIT

## Roadmap / Future Features

### Completed Enhancements

- [x] **Create Parent Item**: Convert standalone PDF attachments to proper bibliographic entries with parent-child relationship
  - ✅ Equivalent to Zotero GUI's "Create Parent Item" feature
  - ✅ Automatically link PDF as child attachment
  - ✅ Support for manual metadata entry and automatic retrieval
  - ✅ Batch processing for multiple standalone PDFs
  - Released: v1.4.0

- [x] **Extend zotero-update-item fields**: Add support for additional metadata fields
  - ✅ `--author` / `--creator` (handle both individual and organizational authors)
  - ✅ `--report-type` (for report items)
  - ✅ `--institution` (for reports and institutional documents)
  - ✅ `--place` (location/geographic metadata)
  - ✅ `--publisher` (enhance existing support)
  - ✅ `--series` (for book series and report series)
  - ✅ Item-type specific field validation
  - Released: v1.4.0

- [x] **Duplicate detection for zotero-add-item**: Prevent accidental duplicate entries
  - ✅ Automatic duplicate checking by DOI (if provided)
  - ✅ Fallback to exact title match (case-insensitive)
  - ✅ Informative error messages showing existing item details
  - ✅ `--force` flag to bypass duplicate checking when needed
  - ✅ Comprehensive test suite (7 new tests)
  - Released: v1.4.1

### Planned Enhancements

(No current planned features)

### Feature Requests

Submit feature requests at: https://github.com/gwlund/000-Claude-Code-Templates/issues

## Version

1.4.1 - Duplicate detection for zotero-add-item (2025-11-23)
1.4.0 - Extended metadata and create parent item (2025-11-18)
1.3.0 - DOI-based duplicate management (2025-11-15)
1.2.0 - Nested subcollections CRUD and recursive search (2025-11-14)
1.1.0 - Better BibTeX citation key integration (2025-11-14)
1.0.0 - Initial release (2025-11-11)
