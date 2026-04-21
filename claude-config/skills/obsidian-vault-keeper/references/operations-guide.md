# Operations Guide — Obsidian Vault Keeper

Step-by-step procedures for all vault operations. Follow these instructions precisely when performing each operation.

---

## 1. Init

**Interactive:** Yes — asks vault name, purpose, and domain before proceeding.

### Steps

1. Ask the user for:
   - Vault name
   - Vault purpose (1-2 sentences describing what it tracks)
   - Domain focus (e.g., "climate policy", "software architecture", "personal research")

2. Create the following directory structure under the vault root:

   ```
   vault/
   ├── raw/
   │   └── assets/
   ├── entities/
   ├── concepts/
   ├── sources/
   ├── synthesis/
   ├── events/
   ├── templates/
   ├── documents/
   ├── overview.md
   ├── index.md
   ├── log.md
   └── CLAUDE.md
   ```

3. Copy page templates from the skill's `references/page-templates.md` into `vault/templates/`. Each template should be saved as its own file (e.g., `entity-template.md`, `concept-template.md`, `source-template.md`, `synthesis-template.md`, `event-template.md`).

4. Generate `CLAUDE.md` using the skill's `references/vault-schema-template.md` as the base. Customize it with:
   - Vault name
   - Vault purpose
   - Domain focus
   - Any domain-specific terminology the user provides

5. Create `index.md` with empty category headers:

   ```markdown
   # [Vault Name] Index

   ## Entities
   <!-- Entities listed alphabetically -->

   ## Concepts
   <!-- Concepts listed alphabetically -->

   ## Sources
   <!-- Sources listed chronologically or by topic -->

   ## Synthesis
   <!-- Synthesis pages listed by date or topic -->

   ## Events
   <!-- Events listed chronologically -->
   ```

6. Create `overview.md` with vault name and purpose:

   ```markdown
   # [Vault Name]

   [Vault purpose statement]

   **Domain:** [Domain focus]
   **Created:** [YYYY-MM-DD]
   ```

7. Create `log.md` with an initial entry:

   ```markdown
   # Vault Log

   ## [YYYY-MM-DD] init | Vault created

   - **Pages created**: overview.md, index.md, CLAUDE.md, MOC files
   - **Pages updated**: none
   - **Issues**: none
   ```

8. Create `.gitignore` in the vault root:

   ```
   .obsidian/
   .trash/
   ```

9. Create a Map of Contents (MOC) file in each content folder:

   - `entities/Entities MOC.md`
   - `concepts/Concepts MOC.md`
   - `sources/Sources MOC.md`
   - `synthesis/Synthesis MOC.md`
   - `events/Events MOC.md`

   Each MOC starts with:

   ```markdown
   # [Folder Name] MOC

   <!-- Links to all pages in this folder -->
   ```

10. Report to the user what was created: list all directories and files generated.

---

## 2. Ingest (Single Source)

**Interactive:** Yes — discuss findings with the user before creating pages.

**Input:** A source document placed in `raw/` (or a path the user provides).

### Steps

1. Read the source document in full.

2. **Resolve citations** — identify all academic papers referenced in the source (by author name, numbered footnotes, or DOI):
   - Search Zotero for each reference: `zotero-search-items "<author or keyword>"`
   - Read the vault's `.bib` file to find the exact citekey for each match
   - Note which references are NOT in Zotero — these will be flagged to the user
   - If no `.bib` file exists in the vault, skip citation resolution and note it as an issue

3. Discuss key findings with the user:
   - What entities appear (people, organizations, places, systems)?
   - What concepts are covered?
   - What claims or findings are most significant?
   - What should be emphasized?
   - Are there dated events to capture?
   - **Citation status**: which referenced papers resolved to Zotero citekeys, which did not

   Wait for user input before proceeding.

4. Create a source summary page in `sources/`. File naming: `[YYYY-MM-DD] [Source Title].md` where the date is the source's publication date (or today if unknown). Use the source template from `vault/templates/`. **Use `[@citekey]` Pandoc citations** for all referenced papers that have Zotero entries. List unresolved references in Additional Notes.

5. For each entity identified:
   - Check whether an entity page already exists in `entities/`.
   - If it does not exist: create a new entity page using the entity template. Populate known fields from the source.
   - If it exists: open the existing page and add new information. Preserve existing content; append or integrate new details.

