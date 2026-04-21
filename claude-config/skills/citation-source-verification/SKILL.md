---
name: citation-source-verification
description: Systematic citation management, source verification, and academic integrity using zotero-cli tools and Obsidian integration
tags: [citation, sources, verification, academic, zotero, obsidian, research, zotero-cli]
version: 1.5.0
author: Gil Lund
created: 2025-11-10
updated: 2026-04-09
requires_cli: [zotero-cli>=1.5.0]
---

# Citation & Source Verification

## Purpose

Academic and professional writing demands rigorous source verification, accurate citations, and systematic tracking of references. This skill provides comprehensive patterns for managing citations, verifying sources, maintaining academic integrity, and building a knowledge base that links research to reliable sources.

**When to use this skill**:
- Academic research papers, literature reviews, and dissertations
- Professional reports requiring source attribution
- Content creation that needs fact-checking and citations
- Building a personal research knowledge base
- Verifying claims and tracking provenance of information
- Systematic literature analysis and synthesis

**When NOT to use this skill**:
- Casual blog posts or personal writing without citations
- Internal documentation where citations aren't required
- Creative writing or fiction

---

## Core Methodology

### The Three-Layer Verification System

**The Problem**: Writers often face:
- Lost sources and inability to re-find references
- Inconsistent citation formatting
- Difficulty verifying claims across multiple sources
- No systematic way to track source quality
- Citations that break or sources that disappear

**The Solution**: Three integrated layers

1. **Layer 1: Zotero (Source Truth)** - Central repository for all references
2. **Layer 2: Obsidian (Knowledge Network)** - Connected notes linking ideas to sources
3. **Layer 3: Verification Protocol** - Systematic source quality assessment

**Key Principles**:
1. **Single source of truth** - Zotero holds canonical citation data
2. **Bi-directional linking** - Notes link to sources, sources link to notes
3. **Verify before citing** - Check source quality and accuracy
4. **Track provenance** - Know where every claim comes from
5. **Maintain integrity** - Never cite what you haven't read

---

## Required Setup

### Zotero CLI Tools (Primary Interface)

**Scripts Location**: `scripts/zotero-cli/`

This skill uses **zotero-cli** Python scripts for all Zotero operations (read and write):

**Environment Variables** (Required):
```bash
# Set your Zotero API key and user ID
export ZOTERO_API_KEY=your_api_key_here
export ZOTERO_USER_ID=your_user_id_here
```

**Get your credentials**:
1. Go to https://www.zotero.org/settings/keys
2. Create new API key with **read/write access**
3. Note your User ID (shown on the keys page)

### Obsidian Citation Plugin Stack

Set up via the `obsidian-setup` skill. The citation pipeline requires:
- **Pandoc Reference List** plugin — renders `[@citekey]` inline in the editor
- **Zotero Integration** plugin — imports Zotero items as vault literature notes
- **Citations** plugin (optional) — BibTeX-based citekey search
- **BibTeX file** in vault root — exported from Zotero via Better BibTeX or Web API
- **Pandoc** installed (`brew install pandoc`)

See `~/.claude/skills/obsidian-setup/references/proven-citation-stack.md` for exact configuration.

### Available CLI Commands

**Available Scripts**:
- `zotero-verify-api` - Verify API credentials
- `zotero-create-collection` - Create collections
- `zotero-add-item` - Add items with metadata (with duplicate detection by DOI/title)
- `zotero-import-doi` - Import from DOI (with duplicate detection)
- `zotero-add-pdf` - Add PDF with metadata extraction, or attach PDF to existing item (v1.5.0+)
- `zotero-add-tags` - Tag existing items
- `zotero-update-item` - Update metadata (EXTENDED: authors, institution, place, report-type, publisher, series)
- `zotero-create-parent` - Create parent item for standalone PDFs
- `zotero-find-duplicates` - Find DOI-based duplicates
- `zotero-merge-duplicates` - Interactively merge duplicates

