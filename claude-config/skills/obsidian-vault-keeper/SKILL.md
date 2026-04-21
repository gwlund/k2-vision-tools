---
name: obsidian-vault-keeper
description: Use when maintaining an LLM-managed Obsidian knowledge vault — ingesting source documents, updating entity/concept/source/synthesis/event pages, answering queries from vault content, or running vault health checks. Applies to any domain-specific knowledge base where the LLM incrementally builds structured, interlinked pages from raw sources so knowledge compounds over time rather than being re-derived each session.
tags: [obsidian, knowledge-management, vault, knowledge-base, llm-vault, entities, concepts, synthesis, ingestion, notes]
version: 1.2.0
author: Gil Lund
created: 2026-04-07
updated: 2026-04-09
requires_mcp: none
---

# Obsidian Vault Keeper

## Overview

This skill implements the LLM vault pattern: instead of re-deriving knowledge from raw documents on every query, the LLM incrementally builds and maintains a persistent Obsidian vault of structured, interlinked pages. Knowledge compounds with each source added. The human curates sources and asks questions; the LLM does all the bookkeeping.

This skill handles **ongoing vault operations** for general-purpose LLM-maintained knowledge bases. It is a companion to `obsidian-setup`, which provisions Zotero-integrated research vaults.

---

## When to Use / When Not to Use

**Use this skill when:**
- Starting a new LLM-maintained knowledge base on any domain
- Ingesting documents, articles, or data into an existing vault
- Answering domain questions using vault content
- Running vault health checks (contradictions, orphans, stale claims)
- The vault needs new page types, schema changes, or structural refactoring

**Do not use this skill when:**
- Setting up a Zotero-integrated academic research vault (use `obsidian-setup`)
- Doing one-off document summarization without intent to maintain a vault
- The knowledge base has a single, narrow document set that will not grow

---

## Architecture

The vault has three layers:

**Layer 1 — Raw sources** (LLM reads, never modifies)
**Layer 2 — LLM-maintained pages** (entities, concepts, sources, synthesis, events)
**Layer 3 — Vault schema** (CLAUDE.md inside vault: conventions, workflows, domain config)

```
vault/
├── raw/                    # Layer 1: Immutable source documents
│   └── assets/             # Images, downloaded files
├── entities/               # Layer 2: Named things (tools, people, orgs)
│   └── Entities MOC.md
├── concepts/               # Patterns, principles, ideas
│   └── Concepts MOC.md
├── sources/                # One summary page per ingested raw document
│   └── Sources MOC.md
├── synthesis/              # Comparisons, analyses, filed query results
│   └── Synthesis MOC.md
├── events/                 # Dated events, releases, decisions
│   └── Events MOC.md
├── templates/              # Page templates (do not ingest)
├── documents/              # Raw PDF files (if not using raw/)
├── overview.md             # High-level vault summary (human-readable)
├── index.md                # Master catalog — LLM reads this first
├── log.md                  # Chronological operations log (append-only)
└── CLAUDE.md               # Layer 3: Vault schema and domain config
```

---

## Operations

| Command | Purpose | Interactive? |
|---------|---------|--------------|
| `init` | Create vault structure, schema, templates, empty index/log | Yes — asks vault name/purpose |
| `ingest` | Process one source: discuss findings, create/update pages | Yes — discusses with user |
| `batch-ingest` | Process multiple sources from manifest without pausing | No — sequential, unattended |
| `query` | Answer questions using vault content, optionally file as synthesis | Yes |
| `lint` | Health-check: contradictions, orphans, stale claims, missing pages | No — produces report |

For step-by-step procedures on each operation, see `references/operations-guide.md`.

---

## Page Types

Each page type lives in its own folder and has required YAML frontmatter for Dataview queries.

