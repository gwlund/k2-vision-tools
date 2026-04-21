# Vault Schema Template

This file is the template for the `CLAUDE.md` that gets generated inside each vault during `init`. Replace placeholders (`{{VAULT_NAME}}`, `{{VAULT_PURPOSE}}`, `{{DOMAIN}}`, `{{CREATED_DATE}}`, `{{DOMAIN_NOTES}}`) with vault-specific values.

---

```markdown
# {{VAULT_NAME}} — Vault Schema

## Identity

- **Name**: {{VAULT_NAME}}
- **Purpose**: {{VAULT_PURPOSE}}
- **Domain**: {{DOMAIN}}
- **Created**: {{CREATED_DATE}}
- **Maintained by**: LLM (via obsidian-vault-keeper skill)

---

## Architecture

This vault follows the three-layer LLM vault pattern:

1. **Raw Sources** (`raw/`) — Immutable source documents. You read from here but never modify these files.
2. **Vault Pages** (`entities/`, `concepts/`, `sources/`, `synthesis/`, `events/`) — LLM-maintained pages. You create, update, and cross-reference these.
3. **Schema** (this file) — Conventions, workflows, and domain configuration.

### Directory Structure

vault/
├── raw/                # Layer 1: Immutable source documents
│   └── assets/         # Images, downloaded files
├── entities/           # Named things — tools, people, orgs, projects
├── concepts/           # Patterns, principles, ideas, methodologies
├── sources/            # One summary page per ingested raw document
├── synthesis/          # Comparisons, analyses, filed query results
├── events/             # Dated events, releases, decisions
├── templates/          # Page templates (entity, concept, source, synthesis, event)
├── documents/          # Raw PDF files
├── overview.md         # High-level vault summary
├── index.md            # Master catalog — read this first to navigate
├── log.md              # Chronological operations log (append-only)
└── CLAUDE.md           # This file — schema and conventions

### Special Files

| File | Purpose | Who Updates |
|------|---------|------------|
| `index.md` | Categorized catalog of all vault pages with one-line descriptions | LLM — on every ingest |
| `overview.md` | High-level vault summary and key themes | LLM — periodically |
| `log.md` | Chronological record of all operations | LLM — append-only |

---

## Page Types

| Type | Folder | Required YAML Fields |
|------|--------|---------------------|
| Entity | `entities/` | type, title, aliases, created, updated, status, source_count, tags_yaml |
| Concept | `concepts/` | type, title, aliases, created, updated, status, source_count, tags_yaml |
| Source | `sources/` | type, title, source_file, source_type, date_ingested, created, updated, tags_yaml |
| Synthesis | `synthesis/` | type, title, synthesis_type, created, updated, status, source_count, tags_yaml |
| Event | `events/` | type, title, event_date, event_type, created, updated, tags_yaml |

**Templates**: See `templates/` folder for complete page templates with all sections.

**Status values**: `stub` | `developing` | `mature`

---

## Conventions

### File Naming
- Title Case with hyphens: `My-Entity-Name.md`
- Source pages: match the source document name where practical
- Event pages: prefix with date: `2026-04-07-Event-Name.md`

### Wikilinks
- Always use `[[Page Name]]` for internal vault references
- Link to the page name without the `.md` extension
- Use `[[Page Name|display text]]` when the display text differs from the page name

### Tags
- **Body tags** (Obsidian native): `Tags: #type #domain-tag` — placed after frontmatter, before first section
- **YAML tags_yaml** (Dataview): `tags_yaml: [type, domain-tag]` — in frontmatter for queries
- Both must be kept in sync

### Dates
- ISO 8601 format: `YYYY-MM-DD`
- All `created` and `updated` fields use this format

### MOCs (Maps of Content)
- One per content folder: `{FolderName} MOC.md`
- Example: `entities/Entities MOC.md`, `concepts/Concepts MOC.md`
- MOCs list all pages in their folder with one-line descriptions

---

## Operations

You maintain this vault using the obsidian-vault-keeper skill. The five operations are:

| Operation | Purpose |
|-----------|---------|
| `init` | Create vault structure (already done for this vault) |
| `ingest` | Process one source: create/update pages, discuss findings |
| `batch-ingest` | Process multiple sources without pausing |
| `query` | Answer questions using vault content, optionally file as synthesis |
| `lint` | Health-check: frontmatter, orphans, broken links, completeness |

### On Every Ingest

Follow this checklist for every source ingested (both single and batch):

1. Create source summary page in `sources/`
2. Create or update entity pages in `entities/`
3. Create or update concept pages in `concepts/`
4. Create event pages in `events/` if dated events found
5. Update `index.md` with new entries
6. Update relevant MOCs
7. Append entry to `log.md`
8. Run incremental lint on touched pages

### What You Must Never Do

- Never modify files in `raw/` — these are immutable source documents
- Never delete pages without explicit user instruction
- Never skip updating `index.md` or `log.md` after an ingest
- Never create pages without proper YAML frontmatter
- Never use plain text references when a wikilink is appropriate

---

## Cross-Reference Rules

When creating or updating pages, maintain these links:

| Page Type | Must Link To |
|-----------|-------------|
| Entity | Related entities, concepts it embodies, sources that mention it |
| Concept | Related concepts, entities that exemplify it, sources that cover it |
| Source | All entities extracted, all concepts covered |
| Synthesis | All sources consulted, entities and concepts analyzed |
| Event | Related entities, related concepts, source references |

---

## Index Format

The `index.md` file uses categorized tables:

### Entities

| Page | Description | Status | Sources |
|------|-------------|--------|---------|
| [[Entity-Name]] | One-line description | developing | 3 |

### Concepts

| Page | Description | Status | Sources |
|------|-------------|--------|---------|
| [[Concept-Name]] | One-line description | mature | 5 |

### Sources

| Page | Source File | Type | Date Ingested |
|------|-----------|------|---------------|
| [[Source-Name]] | raw/file.md | documentation | 2026-04-07 |

### Synthesis

| Page | Type | Status | Sources |
|------|------|--------|---------|
| [[Synthesis-Name]] | comparison | developing | 4 |

### Events

| Page | Date | Type |
|------|------|------|
| [[Event-Name]] | 2026-04-07 | release |

---

## Log Format

Each entry in `log.md` follows this structure:

## [YYYY-MM-DD] operation | Description

- **Pages created**: list of new pages
- **Pages updated**: list of modified pages
- **Issues**: any problems encountered

Valid operations: `init`, `ingest`, `batch-ingest`, `query`, `lint`

---

## Domain-Specific Configuration

{{DOMAIN_NOTES}}

---

**Schema Version**: 1.0.0
**Last Updated**: {{CREATED_DATE}}
```