**Usage During Development**:
```bash
cd scripts/zotero-cli
uv run bin/zotero-import-doi 10.1234/example --tags "important"
```

**After Deployment** (via `install.sh`):
```bash
zotero-import-doi 10.1234/example --tags "important"
```

**Claude Code Integration**: Claude invokes these scripts via Bash tool during research workflows.

###  ⚠️ CRITICAL: Proper CLI Usage for Claude Code

**ALWAYS use zotero-cli commands directly via Bash tool.**

**Correct Usage:**
```bash
# Correct - Direct CLI command
zotero-add-item --type report \
  --title "City Executive Order 2024-01: Title" \
  --authors "City of Example" \
  --year "2024" \
  --url "https://example.gov/order.pdf" \
  --collection "my-collection" \
  --tags "tag1,tag2,tag3"
```

**IMPORTANT: Parameter Syntax**:
- Use `--authors` (plural) NOT `--author`
- Use `--tags` for comma-separated tags
- Use `--collection` to specify collection name
- Available types: `journalArticle`, `book`, `webpage`, `report`, `conferencePaper`

**For report type** (municipal orders, government documents):
- `--title`: Full title
- `--authors`: Author/organization name
- `--year`: Publication year
- `--url`: Document URL
- `--publisher`: Optional publisher name (NOT `--institution` for basic add)
- `--pages`: Optional page count
- `--tags`: Comma-separated tags (no spaces after commas)
- `--collection`: Collection name to add item to

**After adding, note the Zotero key returned** - you'll need it for linking in Obsidian.