| Type | Folder | Required YAML Fields |
|------|--------|----------------------|
| Entity | `entities/` | type, title, aliases, created, updated, status, source_count, tags_yaml |
| Concept | `concepts/` | type, title, aliases, created, updated, status, source_count, tags_yaml |
| Source | `sources/` | type, title, source_file, source_type, date_ingested, created, updated, tags_yaml |
| Synthesis | `synthesis/` | type, title, synthesis_type, created, updated, status, source_count, tags_yaml |
| Event | `events/` | type, title, event_date, event_type, created, updated, tags_yaml |

All pages are Dataview-queryable. For full page templates, see `references/page-templates.md`.

---

## Navigation

Three navigation mechanisms keep the vault traversable:

**index.md** — Master catalog. Categorized links with one-line descriptions. The LLM reads this first before answering any query. Updated on every ingest.

**MOCs (Maps of Content)** — One per content folder (`Entities MOC.md`, `Concepts MOC.md`, etc.). Human-friendly navigation; no plugin required. Named `{FolderName} MOC.md` per Obsidian community convention.

**Dataview** — All pages have queryable frontmatter. Standard fields `type`, `status`, `source_count`, and `tags_yaml` enable cross-folder queries and dashboards.

---

## Ingest Workflow

On every `ingest` and `batch-ingest`, perform these steps in order:

1. Read source document from `raw/` (never modify it)
2. **Resolve citations** — identify all academic papers referenced in the source (by author name, DOI, or citation number). Search Zotero via `zotero-search-items` to find matching entries. For each match, note the citekey from the `.bib` file. If a referenced paper is NOT in Zotero, flag it for the user (do not auto-import).
3. Create source summary page in `sources/` — use `[@citekey]` Pandoc citations for all referenced papers that have Zotero entries. List unresolved references in Additional Notes.
4. Create or update entity pages in `entities/` for all named things found
5. Create or update concept pages in `concepts/` for patterns and principles found — use `[@citekey]` citations when stating claims backed by specific papers (e.g., accuracy benchmarks, dissatisfaction thresholds)
6. Create event pages in `events/` for any dated events found
7. Update `index.md` with new entries
8. Update relevant MOCs (`{FolderName} MOC.md`)
9. Append to `log.md` (date, source, pages created/updated, summary)
10. Run incremental lint on all touched pages (includes citation lint — see below)

For `ingest` (interactive), discuss findings with the user before writing pages; surface interesting connections and contradictions. For `batch-ingest`, proceed without pausing.

---

## Vault Schema (CLAUDE.md)

Each vault contains a `CLAUDE.md` at its root. This is Layer 3 — it defines:
- Vault purpose and domain scope
- Active entity and concept taxonomies
- Naming conventions for this vault's content
- Domain-specific status values and tag vocabularies
- Any deviations from the default schema

The LLM reads `CLAUDE.md` at the start of every session before touching any pages.

For a starter template, see `references/vault-schema-template.md`.

---

## Vault Lint

The `lint` operation checks vault health without modifying any pages. It produces a report covering:

- **Contradictions** — Claims across pages that conflict
- **Orphans** — Pages with no incoming links
- **Stale claims** — Entity/concept pages not updated since new sources were added
- **Missing pages** — Wikilinks in `index.md` or MOCs that have no target page
- **Schema violations** — Pages missing required frontmatter fields

Run manually with:
```bash
bash ~/.claude/skills/obsidian-vault-keeper/scripts/vault-lint.sh /path/to/vault
```

For automated integration, see `references/operations-guide.md`.

---

## Best Practices

**Do:**
- Read `index.md` before every query — never answer from memory alone
- Read source files from `raw/` only; write only to `entities/`, `concepts/`, `sources/`, `synthesis/`, `events/`
- Keep `log.md` append-only — never edit prior entries
- Update MOCs and `index.md` on every ingest, not as a cleanup step later
- Use `[[wikilinks]]` between pages — this creates the knowledge graph
- Prefer updating existing entity/concept pages over creating redundant new ones
- Run incremental lint on touched pages after each ingest
- Preserve `raw/` documents exactly as received
- Use `[@citekey]` Pandoc citations when referencing academic papers (rendered by Pandoc Reference List plugin)
- Include citekeys in source page frontmatter when the source has a Zotero entry

