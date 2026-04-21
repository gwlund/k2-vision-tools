# Proven Citation Plugin Stack

Reference configuration from a working Obsidian + Zotero citation setup (2025-09-CEDS project). This documents the exact plugins, versions, and settings that enable live `[@citekey]` rendering, Zotero import, and Pandoc export.

> **IMPORTANT:** Obsidian holds plugin settings in memory and flushes to `data.json` periodically. Writing `data.json` programmatically works, but **Obsidian must be fully quit first** (`Cmd+Q`, verify with `pgrep -l Obsidian`). If Obsidian is running, in-memory state overwrites any external file changes. Sequence: quit Obsidian → write `data.json` → reopen Obsidian.

---

## Plugin Stack Overview

| Plugin | ID | Version | Role |
|--------|-----|---------|------|
| **Zotero Integration** | `obsidian-zotero-desktop-connector` | 3.2.1 | Import Zotero items as structured notes, pull PDF annotations |
| **Pandoc Reference List** | `obsidian-pandoc-reference-list` | 2.0.25 | Live `[@citekey]` rendering in editor + reading mode, hover tooltips |
| **Citations** | `obsidian-citation-plugin` | 0.4.5 | BibTeX-based citekey search and insertion |
| **Pandoc Plugin** | `obsidian-pandoc` | 0.4.1 | Export notes to DOCX/PDF via Pandoc |
| **Dataview** | `dataview` | 0.5.x | Dynamic queries over YAML frontmatter |
| **Templater** | `templater-obsidian` | 2.16.2 | Advanced template engine |

**Minimum viable stack for citations:** Pandoc Reference List + a `.bib` file. Everything else is enhancement.

---

## How the Pieces Connect

```
Zotero Desktop App
    │
    ├──► Better BibTeX plugin ──► .bib file (auto-exported)
    │                                 │
    │                                 ├──► Pandoc Reference List (live rendering)
    │                                 ├──► Citations plugin (citekey autocomplete)
    │                                 └──► Pandoc CLI (document export)
    │
    ├──► Zotero Integration plugin (direct DB connection)
    │         └──► Import items as vault notes with annotations
    │
    └──► Zotero Web API
              └──► zotero-cli scripts (search, import, tag)
              └──► Pandoc Reference List (pullFromZotero: true)
```

**Three connection paths to Zotero:**
1. **BibTeX file** — Stable, works offline. Exported by Better BibTeX.
2. **Desktop database** — Zotero Integration plugin reads the local Zotero SQLite DB directly.
3. **Web API** — zotero-cli scripts and Pandoc Reference List live pull.

---

## Plugin Configurations

### Zotero Integration (`obsidian-zotero-desktop-connector`)

`.obsidian/plugins/obsidian-zotero-desktop-connector/data.json`:
```json
{
  "database": "Zotero",
  "noteImportFolder": "sources",
  "pdfExportImageDPI": 120,
  "pdfExportImageFormat": "jpg",
  "pdfExportImageQuality": 90,
  "citeFormats": [
    { "name": "IEEE", "format": "pandoc" }
  ],
  "exportFormats": [
    {
      "name": "sources",
      "outputPathTemplate": "sources/{{citekey}}.md",
      "imageOutputPathTemplate": "sources/images/{{citekey}}/",
      "imageBaseNameTemplate": "image"
    }
  ],
  "citeSuggestTemplate": "[@{{citekey}}]",
  "openNoteAfterImport": false,
  "whichNotesToOpenAfterImport": "first-imported-note",
  "pdfExportImageOCR": true,
  "pdfExportImageTesseractPath": "/opt/homebrew/bin/tesseract"
}
```

**Key settings:**
- `database: "Zotero"` — connects to Zotero desktop (not Juris-M)
- `noteImportFolder: "sources"` — imported notes go to `sources/` folder
- `citeSuggestTemplate: "[@{{citekey}}]"` — Pandoc-style citation insertion
- `pdfExportImageOCR: true` — OCR on PDF annotation images via Tesseract

**Adapt for new vaults:** Change `noteImportFolder` to match your vault structure (e.g., `Literature` for vault-keeper compatible vaults).

### Pandoc Reference List (`obsidian-pandoc-reference-list`)

`.obsidian/plugins/obsidian-pandoc-reference-list/data.json`:
```json
{
  "pathToPandoc": "/opt/homebrew/bin/pandoc",
  "tooltipDelay": 400,
  "zoteroGroups": [
    { "id": 1, "name": "My Library", "lastUpdate": 1775752826048 }
  ],
  "renderCitations": true,
  "renderCitationsReadingMode": true,
  "renderLinkCitations": true,
  "pullFromZotero": true,
  "cslStylePath": "",
  "cslStyleURL": "https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl",
  "pathToBibliography": "/absolute/path/to/your-citations.bib",
  "enableCiteKeyCompletion": true,
  "showCitekeyTooltips": true
}
```