**Common Mistakes to Avoid:**
- ❌ Using `--author` instead of `--authors`
- ❌ Using `--institution` with `zotero-add-item` (not available for basic add)
- ❌ Not specifying `--collection` (item won't be in your target collection)
- ❌ Forgetting to capture the returned Zotero key

**Workflow:**
1. Add item with `zotero-add-item` CLI → Get Zotero key (e.g., ABC123XYZ)
2. Create Obsidian note with frontmatter including `zotero-key: ABC123XYZ`
3. Add Zotero link: `[Open in Zotero](zotero://select/items/ABC123XYZ)`

---

## Core Patterns

### Pattern 1: Add Source to Zotero (Using CLI Scripts)

**Quick Add from DOI** (RECOMMENDED):
```bash
zotero-import-doi 10.1234/example --collection "Research Project" --tags "climate,policy"
```

**Manual Add** (with automatic duplicate detection):
```bash
# Automatically checks for duplicates by DOI or title
zotero-add-item --type journalArticle \
  --title "Paper Title" \
  --authors "Smith, John; Doe, Jane" \
  --year 2024 \
  --publication "Nature" \
  --doi "10.1234/example" \
  --collection "Research Project" \
  --tags "important"

# Force adding even if duplicate exists
zotero-add-item --type journalArticle \
  --title "Paper Title" \
  --authors "Smith, John; Doe, Jane" \
  --year 2024 \
  --force
```

**Duplicate Detection**:
- Checks by DOI if provided (most reliable)
- Falls back to exact title match (case-insensitive)
- Displays existing item details and exits with error
- Use `--force` flag to bypass duplicate checking

**Update Item with Extended Metadata** (v1.4.0+):
```bash
# Update with comprehensive metadata
zotero-update-item ITEM_KEY \
  --title "Full Report Title" \
  --author "Organization Name; Smith, Jane" \
  --year "2024" \
  --institution "Research Institute" \
  --place "City, State" \
  --report-type "Technical Report" \
  --abstract "Full abstract text..." \
  --url "https://example.org/report"

# Create parent for standalone PDF
zotero-create-parent PDF_ITEM_KEY \
  --title "Report Title" \
  --author "Organization Name" \
  --institution "Research Institute" \
  --year "2024"
```

**Author Format Options**:
- Individual: `"Lastname, Firstname"` or `"Firstname Lastname"`
- Organizational: `"Organization Name"` (no comma)
- Multiple: Separate with semicolons: `"Smith, John; WHO; Doe, Jane"`

**Example Workflow**:
```
User: "Add this paper: DOI 10.1234/example, collection 'Climate Research'"

Claude: [Runs zotero-import-doi script]
        "Added: 'Climate Strategies' by Smith et al. (2024)
         Item key: ABC123XYZ"
```

**Alternative: Browser/Desktop Entry**
If CLI scripts aren't deployed, use:

1. **Browser Extension**:
   - Install Zotero Connector browser extension
   - Click Zotero icon on paper webpage
   - Automatically saves to library

2. **DOI Import in Zotero Desktop**:
   - Click magic wand icon
   - Enter DOI
   - Zotero automatically retrieves metadata

**Verification Checklist**:
- [ ] Full citation information captured
- [ ] PDF attached (if available)
- [ ] DOI or URL recorded
- [ ] Tags added for classification
- [ ] Collection assigned

**Attach PDF to Existing Item** (v1.5.0+):

When you have a Zotero item but need to attach a PDF:
```bash
# Non-interactive: attach PDF without metadata prompts
zotero-add-pdf /path/to/paper.pdf --item-key ABC123 --attach-only

# Download and attach from URL
zotero-add-pdf --url https://example.com/paper.pdf --item-key ABC123 --attach-only
```

This is useful for:
- Adding PDFs found after initial citation import
- Attaching open-access versions to paywall citations
- Bulk attaching PDFs to imported DOI references
- Scripted/automated PDF attachment workflows

**Interactive mode** (for new items):
```bash
# Full interactive: extracts metadata from PDF and prompts for confirmation
zotero-add-pdf document.pdf --collection "Research" --tags "review"
```

---

### Pattern 2: Search Existing Sources

**When**: Need to find sources you've already collected

**By Topic**:
```
"Search my Zotero library for papers about machine learning interpretability"
```

**By Author**:
```
"Find all papers by Yoshua Bengio in my library"
```

**By Date Range**:
```
"Show me papers I added to Zotero last week"
```

**By Tag**:
```
"List all sources tagged 'climate-change' in my Zotero"
```

**By Collection**:
```
"What papers are in my 'Dissertation - Chapter 3' collection?"
```

---

### Pattern 3: Verify Source Quality

**When**: Before citing a source in your work

**The 5-Point Verification Protocol**:

1. **Authority**: Who is the author?
   ```
   "Check the credentials of the author [Author Name] for this paper"
   ```
   - Academic affiliation?
   - Relevant expertise?
   - Citation count?

2. **Currency**: How recent is the information?
   ```
   "Find more recent papers on [topic] since [year]"
   ```
   - Is it current for the field?
   - Has it been superseded?

3. **Accuracy**: Can claims be verified?
   ```
   "Find other sources that confirm/contradict the claim that [specific claim]"
   ```
   - Cross-reference with other sources
   - Check for retractions
   - Verify key statistics

4. **Purpose**: Why was this created?
   ```
   "Analyze the funding sources and potential biases for this study"
   ```
   - Funding sources?
   - Conflicts of interest?
   - Peer-reviewed?

5. **Coverage**: Is treatment comprehensive?
   ```
   "Compare the coverage of [topic] in this source versus [other source]"
   ```
   - Depth appropriate for your needs?
   - Important aspects omitted?

**Example Full Verification**:
```
"I want to cite this claim: '[specific claim]' from [Source].
Please help me verify:
1. Author credentials
2. If claim is supported by other sources
3. Any known issues with this source
4. More recent research on this topic"
```

---

### Pattern 4: Create Citation in Multiple Formats

**When**: Need to cite a source in your writing

**Get Citation**:
```
"Generate citations for [Paper Title] in:
- APA 7th edition
- Chicago style
- Nature format
- MLA format"
```

**Inline Citation**:
```
"Give me the inline citation for [Paper Title] in APA format"
```
Output: `(Smith & Jones, 2024)`

**Full Bibliography Entry**:
```
"Generate the bibliography entry for [Paper Title] in Chicago style"
```

**BibTeX Export** (for LaTeX):
```
"Export this Zotero item as BibTeX"
```

---

### Pattern 5: Build Connected Knowledge in Obsidian

**When**: Taking notes from sources and linking ideas

**Create Source Note**:
```
"Create an Obsidian note for this paper:
Title: [Paper Title]
Key findings: [1-3 sentences]
Link to Zotero item key: [ITEM_KEY]
My thoughts: [your analysis]"
```

**Link Notes to Sources**:
```markdown
# My Research Note

This claim is supported by [[Smith2024]] who found that...

^source: zotero://select/items/@smith2024
```

**Create Literature Note Template**:
```markdown
---
type: literature-note
source: zotero://select/items/[ITEM_KEY]
date-read: 2025-11-10
rating: 4/5
tags: [machine-learning, interpretability]
---

# [Paper Title]

## Bibliographic Information
- **Authors**:
- **Year**:
- **DOI**:
- **Zotero Link**:

## Summary
[3-5 sentence summary in your own words]

## Key Findings
1.
2.
3.

## Methodology
[Brief description of methods used]

## Strengths
-

## Weaknesses
-

## Relevance to My Work
[How this connects to your research]

## Key Quotes
> "Quote here" (p. XX)

> "Another quote" (p. XX)

## Related Papers
- [[Other Paper 1]]
- [[Other Paper 2]]

## Follow-up Questions
-
```

---

### Pattern 6: Literature Review Workflow

**When**: Conducting systematic literature review

**Phase 1: Collection**
```
"Help me build a literature review on [topic]:
1. Search my Zotero for existing papers on [topic]
2. Identify gaps in coverage
3. Suggest search terms for finding additional sources"
```

**Phase 2: Organization**
```
"Create a Zotero collection called '[Topic] Literature Review'
and help me categorize papers by:
- Methodology
- Key findings
- Publication date"
```

**Phase 3: Synthesis**
```
"Analyze these 10 papers from my Zotero collection and:
1. Identify common themes
2. Find contradictions or debates
3. Trace development of ideas over time
4. Identify seminal papers that are frequently cited"
```

**Phase 4: Writing**
```
"Generate an outline for a literature review on [topic] based on
the papers in my Zotero collection, organized by:
- Chronological development
- Thematic categories
- Methodological approaches"
```

---

### Pattern 7: Fact-Checking Workflow

**When**: Verifying claims before publishing

**Single Claim Verification**:
```
"I want to verify this claim: '[specific claim]'

Please:
1. Search my Zotero for sources that support or contradict it
2. If not in my library, suggest authoritative sources to check
3. Assess the quality of evidence for this claim
4. Identify any important caveats or limitations"
```

**Multi-Source Triangulation**:
```
"Compare how these three sources treat [topic]:
1. [Source 1]
2. [Source 2]
3. [Source 3]

Identify:
- Points of agreement
- Points of disagreement
- Gaps in coverage
- Which source is most authoritative"
```

**Claim Provenance Tracking**:
```
"Trace the original source of this claim: '[claim]'

Questions:
- Who first published this?
- Has it been replicated?
- Are there better/more recent sources?
- Is it being cited accurately?"
```

---

### Pattern 8: Managing Standalone PDFs (v1.4.0+)

**When**: You have PDF files in Zotero without proper bibliographic parent items

**The Problem**: PDFs added directly to Zotero lack proper metadata and citation information. They appear as standalone attachments rather than organized bibliographic entries.

**Find Standalone PDFs**:
```bash
# Batch mode - shows all standalone PDFs
zotero-create-parent --batch
```

**Create Parent for Single PDF**:
```bash
# Interactive mode - prompts for metadata
zotero-create-parent PDF_ITEM_KEY

# Non-interactive with full metadata
zotero-create-parent PDF_ITEM_KEY \
  --title "Report Title" \
  --author "World Health Organization" \
  --year "2024" \
  --institution "WHO" \
  --place "Geneva" \
  --item-type "report"
```

**Workflow Example**:
```
1. User drops PDF into Zotero (becomes standalone attachment)
2. Run: zotero-create-parent --batch
3. System shows list of standalone PDFs
4. For each PDF:
   - System suggests title from PDF filename
   - User provides: authors, year, institution, etc.
   - System creates proper bibliographic entry
   - PDF becomes child attachment of entry
5. Result: Properly cited source with PDF attached
```

**Benefits**:
- Converts informal PDF collections into proper library
- Enables proper citation generation
- Maintains PDF file and any annotations
- Equivalent to Zotero GUI's "Create Parent Item" feature

**Best Practice**:
```bash
# Weekly cleanup of standalone PDFs
zotero-create-parent --batch

# Then verify metadata quality
zotero-search-items "type:report" --limit 10
```

---

## Best Practices

### ✅ Do This

1. **Cite What You Read**
   - Never cite a source you haven't actually read
   - If citing a secondary source, make it clear
   ```
   Smith (2020, as cited in Jones, 2024) found that...
   ```

2. **Maintain Metadata Quality**
   - Fill in all Zotero fields completely
   - Add tags immediately when adding sources
   - Attach PDFs when available
   - Add personal notes about relevance

3. **Use Collections for Projects**
   ```
   Zotero Library/
   ├── 📁 Dissertation/
   │   ├── 📁 Chapter 1 - Background
   │   ├── 📁 Chapter 2 - Methods
   │   └── 📁 Chapter 3 - Analysis
   ├── 📁 Paper - Climate Adaptation
   └── 📁 General Reading
   ```

4. **Link Everything**
   - Link Obsidian notes to Zotero items
   - Link related papers together
   - Create concept maps showing relationships
   - Use bidirectional links: `[[Source]]` and `^source:`

5. **Regular Verification Schedule**
   ```
   Weekly: Check new sources for quality
   Monthly: Re-verify key claims in ongoing work
   Before submission: Full verification pass
   ```

6. **Use Citation Key Naming Convention**
   - Format: `author_year_keyword`
   - Example: `smith_2024_machine_learning`
   - Makes citations searchable and memorable

7. **Track Citation Context**
   - Note *why* you're citing each source
   - Tag with purpose: `#methodology`, `#supporting-evidence`, `#counterpoint`

8. **Backup Your Library**
   ```bash
   # Zotero sync (automatic via Zotero account)
   # Local backup
   cp -r ~/Zotero ~/Backups/Zotero-$(date +%Y-%m-%d)
   ```

---

### ❌ Avoid This

1. **Don't Cite Without Reading**
   ```
   ❌ BAD: "Studies show X (Smith 2024, Jones 2023, Brown 2022)"
          (Never actually read these papers)

   ✅ GOOD: "Smith (2024) found X in a study of Y..."
           (Read and understood the actual study)
   ```

2. **Don't Trust Citations Blindly**
   ```
   ❌ BAD: Cite a paper because another paper cited it

   ✅ GOOD: Verify the original source and check context
   ```

3. **Don't Mix Citation Styles**
   ```
   ❌ BAD: APA in paragraph 1, MLA in paragraph 2

   ✅ GOOD: Choose one style and stick to it
   ```

4. **Don't Lose Track of Sources**
   ```
   ❌ BAD: "I read something about this somewhere..."

   ✅ GOOD: Add to Zotero immediately when you find it
   ```

5. **Don't Over-rely on Secondary Sources**
   ```
   ❌ BAD: Only read review papers, never primary research

   ✅ GOOD: Read key primary sources yourself
   ```

6. **Don't Ignore Retractions**
   ```
   ❌ BAD: Continue citing retracted papers

   ✅ GOOD: Check for retractions before citing
           Use tools like RetractionWatch
   ```

7. **Don't Cherry-Pick Evidence**
   ```
   ❌ BAD: Only cite sources that support your position

   ✅ GOOD: Present full picture including contradictory findings
   ```

---

## Common Scenarios

For detailed workflows, read `references/workflows-and-scenarios.md`. Summary:

| Scenario | When |
|----------|------|
| Starting a Research Project | New dissertation chapter, major paper |
| Fact-Checking Before Publication | Article ready to submit |
| Building a Literature Review | Systematic review of 50+ papers |
| Verifying a Controversial Claim | Surprising finding needs deep verification |

See `references/workflows-and-scenarios.md` for detailed walkthroughs of all four scenarios.

---

## Obsidian Integration

### Citation Rendering

The Pandoc Reference List plugin renders `[@citekey]` citations inline in the Obsidian editor. This requires:
- A `.bib` file in the vault (exported from Zotero)
- Pandoc installed (`/opt/homebrew/bin/pandoc`)
- Plugin configured with bibliography path and CSL style

**After adding sources to Zotero, refresh the BibTeX file:**
```bash
# Via Zotero Web API
curl -H "Zotero-API-Key: $ZOTERO_API_KEY" \
  "https://api.zotero.org/users/$ZOTERO_USER_ID/collections/COLLECTION_KEY/items?format=bibtex" \
  > vault/citations.bib
```
Or use Better BibTeX auto-export (updates when Zotero desktop is running).

### Creating Literature Notes

Use the Zotero Integration plugin (Cmd+P → "Zotero Integration: Create literature note") to import items with the Handlebars template from `obsidian-setup`. This auto-populates metadata, abstract, and annotation sections.

For the template, see `~/.claude/skills/obsidian-setup/templates/Zotero-Literature-Note.md`.

### Vault-Keeper Handoff

After verifying and importing a source to Zotero:
1. Import as literature note via Zotero Integration plugin
2. Use `obsidian-vault-keeper` ingest to create a source page with `[@citekey]` references
3. The source page cross-references entity and concept pages in the vault

### Citation Styles

| Style | Inline | Common In | CSL File |
|-------|--------|-----------|----------|
| IEEE | [1] | Engineering, CS | `ieee.csl` |
| Vancouver | superscript ¹ | Medicine, JCRS, ASCRS | `vancouver.csl` |
| APA | (Smith et al., 2024) | Social sciences | `apa.csl` |
| Nature | superscript ¹ | Natural sciences | `nature.csl` |

CSL styles from: `https://raw.githubusercontent.com/citation-style-language/styles/master/{style}.csl`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't find a source | Search Zotero by keyword, author, date range. Add to Zotero immediately when found. |
| Source quality unclear | Run 5-Point Verification Protocol. Check Beall's List for predatory journals. |
| Citations not rendering | Check Pandoc Reference List plugin: bibliography path, pandoc path, `pullFromZotero` toggle. |
| Lost link between note and source | Search Zotero by title/author, update note frontmatter with `zotero-key` and `[@citekey]`. |
| BibTeX file stale | Re-export from Zotero or refresh via Web API `curl` command above. |

For advanced techniques (citation network analysis, temporal trends, comparative analysis, gap identification), see `references/workflows-and-scenarios.md`.

---

## Integration with Other Skills

| Skill | Role in Pipeline |
|-------|-----------------|
| `obsidian-setup` | Provisions vault with citation plugin stack (Pandoc Reference List, Zotero Integration, Citations). Must be run first. See `references/proven-citation-stack.md` for plugin configs. |
| `obsidian-vault-keeper` | After citation-source-verification adds/verifies sources in Zotero, vault-keeper creates source/entity/concept pages with `[@citekey]` references. |
| `literature-review` | Systematic literature search across PubMed, arXiv, Semantic Scholar. Use to find sources, then use this skill to verify and add to Zotero. |
| `configuration-management` | Store Zotero API credentials in environment variables. |

### Pipeline Flow

```
1. Find sources        → literature-review skill or manual search
2. Verify & add        → citation-source-verification (this skill) + zotero-cli
3. Refresh BibTeX      → curl or Better BibTeX auto-export
4. Import to vault     → Zotero Integration plugin (Obsidian)
5. Create vault pages  → obsidian-vault-keeper ingest with [@citekey] citations
6. Render citations    → Pandoc Reference List plugin (live in editor)
```

---

## Included Assets

### References
- `references/workflows-and-scenarios.md` — Detailed scenario walkthroughs, advanced techniques, templates, quality checklist

---

## References & Resources

- **Zotero**: https://www.zotero.org/support/
- **Pandoc Reference List Plugin**: https://github.com/mgmeyers/obsidian-pandoc-reference-list
- **Zotero Integration Plugin**: https://github.com/mgmeyers/obsidian-zotero-integration
- **Better BibTeX**: https://retorque.re/zotero-better-bibtex/
- **CSL Styles**: https://github.com/citation-style-language/styles
- **RetractionWatch**: https://retractionwatch.com/

---

## Version History

### 1.5.0 (2026-04-09)
- **Integrated with obsidian-setup and vault-keeper skills** — full pipeline documentation
  - Added Obsidian Citation Plugin Stack to Required Setup (replaces Local REST API)
  - Added BibTeX refresh step after Zotero imports
  - Added vault-keeper handoff workflow
  - Added pipeline flow diagram (find → verify → refresh → import → ingest → render)
- **Added citation style comparison** — IEEE, Vancouver, APA, Nature with CSL URLs
- **Moved bulk content to `references/workflows-and-scenarios.md`** — scenarios, advanced techniques, templates, quality checklist (SKILL.md reduced from 1,461 to ~490 lines)
- Updated Integration section with skill pipeline table
- Removed stale Local REST API and manual template sections
- Added Included Assets section

### 1.4.0 (2026-02-09)
- **Added zotero-add-pdf documentation** with `--attach-only` flag
  - Non-interactive PDF attachment to existing Zotero items
  - Enables scripted/automated workflows without stdin prompts
  - Supports both local files and URL downloads
- Updated requires_cli to zotero-cli v1.5.0+

### 1.3.0 (2025-12-11)
- **Removed Zotero MCP dependency** - now uses zotero-cli exclusively
  - All operations (read and write) via CLI tools
  - Simplified setup without MCP server configuration
  - More reliable and consistent interface
- Updated documentation to reflect CLI-only workflow
- Removed MCP-specific sections and references

### 1.2.0 (2025-11-23)
- Enhanced duplicate detection in zotero-add-item
  - Automatic checking by DOI (if provided) or exact title match
  - Shows existing item details with authors, year, and item key
  - Requires `--force` flag to bypass duplicate prevention
  - Prevents accidental duplicate entries in manual workflows
- zotero-cli v1.4.1+ integration

### 1.1.0 (2025-11-22)
- Added Pattern 8: Managing Standalone PDFs
- Updated zotero-update-item with extended metadata fields
  - Author/creator parsing (individual and organizational)
  - Institution, place, report-type, publisher, series fields
  - Item-type-specific validation
- Added zotero-create-parent for converting standalone PDFs
- Added duplicate detection and merging capabilities
- zotero-cli v1.4.0 integration

### 1.0.0 (2025-11-10)
- Initial release
- Zotero integration patterns
- Obsidian integration patterns
- 5-Point Verification Protocol
- Literature review workflows
- Source quality assessment

---

**Last Updated**: 2026-04-09
**Maintainer**: Gil Lund
**License**: MIT
**CLI Tools**: zotero-cli v1.5.0+ (required)
**Companion Skills**: obsidian-setup (vault provisioning), obsidian-vault-keeper (ongoing vault operations)