**Avoid:**
- Answering queries from general training knowledge when vault content is available
- Creating entity/concept pages without linking them from `index.md`
- Writing synthesis conclusions directly into entity pages — file them in `synthesis/`
- Skipping `log.md` entries — the log is the audit trail
- Letting `index.md` go stale — it must be current or the LLM navigates blind
- Hardcoding domain assumptions in the skill — put them in vault `CLAUDE.md`
- Writing to `.obsidian/` config files while Obsidian is running — in-memory state overwrites external changes. Always verify Obsidian is quit first (`pgrep -l Obsidian`)

---

## Citation Integration

**Mandatory on ingest.** Every academic paper referenced in a source document MUST be cited with `[@citekey]` Pandoc syntax if it exists in Zotero. This renders live formatted references in Obsidian via Pandoc Reference List plugin.

### Citation Resolution During Ingest

When a source document references external papers (by author name, numbered footnotes, or DOI):

1. **Search Zotero** for each reference using `zotero-search-items "<author or keyword>"`
2. **Match to .bib citekeys** — read the vault's `.bib` file to find the exact citekey (e.g., `soareCataractSurgeryOutcomes2022`)
3. **Use `[@citekey]` in vault pages** — replace plain-text references like "Soare et al. (2022)" with `[@soareCataractSurgeryOutcomes2022]`
4. **Flag unresolved references** — if a cited paper is NOT in Zotero, list it in the source page's Additional Notes section as a candidate for import

### Where Citations Are Required

| Page Type | When to Cite |
|-----------|-------------|
| **Source pages** | All external papers referenced in the raw source document. List all citekeys in Additional Notes even if not used inline. |
| **Concept pages** | Claims backed by specific papers (e.g., accuracy benchmarks, clinical thresholds, comparative data). |
| **Synthesis pages** | All sources consulted, cited inline at point of use. |
| **Entity pages** | Publications by the entity (for researchers) or foundational papers about the entity. |
| **Event pages** | Papers presented or published as part of the event. |

### Citation Format

```markdown
Even the best formula achieves only 52.6% within 0.5D [@soareCataractSurgeryOutcomes2022].
Multiple studies confirm this [@wilson2022; @doe2023].
```

### Prerequisites

Citations require:
- A `.bib` file in the vault root (exported from Zotero)
- Pandoc Reference List plugin installed and configured in Obsidian
- See `obsidian-setup` skill for installation

### Refreshing the BibTeX File

After adding new items to Zotero, refresh the `.bib` file:

```bash
# Via Zotero Web API (works from CLI)
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY/items?format=bibtex" \
  > vault/citations.bib
```

Or use Better BibTeX auto-export (updates automatically when Zotero desktop is running).

---

## Integration with Other Skills

| Skill | How It Integrates |
|-------|-------------------|
| `obsidian-setup` | Provisions Zotero-integrated research vaults with citation plugins (Pandoc Reference List, Zotero Integration, Citations); vault-keeper handles ongoing operations after setup |
| `citation-source-verification` | Use before ingesting academic sources — verify citations via zotero-cli, then vault-keeper creates source pages with `[@citekey]` references |
| `marp` | Export synthesis pages as slide decks; vault provides structured content, marp formats for presentation |
| `agent-browser` | Use to fetch web sources before ingesting; agent-browser retrieves and saves to `raw/`, vault-keeper processes |
| `learning-loop` | Run `/llr` after significant vault work to capture patterns; run `/lla` before unfamiliar vault domains |

---

## Included Assets

### References
- `references/operations-guide.md` — Step-by-step procedures for all operations
- `references/page-templates.md` — Full frontmatter templates for all 5 page types
- `references/vault-schema-template.md` — Starter `CLAUDE.md` template for new vaults

### Scripts
- `scripts/vault-lint.sh` — Standalone lint script (bash)

---

**Last Updated:** 2026-04-09
**Maintainer:** Gil Lund
