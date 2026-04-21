---
name: obsidian-setup
description: Automated Obsidian vault setup with Zotero Integration for academic literature management, citation workflows, and research note-taking. Creates folder structure, installs templates, configures Zotero Web API connection, and verifies setup. Use when setting up new research projects, knowledge bases, or literature review vaults with automated citation management using Handlebars templates and Pandoc-style citations.
tags: [obsidian, zotero, research, literature-management, citation, academic, note-taking, knowledge-management, vault-setup, automation]
version: 1.3.0
author: Gil Lund
created: 2025-11-13
updated: 2026-04-09
requires_mcp: none
---

# Obsidian Vault Setup with Zotero Integration

## Installation

This skill includes templates and automation scripts that need to be installed globally.

### Installation Location

When installed to `~/.claude/skills/obsidian-setup/`, the skill provides:
- **Scripts**: `~/.claude/skills/obsidian-setup/scripts/` (setup and verification)
- **Templates**: `~/.claude/skills/obsidian-setup/templates/` (literature note template)
- **Guides**: `~/.claude/skills/obsidian-setup/guides/` (quick start and troubleshooting)
- **Config Examples**: `~/.claude/skills/obsidian-setup/config-examples/` (environment templates)
- **Documentation**: `~/.claude/skills/obsidian-setup/skill.md` (this file)

### Script Paths

All scripts in this skill use the following path to locate templates and resources:

```bash
SKILL_DIR="$HOME/.claude/skills/obsidian-setup"
SCRIPTS_DIR="$SKILL_DIR/scripts"
TEMPLATES_DIR="$SKILL_DIR/templates"
```

From any project, you can run:
```bash
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh
bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh
```

---

## Purpose

This skill provides a complete automated workflow for setting up Obsidian vaults integrated with Zotero for academic literature management and citation workflows. It includes automated scripts, templates, verification tests, and comprehensive documentation to create production-ready research environments in minutes.

The skill teaches the methodology for:
- **Automated vault provisioning** - Script-based setup creating folder structures, templates, and configuration
- **Custom vault display names** - Vault Nickname plugin auto-installed for context-based naming (folder stays `vault/`)
- **Zotero Web API integration** - Connecting Obsidian to Zotero library for seamless citation management
- **Template-based literature notes** - Handlebars templates that auto-populate with Zotero metadata
- **Verification-driven setup** - Automated testing to ensure correct configuration
- **Citation workflow optimization** - Pandoc-style citations with bibliography generation

**When to use this skill**:
- Starting a new research project requiring literature management
- Setting up a knowledge base with academic citation support
- Creating literature review vaults for thesis/dissertation work
- Migrating from manual citation management to automated workflows
- Teaching others to set up research environments
- Creating replicable research project templates

**When NOT to use this skill**:
- Simple note-taking without citations (use basic Obsidian setup)
- Projects not requiring Zotero integration
- When using alternative citation managers (Mendeley, EndNote)
- Read-only literature review (just use Zotero directly)

---

## Quick Start

### Prerequisites