6. For each concept identified:
   - Check whether a concept page already exists in `concepts/`.
   - If it does not exist: create a new concept page using the concept template.
   - If it exists: open the existing page and update with new details or references.
   - **Use `[@citekey]` citations** when stating claims backed by specific papers (e.g., accuracy benchmarks, dissatisfaction thresholds, comparative data).

7. For each dated event found:
   - Create an event page in `events/`. File naming: `[YYYY-MM-DD] [Event Name].md`.
   - Link the event page to relevant entities and concepts.

8. Update `index.md`:
   - Add entries for all newly created pages under the appropriate category headers.
   - Index entry format: `- [[Page Name]] — brief one-line description`

9. Update relevant MOC files:
   - Add a wikilink to each newly created page in the corresponding MOC.
   - MOC entry format: `- [[Page Name]]`

10. Append an ingest entry to `log.md`:

    ```markdown
    ## [YYYY-MM-DD] ingest | [Source Title]

    - **Pages created**: list of new pages
    - **Pages updated**: list of existing pages that were modified
    - **Issues**: any problems encountered (broken links, ambiguous entities, unresolved citations, etc.)
    ```

11. Run incremental lint on all pages touched during this ingest (see Lint — Incremental below).

12. Report to the user: what was created, what was updated, any lint issues, and any unresolved citations that need Zotero import.

---

## 3. Batch Ingest

**Interactive:** No — runs sequentially without pausing for discussion.

**Input:** Either a list of file paths or a manifest file (a markdown file listing sources to process, one per line or as a list).

### Steps

1. Read the manifest or file list. Identify all source documents to process.

2. For each source document, perform the following without pausing for user input:
   - Read the source document in full.
   - **Resolve citations** — search Zotero and match to `.bib` citekeys (step 2 from single ingest).
   - Apply reasonable defaults for emphasis and focus based on document content.
   - Create a source summary page in `sources/` with `[@citekey]` citations (step 4 from single ingest).
   - Create or update entity pages (step 5 from single ingest).
   - Create or update concept pages with `[@citekey]` citations where applicable (step 6 from single ingest).
   - Create event pages for any dated events (step 7 from single ingest).
   - Update `index.md` (step 8 from single ingest).
   - Update MOC files (step 9 from single ingest).
   - Append an ingest entry to `log.md` for this source (step 10 from single ingest).

3. After all sources have been processed, run full lint on the entire vault (see Lint — Full below).

4. Append a batch summary to `log.md`:

   ```markdown
   ## [YYYY-MM-DD] batch-ingest | [N] sources processed

   - **Sources processed**: list of source titles
   - **Pages created**: total count and list
   - **Pages updated**: total count and list
   - **Issues**: summary of any problems encountered
   ```

5. Report to the user: summary of what was processed, created, updated, and any lint issues.

---

## 4. Query

**Interactive:** Yes.

### Steps

1. Read `index.md` to identify pages relevant to the user's query.

2. Read the relevant vault pages (entities, concepts, sources, synthesis, events as applicable).

3. Synthesize an answer using content from the vault. Cite vault pages using `[[wikilinks]]` inline in the response. Do not fabricate information not present in the vault.

4. Ask the user: "Should I file this as a synthesis page?"

5. If the user says yes:
   - Create a synthesis page in `synthesis/`. File naming: `[YYYY-MM-DD] [Query Topic].md`. Use the synthesis template from `vault/templates/`.
   - Populate the synthesis page with the answer, sources consulted, and key conclusions.
   - Update `index.md` with a new entry under Synthesis.
   - Update `synthesis/Synthesis MOC.md` with a wikilink to the new page.
   - Append an entry to `log.md`:

     ```markdown
     ## [YYYY-MM-DD] query | [Query Topic]

     - **Pages created**: [synthesis page name]
     - **Pages updated**: index.md, Synthesis MOC.md
     - **Issues**: none
     ```

6. If the user says no: the answer remains in the conversation only. No files are created or modified.

---

## 5. Lint — Incremental

**Scope:** Pages touched during the most recent ingest operation only.

**When to run:** Automatically after each ingest (single or batch per-source).

### Checks

1. **YAML frontmatter present and valid** — Every page must have a YAML frontmatter block (`---` delimiters, valid YAML syntax).