**Key settings:**
- `pathToPandoc` — must point to Pandoc binary (install via `brew install pandoc`)
- `pathToBibliography` — **absolute path** to your `.bib` file
- `pullFromZotero: true` — also pulls live from running Zotero desktop
- `cslStyleURL` — CSL style for rendering (IEEE, APA, Nature, etc.)
- `renderCitations: true` — renders `[@citekey]` inline in edit mode
- `enableCiteKeyCompletion: true` — autocomplete when typing `[@`

**Common CSL style URLs:**
- IEEE: `https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl`
- APA 7th: `https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl`
- Nature: `https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl`
- Vancouver: `https://raw.githubusercontent.com/citation-style-language/styles/master/vancouver.csl`
- Chicago Author-Date: `https://raw.githubusercontent.com/citation-style-language/styles/master/chicago-author-date.csl`

### Citations Plugin (`obsidian-citation-plugin`)

Typically minimal configuration needed. Set the path to your `.bib` file in plugin settings. Provides:
- Hotkey to insert `[@citekey]` from search
- Literature note creation from BibTeX entries
- Complements Pandoc Reference List with better search UI

---

## BibTeX File Setup

The `.bib` file is the bridge between Zotero and Obsidian's citation rendering.

### Option A: Better BibTeX Auto-Export (Recommended)

1. Install **Better BibTeX** plugin in Zotero desktop
2. Right-click a collection → Export Collection
3. Format: Better BibLaTeX or Better BibTeX
4. Check "Keep updated" for auto-export
5. Save to vault root as `{ProjectName}-Citations.bib`

### Option B: Manual Export via zotero-cli

```bash
# Export collection to BibTeX (requires zotero-cli)
zotero-export-collection "Collection Name" --format bibtex > vault/citations.bib
```

### Option C: Zotero Web API Export

```bash
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY/items?format=bibtex" \
  > vault/citations.bib
```

---

## Citation Format Convention

**In-text (Pandoc style):**
```markdown
Recent research shows [@smith2024climate] that outcomes improve.
Multiple studies support this [@wilson2022; @doe2023].
```

**Rendered by Pandoc Reference List as:**
> Recent research shows (Smith et al., 2024) that outcomes improve.
> Multiple studies support this (Wilson, 2022; Doe, 2023).

**Citation syntax:**
- `[@citekey]` — standard parenthetical citation
- `@citekey` — in-text (author as part of sentence)
- `[-@citekey]` — suppress author, show year only
- `[@key1; @key2]` — multiple citations
- `[@key, p. 42]` — with page number

---

## Prerequisites

| Dependency | Install | Verify |
|-----------|---------|--------|
| Pandoc | `brew install pandoc` | `pandoc --version` |
| Zotero Desktop | https://zotero.org/download | App running |
| Better BibTeX (Zotero plugin) | https://retorque.re/zotero-better-bibtex/ | Zotero → Preferences → Better BibTeX |
| Tesseract (optional, for OCR) | `brew install tesseract` | `tesseract --version` |

---

## Template Examples

### Zotero Integration Export Template

Save as `Templates/sources.md` in vault. Used when importing from Zotero Integration plugin:

```markdown
---
type: literature-note
citekey: {{citekey}}
title: "{{title}}"
authors: [{{authors}}]
year: {{date | format("YYYY")}}
itemType: {{itemType}}
publication: "{{publicationTitle}}"
doi: "{{DOI}}"
zotero-key: "{{itemKey}}"
---

Tags: #literature #{{itemType}}

# {{title}}

## Metadata

- **Authors:** {{authors}}
- **Year:** {{date | format("YYYY")}}
- **Type:** {{itemType}}
{{#if publicationTitle}}- **Publication:** {{publicationTitle}}{{/if}}
{{#if DOI}}- **DOI:** [{{DOI}}](https://doi.org/{{DOI}}){{/if}}
{{#if url}}- **URL:** {{url}}{{/if}}
- **Zotero:** [Open in Zotero]({{desktopURI}})
- **Cite as:** [@{{citekey}}]

## Abstract

{{abstractNote}}

## Key Findings

1.
2.
3.

## Relevance to Project

[How this relates to your research]

## Key Quotes

> "Quote here" (p. XX)

## Annotations

{{#each annotations}}
### {{color}} — p. {{pageLabel}}

{{#if comment}}**Note:** {{comment}}{{/if}}

> {{annotatedText}}

{{/each}}

## Related Literature

- [[]]

---

**Imported:** {{importDate | format("YYYY-MM-DD")}}
**Zotero Key:** {{itemKey}}
```

---

**Last Updated:** 2026-04-09
**Source:** 2025-09-CEDS project (verified working setup)
