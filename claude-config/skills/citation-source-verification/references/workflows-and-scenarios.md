# Citation Workflows and Scenarios

Extended reference for common citation management scenarios, advanced techniques, templates, and quality checklists. Read this file when working on a specific scenario type.

---

## Scenario 1: Starting a New Research Project

**Context**: Beginning dissertation chapter or major paper

1. Create Zotero collection + Obsidian folder structure
2. Search existing library, identify gaps
3. Expand collection (seminal papers, recent reviews, methodological papers)
4. For each paper: create literature note via Zotero Integration plugin (Cmd+P → "Zotero Integration: Create literature note")
5. Tag by methodology, geographic focus, importance
6. Create synthesis map in vault showing themes and relationships
7. Export BibTeX file for Pandoc Reference List rendering

---

## Scenario 2: Fact-Checking Before Publication

1. Extract all factual claims needing citations from draft
2. For each claim: verify source authority, currency, accuracy
3. Check for retractions (RetractionWatch, DOI lookup)
4. Verify statistics against original source
5. Cross-reference key claims with 2-3 additional sources
6. Run 5-Point Verification Protocol on any weak sources

---

## Scenario 3: Building a Literature Review

**Phase 1 — Collection** (Week 1-2):
- Search Zotero + external databases
- Create collection structure by themes
- Add 20-30 papers to reach saturation

**Phase 2 — Analysis** (Week 3):
- Thematic analysis: major themes, under-researched areas
- Methodological analysis: common methods, gaps
- Temporal analysis: evolution of field, turning points
- Citation analysis: influential papers, clusters

**Phase 3 — Synthesis** (Week 4):
- Generate literature review outline
- Gap analysis and research question refinement
- Include `[@citekey]` citations from Zotero collection

---

## Scenario 4: Verifying a Controversial Claim

**Deep Verification Protocol:**

1. **Source Assessment** — Author credentials, venue, peer review, funding, citation count
2. **Primary Source Check** — Is source citing from another? Verify original
3. **Evidence Quality** — Study design, sample size, statistical significance, effect size
4. **Corroboration** — 3-5 independent sources supporting or contradicting
5. **Expert Opinion** — Recent reviews, meta-analyses, current consensus
6. **Temporal Check** — More recent research that updates or challenges finding

**Decision Matrix:**
- STRONG: Multiple independent sources confirm → cite with confidence
- MODERATE: Some support with caveats → cite with limitations noted
- WEAK: Contradicted or unverifiable → don't cite, or note as historical only

---

## Advanced Techniques

### Citation Network Analysis
Analyze citation patterns in a Zotero collection: most-cited papers, clusters, gaps, papers to add based on frequent citations.

### Temporal Trend Analysis
Organize papers by publication year, identify shifts in consensus, emergence of new methods, development of key concepts.

### Comparative Source Analysis
Compare 3+ papers on same topic: methodology differences, sample sizes, key findings, contradictions, which is most authoritative.

### Literature Gap Identification
From a collection: what's well-covered, under-researched, underrepresented populations, missing methodologies, potential research questions.

---

## Templates

### Literature Note Template

For manual creation (not via Zotero Integration plugin). For the Zotero Integration Handlebars template, see `obsidian-setup` skill at `~/.claude/skills/obsidian-setup/templates/Zotero-Literature-Note.md`.

```markdown
---
type: literature-note
zotero_key: ITEM_KEY
source_type: journalArticle
date_read: YYYY-MM-DD
rating: /5
status: unread
tags_yaml: [literature]
---

Tags: #literature

# Paper Title

**Authors**:
**Year**:
**DOI**:
**Zotero**: [Open in Zotero](zotero://select/items/ITEM_KEY)
**Cite as**: [@citekey]

## Summary
3-5 sentence summary in your own words.

## Key Findings
1.
2.
3.

## Methodology

## Strengths

## Limitations

## Relevance to Project

## Key Quotes
> "Quote" (p. XX)

## Related Literature
- [[]]
```

### Source Verification Checklist

```markdown
# Source Verification: SOURCE_NAME

## Basic Information
- **Title**:
- **Author(s)**:
- **Publication**:
- **Date**:
- **DOI/URL**:

## 5-Point Verification

### 1. Authority
- [ ] Author credentials verified
- [ ] Institutional affiliation checked
- [ ] Expertise relevant to topic

### 2. Currency
- [ ] Publication date appropriate
- [ ] Not superseded by newer research

### 3. Accuracy
- [ ] Claims cross-referenced
- [ ] Statistics verified
- [ ] No known retractions

### 4. Purpose
- [ ] Funding sources identified
- [ ] Conflicts of interest noted
- [ ] Peer-reviewed

### 5. Coverage
- [ ] Depth appropriate
- [ ] Limitations acknowledged

## Assessment
- [ ] Cite with confidence
- [ ] Cite with caveats
- [ ] Do not cite
```

---

## Quality Control Checklist (Before Submission)

- [ ] All claims have citations (no unsourced "studies show...")
- [ ] All sources read and understood (not citing from abstracts only)
- [ ] Citations consistently formatted (one style throughout)
- [ ] Sources are high quality (authoritative, peer-reviewed, current)
- [ ] No retracted sources (checked RetractionWatch)
- [ ] Key claims verified with multiple sources
- [ ] Proper attribution (quotes with page numbers, paraphrasing distinct from original)
- [ ] Zotero library organized (collections, metadata, tags)
- [ ] BibTeX file refreshed (reflects latest Zotero additions)
- [ ] Vault notes linked to sources via `[@citekey]` and `[[wikilinks]]`

---

**Last Updated:** 2026-04-09