1. **Obsidian** installed ([download](https://obsidian.md))
2. **Zotero** installed ([download](https://www.zotero.org/download/))
3. **Better BibTeX** Zotero plugin installed ([download](https://retorque.re/zotero-better-bibtex/))
4. **Pandoc** installed (`brew install pandoc`)
5. **Zotero API Key** obtained ([get key](https://www.zotero.org/settings/keys))

### Step 1: Set Environment Variables

```bash
# Add to ~/.zshrc or ~/.bash_profile
export ZOTERO_API_KEY="your_24_character_api_key"
export ZOTERO_USER_ID="your_8_digit_user_id"

# Reload shell
source ~/.zshrc
```

### Step 2: Run Setup Script

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run automated setup
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh
```

### Step 3: Verify Setup

```bash
bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh
```

### Step 4: Configure Obsidian

1. Open folder as vault in Obsidian
2. **Enable community plugins** (required — cannot be automated):
   - Settings → Community plugins → **Turn on community plugins**
   - Obsidian requires this manual step for security
   - The **Vault Nickname** and **Dataview** plugins are pre-installed by the setup script and will activate automatically once community plugins are enabled
3. Verify the vault display name appears in the title bar (set during setup via `--vault-name`)

### Step 5: Install Citation Plugin Stack

Install these plugins via Community plugins → Browse. See `references/proven-citation-stack.md` for detailed configuration.

**Required plugins (install in this order):**

4. Install **Pandoc Reference List** plugin — live `[@citekey]` rendering
   - Settings → Pandoc Reference List:
   - **Path to Pandoc:** `/opt/homebrew/bin/pandoc` (verify with `which pandoc`)
   - **Path to Bibliography:** absolute path to your `.bib` file (e.g., `/Users/you/project/vault/citations.bib`)
   - **Pull from Zotero:** ✓ Enabled (also pulls live from Zotero desktop)
   - **CSL Style URL:** `https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl` (or your preferred style)
   - **Render Citations:** ✓ Enabled
   - **Enable CiteKey Completion:** ✓ Enabled

5. Install **Zotero Integration** plugin — import items from Zotero as vault notes
   - Settings → Zotero Integration:
   - **Database:** Zotero (connects to running Zotero desktop app)
   - **Note Import Folder:** `Literature/` (or `sources/` for CEDS-style)
   - **Cite Suggest Template:** `[@{{citekey}}]`
   - **Export Format → Output Path:** `Literature/{{citekey}}.md`
   - **Template File:** `Templates/Zotero-Literature-Note.md`

6. *(Optional)* Install **Citations** plugin — BibTeX-based citekey search and insertion
   - Settings → Citations:
   - **Citation database format:** BibLaTeX
   - **Citation database path:** same `.bib` file as Pandoc Reference List

### Step 6: Create BibTeX File

The `.bib` file bridges Zotero and Obsidian's citation rendering:

**Option A: Better BibTeX Auto-Export (Recommended)**
1. In Zotero desktop, right-click your project collection → Export Collection
2. Format: Better BibLaTeX (or Better BibTeX)
3. Check **"Keep updated"** for automatic re-export
4. Save to vault root as `{ProjectName}-Citations.bib`

**Option B: Zotero Web API Export**
```bash
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY/items?format=bibtex" \
  > vault/citations.bib
```

### Step 7: Test Citation Workflow

1. Add a paper to your Zotero collection (ensures it appears in `.bib` file)
2. In an Obsidian note, type `[@` — autocomplete should suggest citekeys
3. Insert a citation: `[@smith2024]`
4. The Pandoc Reference List should render it inline (e.g., "(Smith et al., 2024)")
5. Test Zotero import: Cmd+P → "Zotero Integration: Create literature note"

---

## Core Methodology

### 1. Automated Vault Provisioning

The setup uses a bash script (`setup-obsidian-vault.sh`) that automates the entire vault creation process.

**Key Principles**:
1. **Idempotent execution** - Safe to run multiple times, won't overwrite existing content
2. **Non-interactive mode** - Supports both interactive prompts and automated execution
3. **Environment-based configuration** - Uses `ZOTERO_API_KEY` and `ZOTERO_USER_ID` environment variables
4. **Template-first approach** - Installs working templates immediately, ready for first use
5. **Verification-ready** - Creates marker files and structure for automated testing

**Setup Script Execution**:
```bash
# Basic usage (interactive — prompts for vault location and display name)
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh

# With custom vault display name
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh \
  --vault-name "My Research Project"

# Non-interactive mode (for automation — display name defaults to parent dir name)
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh \
  --non-interactive \
  --vault-path /path/to/vault

# Non-interactive with explicit display name
bash ~/.claude/skills/obsidian-setup/scripts/setup-obsidian-vault.sh \
  --non-interactive \
  --vault-path /path/to/vault \
  --vault-name "Climate Research"
```

**Folder Structure Created**:
```
vault/
├── .obsidian/
│   ├── plugins/vault-nickname/  # Custom vault display name
│   └── community-plugins.json   # Pre-registered plugins
├── Literature/              # Auto-generated literature notes from Zotero
│   └── attachments/        # PDFs, images, attachments
├── Synthesis/              # Research synthesis and analysis notes
├── Templates/              # Note templates
│   └── Zotero-Literature-Note.md
├── docs/                   # Project documentation
├── README.md              # Setup instructions and next steps
├── .gitignore             # Git configuration
└── .config-examples/      # Plugin configuration examples
```

---

### 2. Zotero Web API Integration

The skill configures Zotero Integration plugin to use Web API (not local Zotero database), enabling:
- Cloud-based access to library
- Cross-platform compatibility
- No file path dependencies
- Remote collaboration support

**Prerequisites Setup**:
```bash
# 1. Get Zotero credentials from https://www.zotero.org/settings/keys
# 2. Create API key with permissions:
#    - Library access: Read/Write
#    - Notes access: Read/Write
#    - File access: Read/Write

# 3. Set environment variables
export ZOTERO_API_KEY="your_24_character_api_key"
export ZOTERO_USER_ID="your_8_digit_user_id"

# 4. Add to shell config for persistence
echo 'export ZOTERO_API_KEY="your_key"' >> ~/.zshrc
echo 'export ZOTERO_USER_ID="your_id"' >> ~/.zshrc
source ~/.zshrc
```

**Plugin Configuration** (in Obsidian):
```
Settings → Zotero Integration

Database Type: Web Library
User ID: [8-digit number]
API Key: [24-character key]

Literature Note Folder: Literature/
Template File: Templates/Zotero-Literature-Note.md
Image Folder: Literature/attachments/
Import Attachments: ✓ Enabled

Citation Format: Pandoc
Bracket Style: [@citekey]
```

---

### 3. Template-Based Literature Notes

Literature notes use Handlebars template syntax to auto-populate metadata from Zotero items, plus Obsidian-standard tag format.

**Obsidian Tag Standards**:
- Use `Tags: #tag1 #tag2` format (with `#` prefix, space-separated) in the body after YAML frontmatter
- This enables Obsidian's native tag functionality and graph visualization
- Do NOT use array format `tags: [tag1, tag2]` in frontmatter

**Available Variables** (most commonly used):
- `{{title}}` - Paper title
- `{{authors}}` - Author list
- `{{date}}` - Publication date (use `| format("YYYY")` for year)
- `{{itemType}}` - journalArticle, book, conferencePaper, etc.
- `{{publicationTitle}}` - Journal or book name
- `{{DOI}}` - Digital Object Identifier
- `{{abstractNote}}` - Abstract text
- `{{citekey}}` - Citation key (Better BibTeX)
- `{{itemKey}}` - Zotero API key
- `{{notes}}` - Zotero notes
- `{{tags}}` - Zotero tags
- `{{attachments}}` - PDFs and files (array)

---

### 4. Verification-Driven Setup

Every setup should be verified with the automated verification script.

**Verification Script**:
```bash
# Test current directory
bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh

# Test specific vault
bash ~/.claude/skills/obsidian-setup/scripts/verify-obsidian-setup.sh /path/to/vault
```

**What Gets Verified** (7 test categories):

1. **Folder Structure** - Literature/, Synthesis/, Templates/, docs/
2. **Required Files** - Templates, README, .gitignore
3. **Zotero Credentials** - API key and User ID format
4. **Zotero API Connection** - Authentication and library access
5. **Template Validation** - YAML frontmatter and Handlebars variables
6. **File Permissions** - Writable directories
7. **Obsidian Configuration** - Plugin detection (optional)

---

### 5. Citation Workflow

**Step-by-Step Workflow**:

1. **Add Paper to Zotero** (browser connector, DOI import, or manual)
2. **Create Literature Note in Obsidian**:
   - Press `Ctrl/Cmd + P` (Command Palette)
   - Type: "Zotero Integration: Create literature note"
   - Select paper → Template auto-populates!
3. **Cite in Synthesis Notes**:
   ```markdown
   Recent research shows [@smith2024climate] that...
   Multiple studies support this [@wilson2022green; @doe2023urban].
   ```
4. **Generate Bibliography** (using Pandoc Reference List plugin)

**Citation Formats**:
```markdown
[@smith2024]              # Standard citation: (Smith et al., 2024)
@smith2024                # In-text: Smith et al. (2024)
[-@smith2024]             # Suppress author: (2024)
[@smith2024; @wilson2022] # Multiple citations
[@smith2024, p. 42]       # With page number
```

---

## Best Practices

### Maps of Content (MOCs)

Use MOC files as navigational index pages for folder hierarchies. MOCs link to all notes within a section and provide status/context at a glance.

**Naming Convention:** `{FolderName} MOC.md` (e.g., `Literature MOC.md` inside `Literature/`)
- The "MOC" suffix is the most common Obsidian community standard
- No plugins required — works with vanilla Obsidian
- Easily searchable across the vault (search "MOC")
- Alternative: Name the MOC the same as the folder (e.g., `Literature/Literature.md`) — requires the **Folder Notes** plugin

**MOC Structure:**
```markdown
# {Section Name} MOC

Brief description of what this section contains.

---

## Contents

| Note | Description | Status |
|------|-------------|--------|
| [[Note-Name]] | What it covers | ✅ Complete |
| [[Other-Note]] | What it covers | 🟡 Draft |

---

**Section Status:** ✅ Complete
```

**When to Create MOCs:**
- Any folder with 3+ notes benefits from a MOC
- Hierarchical projects (proposals, research, documentation)
- When notes need status tracking or sequencing
- When sharing a vault with collaborators who need navigation

### Do This

1. **Use environment variables for credentials** - Keep credentials out of git
2. **Run verification after setup** - Catch errors immediately
3. **Use separate folders for literature vs synthesis** - Separate imported content from your analysis
4. **Use Better BibTeX for citation keys** - Human-readable citation keys
5. **Git-track your vault** with appropriate .gitignore
6. **Use MOC files for folder navigation** - Name them `{FolderName} MOC.md`

### Avoid This

1. **Don't hardcode API credentials in files** - Use environment variables
2. **Don't use local Zotero database connection** - Use Web Library for portability
3. **Don't manually create folder structure** - Use automated script
4. **Don't edit literature notes extensively** - Put analysis in Synthesis/
5. **Don't skip template validation** - Use conditional rendering for optional fields
6. **Don't use `_Index.md` for folder indexes** - Use `{FolderName} MOC.md` convention instead

---

## Troubleshooting

### Plugin Won't Connect to Zotero

```bash
# Verify credentials
echo $ZOTERO_API_KEY  # Should be 24 characters
echo $ZOTERO_USER_ID  # Should be 8 digits

# Test API
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1"
```

### Template Not Populating

1. Verify template path: `Templates/Zotero-Literature-Note.md`
2. Check template file exists: `ls Templates/`
3. Validate template syntax (YAML frontmatter, Handlebars variables)

### Citations Not Rendering Inline

1. Verify Pandoc Reference List plugin is enabled (this does the rendering, not Zotero Integration)
2. Check `pathToBibliography` in plugin settings points to your `.bib` file (must be absolute path)
3. Check `pathToPandoc` points to pandoc binary (`which pandoc`)
4. Verify `.bib` file has entries (`wc -l vault/*.bib`)
5. If using `pullFromZotero: true`, Zotero desktop must be running

### Plugin Settings Reset to Defaults After Install

**Problem:** Obsidian overwrites `data.json` when a plugin is first loaded. Pre-configured settings written before plugin installation get wiped.

**Root cause:** Obsidian holds plugin settings in memory. While running, it periodically flushes in-memory state to `data.json`, overwriting any external changes.

**Solution:** Writing `data.json` programmatically DOES work, but **Obsidian must be fully quit first** (Cmd+Q, not just close window). The sequence is:

1. **User quits Obsidian** (verify with `pgrep -l Obsidian` — must show nothing)
2. **Claude writes `data.json`** with the desired settings
3. **User reopens Obsidian** — plugin loads settings from the file

This is also the required sequence for ANY `.obsidian/` config changes (community-plugins.json, plugin data.json, etc.). If Obsidian is running, in-memory state wins.

**Key Pandoc Reference List settings** (match the working CEDS pattern):
- `pullFromZotero: true` — live pull from Zotero desktop (requires Better BibTeX)
- `pathToBibliography` — absolute path to `.bib` file
- `cslStyleURL` — CSL style from GitHub (APA, IEEE, Nature, etc.)
- `enableCiteKeyCompletion: true` — `[@` autocomplete
- `showCitekeyTooltips: true` — hover tooltips on citations
- `zoteroGroups: [{"id": 1, "name": "My Library"}]` — include your library

### Citekey Autocomplete Not Working

1. Verify `enableCiteKeyCompletion: true` in Pandoc Reference List settings
2. Type `[@` (not just `@`) — the bracket triggers autocomplete
3. Check `.bib` file is valid BibTeX (no syntax errors)
4. If using Citations plugin, verify its BibTeX path matches the same `.bib` file

### BibTeX File Not Updating

1. If using Better BibTeX auto-export: check "Keep updated" was checked during export
2. Manual refresh: re-export collection from Zotero, or use Zotero Web API:
   ```bash
   curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
     "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY/items?format=bibtex" \
     > vault/citations.bib
   ```

---

## Checklist

### Prerequisites
- [ ] Obsidian installed
- [ ] Zotero installed
- [ ] Zotero API key obtained
- [ ] Environment variables set and tested

### Setup
- [ ] Ran setup script
- [ ] Folder structure created
- [ ] Template file installed
- [ ] Ran verification script

### Obsidian Configuration
- [ ] Opened folder as vault in Obsidian
- [ ] **Enabled community plugins** (Settings → Community plugins → Turn on)
- [ ] Verified Vault Nickname plugin is active and display name is correct
- [ ] Installed and configured **Pandoc Reference List** plugin
- [ ] Installed and configured **Zotero Integration** plugin
- [ ] *(Optional)* Installed **Citations** plugin for BibTeX search
- [ ] Dataview plugin active (pre-installed by setup script)

### BibTeX Setup
- [ ] Better BibTeX installed in Zotero desktop
- [ ] Collection exported to `.bib` file in vault root
- [ ] BibTeX path configured in Pandoc Reference List and Citations plugins

### Testing
- [ ] Type `[@` in a note — citekey autocomplete appears
- [ ] Insert `[@citekey]` — renders as formatted citation (e.g., "(Smith et al., 2024)")
- [ ] Cmd+P → "Zotero Integration: Create literature note" — template populates
- [ ] Hover over citation — tooltip shows full reference

---

## Integration with Other Skills

### Works Well With:

- **citation-source-verification**: Complete citation workflow
  - This skill sets up the Obsidian vault
  - citation-source-verification handles searching, verifying, and adding sources

- **obsidian-vault-keeper**: Ongoing vault maintenance and knowledge building
  - This skill sets up the initial Obsidian vault structure
  - obsidian-vault-keeper handles ongoing operations: ingest, query, lint
  - Use Dataview plugin for dynamic vault navigation

- **configuration-management**: Secure config management
  - Keep secrets (API keys) in environment variables
  - Separate config from vault content

---

## Included Assets

### Scripts
- `scripts/setup-obsidian-vault.sh` - Automated vault setup
- `scripts/verify-obsidian-setup.sh` - Verification testing

### Templates
- `templates/Zotero-Literature-Note.md` - Handlebars template for Zotero Integration plugin

### References
- `references/proven-citation-stack.md` - Complete plugin configuration from working CEDS project (Zotero Integration + Pandoc Reference List + Citations plugin settings, BibTeX setup, template examples)

### Guides
- `guides/QUICK-START.md` - 10-minute setup guide

### Config Examples
- `config-examples/env-template.sh` - Environment variable template

---

## External Resources

- **Obsidian**: https://help.obsidian.md/
- **Vault Nickname Plugin**: https://github.com/rscopic/obsidian-vault-nickname
- **Zotero Integration Plugin**: https://github.com/mgmeyers/obsidian-zotero-integration
- **Pandoc Reference List Plugin**: https://github.com/mgmeyers/obsidian-pandoc-reference-list
- **Citations Plugin**: https://github.com/hans/obsidian-citation-plugin
- **Better BibTeX for Zotero**: https://retorque.re/zotero-better-bibtex/
- **Zotero**: https://www.zotero.org/support/
- **Zotero API**: https://www.zotero.org/support/dev/web_api/v3/start
- **Handlebars**: https://handlebarsjs.com/guide/
- **Pandoc Citations**: https://pandoc.org/MANUAL.html#citations
- **CSL Styles Repository**: https://github.com/citation-style-language/styles

---

## Version History

### 1.3.0 (2026-04-09)
- **Added proven citation plugin stack** from CEDS project
  - Pandoc Reference List: live `[@citekey]` rendering, hover tooltips, citekey autocomplete
  - Zotero Integration: import items as vault notes with PDF annotations
  - Citations plugin: BibTeX-based citekey search
- Added `references/proven-citation-stack.md` with exact plugin configs from working setup
- Added BibTeX file setup instructions (Better BibTeX, Web API, zotero-cli)
- Updated prerequisites: Pandoc, Better BibTeX now required
- Rewrote Steps 4-7 with full citation plugin installation workflow
- Expanded troubleshooting: citation rendering, citekey autocomplete, BibTeX refresh
- Fixed verification script crash (`set -e` + arithmetic bug)
- Updated checklist with BibTeX and plugin testing steps
- Pre-configuring plugin `data.json` files works — write configs before first Obsidian install

### 1.2.0 (2026-04-07)
- Updated setup script and obsidian-setup skill doc improvements

### 1.1.0 (2025-12-18)
- Restructured as portable skill for `~/.claude/skills/` installation
- Added Installation section with portable paths
- Included all scripts, templates, and guides in skill folder
- Updated script paths to use `$HOME/.claude/skills/obsidian-setup/`

### 1.0.0 (2025-11-13)
- Initial release
- Automated setup script with interactive and non-interactive modes
- Comprehensive verification testing
- Production-ready Handlebars template
- Complete documentation suite

---

**Last Updated**: 2025-12-18
**Maintainer**: Gil Lund
**License**: MIT