2. **Required fields present** — Check for the required fields appropriate to the page type:
   - Entity pages: `name`, `type`, `tags`
   - Concept pages: `name`, `tags`
   - Source pages: `title`, `date`, `tags`
   - Synthesis pages: `title`, `date`, `tags`
   - Event pages: `title`, `date`, `tags`

3. **Wikilinks resolve** — Every `[[wikilink]]` in the page must correspond to an existing file in the vault. Flag any links that point to non-existent pages.

4. **Body tag line present** — Each page should have at least one `#tag` in the body (distinct from frontmatter tags).

5. **Citation citekeys resolve** — Every `[@citekey]` in the page must correspond to an entry in the vault's `.bib` file. Flag any citekeys that don't match. Also flag plain-text author references (e.g., "Soare et al.") in source or concept pages that should use `[@citekey]` syntax instead.

6. Report issues inline after each page check. Format:

   ```
   LINT: [filename] — [issue description]
   ```

---

## 6. Lint — Full

**Scope:** Entire vault.

**When to run:** On user demand, or automatically after batch ingest.

### Checks

Run all incremental lint checks (1-4 above) on every page in the vault, then additionally:

5. **Orphan pages** — Identify any page in `entities/`, `concepts/`, `sources/`, `synthesis/`, or `events/` that has no inbound wikilinks from any other page. Flag these as orphans.

6. **Index completeness** — Every page in `entities/`, `concepts/`, `sources/`, `synthesis/`, and `events/` must have a corresponding entry in `index.md`. Flag any missing entries.

7. **MOC completeness** — Every page in a content folder must be listed in that folder's MOC file. Flag any missing MOC entries.

8. **Contradictions flag (best effort)** — Identify pages that contain claims that appear to contradict claims in other pages (e.g., conflicting dates, conflicting descriptions of the same entity). Flag potential contradictions for user review. This is a heuristic check; false positives are acceptable.

9. **Stale claims** — Identify source pages where a newer source on the same topic exists in the vault. Flag older sources that may have been superseded.

10. **Missing pages** — Identify `[[wikilinks]]` across all vault pages that reference a page that does not exist. These are candidates for stub pages.

### After Full Lint

Generate a lint report and append a summary to `log.md`:

```markdown
## [YYYY-MM-DD] lint | Full vault lint

- **Pages checked**: [N]
- **Issues found**: [N]
- **Orphan pages**: list
- **Missing index entries**: list
- **Missing MOC entries**: list
- **Broken wikilinks**: list
- **Potential contradictions**: list
- **Stale sources**: list
- **Missing pages (broken links)**: list
```

Report the full lint findings to the user with recommended actions.

---

## Log Format

All log entries follow this format:

```markdown
## [YYYY-MM-DD] operation | Description

- **Pages created**: list of page names (or "none")
- **Pages updated**: list of page names (or "none")
- **Issues**: description of any problems (or "none")
```

Valid operation types: `init`, `ingest`, `batch-ingest`, `query`, `lint`

---

## Cross-Reference Rules

Apply these rules consistently when creating or updating any vault page:

- Always use `[[Wikilinks]]` for internal vault references. Never use bare text when a vault page exists for that entity or concept.
- **Entity pages** must link to:
  - Related entities (other entities this entity is associated with)
  - Concepts the entity embodies or illustrates
  - Sources that mention the entity
- **Concept pages** must link to:
  - Related concepts
  - Entities that exemplify the concept
  - Sources that cover the concept
- **Source pages** must link to:
  - All entities extracted from the source
  - All concepts extracted from the source
- **Synthesis pages** must link to:
  - All sources consulted
  - All entities and concepts analyzed
- **Event pages** must link to:
  - Related entities involved in the event
  - Related concepts illustrated by the event

---

## Index Entry Format

When adding entries to `index.md`:

```markdown
- [[Page Name]] — brief one-line description
```

Examples:
```markdown
- [[Whatcom County Council]] — seven-member governing body for Whatcom County, WA
- [[Carbon Sequestration]] — process by which carbon dioxide is captured and stored
- [[2025-03-15 IPCC Sixth Assessment Report]] — synthesis report on climate science
```

---

## MOC Entry Format

When adding entries to a MOC file:

```markdown
- [[Page Name]]
```

MOC files are lists of wikilinks only — no descriptions. They provide navigational overview without duplication of index descriptions.
