# Citation & Source Verification Implementation Playbook
## CEDS SWOT Analysis for Whatcom County, WA

**Project Type**: Economic Development Strategic Planning
**Document Type**: SWOT Analysis with cited sources
**Timeline**: 2-3 hours initial setup, ongoing use
**Goal**: Extract, verify, and organize citations from existing CEDS SWOT documents

---

## Overview

This playbook helps you implement the Citation & Source Verification skill on an existing project with citations that need to be extracted, organized, and verified.

**Your Situation**:
- You have a Claude project for Whatcom County CEDS SWOT analysis
- Documents contain resources and citations (not yet in Zotero)
- Empty Zotero library (fresh start)
- Need to systematically extract and verify sources

**What You'll Accomplish**:
1. Extract all citations from existing CEDS SWOT documents
2. Add sources to Zotero with proper metadata
3. Verify source quality and reliability
4. Create connected knowledge base in Obsidian
5. Identify gaps and missing citations
6. Establish citation tracking system for ongoing work

---

## Prerequisites & Setup

### Required Software

1. **Zotero Desktop Application**
   - Download: https://www.zotero.org/download/
   - Install the desktop application
   - Create a free Zotero account if you don't have one

2. **Obsidian** (Recommended)
   - Download: https://obsidian.md/
   - Install "Local REST API" plugin:
     - Open Obsidian Settings → Community Plugins
     - Browse plugins → Search "Local REST API"
     - Install and Enable
     - Configure API key in plugin settings (Settings → Local REST API)
     - Note the port (default: 27124)

### API Keys Configuration

The citation-source-verification skill requires API keys that should be configured **globally** so they work across all your Claude Code projects.

#### Step 1: Get Your Zotero Credentials

1. Go to https://www.zotero.org/settings/keys
2. Click "Create new private key"
3. Settings for the key:
   - **Name**: Claude Code Skills
   - **Personal Library**: Allow library access (read/write)
   - **Group Permissions**: As needed
   - Click "Save Key"
4. **Copy your API key** (you won't be able to see it again!)
5. **Note your User ID** (shown at the top of the keys page)

#### Step 2: Get Your Obsidian API Key (Optional but Recommended)

1. Open Obsidian
2. Go to Settings → Community Plugins → Local REST API
3. Copy the **API Key** shown in the settings
4. Note the **Port** (default: 27124)

#### Step 3: Add API Keys to Your Shell Environment

Your API keys are already configured in `~/.zshrc` if you followed the setup. If not, or if you need to update them:

**Edit `~/.zshrc`:**
```bash
# Zotero Configuration
export ZOTERO_API_KEY=your_api_key_here
export ZOTERO_USER_ID=your_user_id_here

# Obsidian Configuration (optional)
export OBSIDIAN_API_URL=https://127.0.0.1:27124
export OBSIDIAN_API_KEY=your_obsidian_api_key_here
```

**Apply changes:**
```bash
source ~/.zshrc
```

Or restart your terminal.

#### Step 4: Install zotero-cli Tools

The skill uses zotero-cli Python scripts for Zotero operations:

```bash
# Navigate to the scripts directory
cd /path/to/claude-skills/scripts/zotero-cli

# Install with uv
uv sync

# Or install globally
./install.sh
```

**Verify installation**:
```bash
zotero-verify-api
```

#### Step 5: Test the Connection

In any Claude Code project, test that the skill can access your Zotero library:

```
Search my Zotero library for recent items
```

If you get an error about missing API keys, verify:
1. `~/.zshrc` has the correct `export` statements
2. You've run `source ~/.zshrc` or opened a new terminal
3. Claude Code was started after setting the environment variables

---

## Using This Playbook

### How to Access This Playbook

This playbook is available in two ways:

1. **From the Skill Documentation**:
   - Located at: `claude-skills/skills/citation-source-verification/CEDS-SWOT-Implementation-Playbook.md`
   - You can reference it anytime with: `@claude-skills/skills/citation-source-verification/CEDS-SWOT-Implementation-Playbook.md`

2. **Copy to Your CEDS Project**:
   - Copy this playbook to your CEDS project folder as a reference
   - Customize it for your specific project needs
   - Track progress by checking off steps as you complete them

### How to Use the Citation Skill

Once setup is complete, you can invoke the citation-source-verification skill in any project:

**Example prompts:**
```
"Search my Zotero library for papers about economic development"

"Add this source to my Zotero library: [paste DOI or URL]"

"Verify the quality of this source using the 5-Point Verification Protocol"

"Create an Obsidian literature note for Zotero item [KEY]"
```

**The skill provides:**
- Citation extraction from documents
- Source quality verification (5-Point Protocol)
- Zotero library management
- Obsidian note creation
- Bibliography generation in multiple formats

---

## Phase 1: Assessment & Extraction (30-45 minutes)

### Step 1: Document Inventory

**Prompt**:
```
I have a Claude project for writing a CEDS SWOT analysis for Whatcom County, WA.

First, help me inventory what documents exist:
1. List all documents in the project
2. For each document, identify:
   - Document type (background research, analysis, draft sections)
   - Whether it contains citations or sources
   - Approximate number of citations
3. Prioritize which documents to process first (most citations, most critical)
```

**Expected Output**:
- Complete list of project documents
- Citation counts per document
- Processing priority order

---

### Step 2: Extract All Citations

**For each high-priority document**:

**Prompt**:
```
For document: [DOCUMENT_NAME]

Extract all citations, sources, and references:

1. Explicit Citations:
   - Formal citations with author, date, title
   - URLs and web sources
   - Government reports and documents
   - Statistical sources

2. Implicit Sources:
   - Facts that need citations (but don't have them yet)
   - Statistics without attribution
   - Claims about Whatcom County that need sources

3. For each citation found, provide:
   - Source type (academic paper, government report, news article, website, data)
   - Available metadata (author, year, title, URL)
   - Context: What claim does it support?
   - Page/section where found
   - Quality assessment (appears reliable, needs verification, questionable)

Format as a structured list I can use to build my Zotero library.
```

**Expected Output**:
- 10-30 citations per document (varies)
- Structured list ready for Zotero import
- Identification of unsourced claims

**Save Output**: Copy to `CEDS-Citations-Extracted.md` for reference

---

### Step 3: Identify Critical Gaps

**Prompt**:
```
Based on the extracted citations and the purpose of a CEDS SWOT analysis,
identify critical gaps:

1. What types of sources are missing?
   - Economic data for Whatcom County
   - Demographic statistics
   - Industry sector analysis
   - Workforce data
   - Infrastructure assessments

2. What claims in the SWOT lack proper sources?
   - Strengths without evidence
   - Weaknesses without data
   - Opportunities without research backing
   - Threats without documented trends

3. What authoritative sources should be included?
   - US Census Bureau data
   - WA State Office of Financial Management
   - Whatcom County economic reports
   - Port of Bellingham data
   - Educational institution reports (WWU, BTC, etc.)

Create a prioritized list of sources to find and add.
```

**Expected Output**:
- Gap analysis
- Prioritized list of needed sources
- Recommended authoritative sources for Whatcom County economic data

---

## Phase 2: Zotero Library Setup (45-60 minutes)

### zotero-cli Provides Full Read/Write Access

The zotero-cli tools provide **complete read and write** access to your Zotero library:

**Write Operations** (via CLI):
- Add new sources (`zotero-add-item`, `zotero-import-doi`)
- Create collections (`zotero-create-collection`)
- Add tags (`zotero-add-tags`)
- Update metadata (`zotero-update-item`)
- Create parent items for PDFs (`zotero-create-parent`)

**Read Operations** (via CLI):
- Search your library (`zotero-search-items`)
- Retrieve metadata (`zotero-get-item`)
- Find duplicates (`zotero-find-duplicates`)

**Workflow**: Claude Code uses zotero-cli for all Zotero operations directly

---

### Step 4: Create Zotero Collection Structure

**Manual Step in Zotero Desktop**:
Open Zotero desktop app and create this collection structure:

1. Main Collection: "Whatcom County CEDS 2025"

2. Sub-collections by source type:
   - Economic Data & Statistics
   - Demographic Data
   - Industry & Sector Analysis
   - Workforce & Education
   - Infrastructure & Transportation
   - Government Reports & Plans
   - News & Media
   - Academic Research

3. Sub-collections by SWOT component:
   - Strengths - Supporting Evidence
   - Weaknesses - Supporting Evidence
   - Opportunities - Supporting Evidence
   - Threats - Supporting Evidence

**Then with Claude Code**, verify the structure:
```
"List the collections in my Zotero library"
```

---

### Step 5: Add Sources to Zotero - Batch 1 (Government & Data)

**Start with highest-quality, most critical sources first**

**Step 5a: Research and Verify Sources with Claude**

**Prompt**:
```
From my extracted citations, let's research the government and statistical sources.

For each source in this category:
1. Find the official URL or DOI
2. Verify it's still accessible
3. Provide the complete metadata:
   - Item type (report, webpage, dataset)
   - Title
   - Authors/Organization
   - Date
   - URL
   - Abstract/Description
   - Suggested tags
   - Which collection(s) to add it to

Start with these sources:
[Paste 5-10 government/statistical sources from your extraction]

For each, also note:
- How current is this data?
- Is there a more recent version?
- Should I use this source or find an update?
```

**Step 5b: Add to Zotero Manually**

For each verified source, use one of these methods:

1. **Browser Connector** (RECOMMENDED - Fastest):
   - Navigate to the source URL
   - Click Zotero Connector icon in browser
   - Automatically saves with metadata
   - Move to appropriate collection in Zotero

2. **Manual Entry** (when browser connector doesn't work):
   - Open Zotero desktop app
   - Click green "+" button → Select item type
   - Fill in fields using Claude's metadata
   - Add to appropriate collections
   - Apply tags

**Step 5c: Verify in Claude Code**:
```
"Search my Zotero library for sources about Whatcom County economic data"
"Show me items in the 'Economic Data & Statistics' collection"
```

---

### Step 6: Add Sources - Batch 2 (Reports & Documents)

**Repeat the same process for reports, plans, and documents**

**Prompt**:
```
Next batch: Regional reports and planning documents.

For these sources:
[Paste report/document citations]

For each:
1. Verify source authenticity and authority
2. Check for updated versions
3. Provide Zotero entry details
4. Assess quality using the 5-Point Verification Protocol:
   - Authority (who created it?)
   - Currency (how recent?)
   - Accuracy (peer reviewed? data source?)
   - Purpose (why was it created? biases?)
   - Coverage (comprehensive enough?)

Flag any sources that fail verification.
```

---

### Step 7: Add Sources - Batch 3 (News, Media, Web)

**Final batch: Lower-tier sources that still need tracking**

**Prompt**:
```
Final batch: News articles, blog posts, and general web sources.

For these sources:
[Paste news/web citations]

For each:
1. Verify source is still accessible (check for link rot)
2. Use Wayback Machine for archived copies if needed
3. Assess credibility of publication/website
4. Provide Zotero entry with:
   - Snapshot/PDF attachment if important
   - Note on reliability
   - Replacement suggestions if source is questionable

Note: Some of these may need to be replaced with more authoritative sources.
```

---

## Phase 3: Source Verification & Quality Control (30-45 minutes)

### Step 8: Run 5-Point Verification on Key Sources

**For your 10 most critical sources**:

**Prompt**:
```
Run the 5-Point Verification Protocol on this critical source:

Source: [Title, Author, Year]
Zotero Key: [KEY]
Used to support: [What SWOT claim?]

Verification Protocol:
1. AUTHORITY
   - Who is the author/organization?
   - What are their credentials/expertise?
   - Why should we trust this source?
   - Citation count or influence in field?

2. CURRENCY
   - Publication date: [YEAR]
   - Is this data still current for 2025 CEDS?
   - Are there more recent updates or reports?
   - For economic/demographic data: Is this outdated?

3. ACCURACY
   - Can claims be cross-referenced?
   - What's the methodology? Sound?
   - Any known corrections or retractions?
   - Do other sources confirm the findings?

4. PURPOSE
   - Why was this source created?
   - Who funded it? Conflicts of interest?
   - Is there potential bias?
   - Is it advocacy or objective analysis?

5. COVERAGE
   - Does it cover Whatcom County specifically?
   - Is depth appropriate for CEDS use?
   - Are important aspects omitted?
   - Geographic/temporal scope appropriate?

RECOMMENDATION:
- ✅ Cite with confidence
- ⚠️ Cite with caveats (specify)
- ❌ Do not cite (explain why + suggest replacement)
```

**Create verification notes in Obsidian**: `Research/CEDS-SWOT/Source-Verification/[Source-Name].md`

---

### Step 9: Cross-Reference Critical Claims

**For major SWOT claims**:

**Prompt**:
```
I want to verify this critical claim in my SWOT analysis:

CLAIM: "[Specific claim from your SWOT, e.g., 'Whatcom County has experienced 15% population growth in the last decade']"

CURRENT SOURCE: [Source name]

Help me verify:
1. Search my Zotero library: Do I have other sources that confirm/contradict this?
2. If only one source: Find 2-3 additional authoritative sources to confirm
3. Check if the statistic is accurate:
   - Verify the number (15% in this example)
   - Verify the timeframe ("last decade")
   - Check if there's more recent data
4. Assess:
   - Is this claim well-supported?
   - Do I need additional sources?
   - Should I modify the claim based on evidence?

Recommendation for how to cite this in the CEDS SWOT.
```

---

### Step 10: Identify and Fix Citation Gaps

**Prompt**:
```
Review my CEDS SWOT draft and current Zotero library.

For each section (Strengths, Weaknesses, Opportunities, Threats):
1. List claims that lack citations
2. Assess: Does this claim NEED a citation? (opinion vs. fact)
3. For facts without citations:
   - Search my Zotero library for applicable sources
   - If no source exists: Identify what source I need to find
   - Suggest search terms and likely source types

Create a prioritized "Citation To-Do List":
- HIGH priority: Critical facts without sources
- MEDIUM priority: Important claims that would benefit from citation
- LOW priority: General statements that could use backing

Format as actionable tasks.
```

---

## Phase 4: Obsidian Knowledge Base Integration (30-45 minutes)

### Step 11: Create Literature Notes for Key Sources

**For top 10-15 most important sources**:

**Prompt**:
```
Create an Obsidian literature note for this source:

Zotero Key: [KEY]
Source: [Title, Author, Year]
Relevance: [Which SWOT components does this support?]

Use this template:

---
type: literature-note
zotero_key: [KEY]
source_type: [report/data/article]
date_added: 2025-11-11
swot_relevance: [S/W/O/T]
tags: [ceds, whatcom-county, economic-development]
---

# [Title]

**Authors**: [Authors]
**Organization**: [Org]
**Year**: [Year]
**URL**: [URL]
**Zotero**: [Link]

## Summary (2-3 sentences)
[What does this source say that's relevant to CEDS SWOT?]

## Key Data Points for SWOT
- [Specific statistic or finding 1]
- [Specific statistic or finding 2]
- [Specific statistic or finding 3]

## Supports These SWOT Elements
- **Strength**: [Which strength? How?]
- **Weakness**: [Which weakness? How?]
- **Opportunity**: [Which opportunity? How?]
- **Threat**: [Which threat? How?]

## Limitations & Caveats
- [Any limitations to note]
- [Date/scope limitations]

## Key Quotes
> "Quote here" (p. XX)

## Related Sources in Library
- [[Other Source 1]]
- [[Other Source 2]]

## Citation
[APA format]

---
**Created**: 2025-11-11
**Last Updated**: 2025-11-11
```

**Save to**: `Research/CEDS-SWOT/Literature/[Source-Name].md`

---

### Step 12: Create SWOT Component Synthesis Notes

**For each SWOT component**:

**Prompt**:
```
Create a synthesis note for: STRENGTHS section of Whatcom County CEDS SWOT

Based on my Zotero library and literature notes:

1. List all sources that support identified strengths
2. For each major strength:
   - What sources support it?
   - What specific data/evidence?
   - Are sources adequate or need more?
   - Rate confidence level (high/medium/low)

3. Identify patterns:
   - Which strengths have strongest evidence?
   - Which strengths need better sources?
   - Any contradictory evidence?

4. Create synthesis paragraph:
   - Integrate findings from multiple sources
   - Proper citations throughout
   - Note where evidence is strong vs. weak

Save as Obsidian note linking to all relevant literature notes.
```

**Create for**:
- `Research/CEDS-SWOT/Synthesis/Strengths-Evidence-Base.md`
- `Research/CEDS-SWOT/Synthesis/Weaknesses-Evidence-Base.md`
- `Research/CEDS-SWOT/Synthesis/Opportunities-Evidence-Base.md`
- `Research/CEDS-SWOT/Synthesis/Threats-Evidence-Base.md`

---

### Step 13: Create Citation Map

**Prompt**:
```
Create a visual map showing relationships between:

1. SWOT Components (Strengths, Weaknesses, Opportunities, Threats)
2. Specific SWOT elements under each component
3. Sources from my Zotero library that support each
4. Connections between sources (sources that relate to each other)
5. Gaps (SWOT elements lacking sources)

Format as Obsidian markdown with links.

This map should help me:
- See at a glance what's well-supported vs. weak
- Identify which sources are most critical
- Find related sources for cross-referencing
- Spot patterns in evidence
```

**Save as**: `Research/CEDS-SWOT/SWOT-Citation-Map.md`

---

## Phase 5: Enhancement & Ongoing Use (Ongoing)

### Step 14: Find Missing Sources

**Use the gap analysis from earlier**:

**Prompt**:
```
I need to find these missing sources for my CEDS SWOT:

HIGH PRIORITY:
- [List gaps from Phase 1, Step 3]

For each:
1. Suggest specific sources likely to have this data
2. Provide search strategy:
   - Keywords to use
   - Databases/websites to check
   - Expected source types
3. Provide direct URLs when possible

Focus on authoritative Whatcom County and Washington State sources:
- WA State Office of Financial Management
- Whatcom County official reports
- Port of Bellingham economic data
- Bellingham/Whatcom County Economic Development
- US Census Bureau (Whatcom County)
- Bureau of Labor Statistics (Bellingham-Whatcom MSA)
```

**For each source found**: Add to Zotero, create literature note, update synthesis

---

### Step 15: Establish Citation Update Protocol

**Prompt**:
```
Create a citation maintenance schedule for this CEDS SWOT project:

1. What sources need regular updates? (e.g., population data, employment stats)
2. How often should each be checked? (monthly, quarterly, annually)
3. Create a checklist for updating citations:
   - Check for new versions of key reports
   - Update statistics with latest available data
   - Verify links still work
   - Review if sources remain authoritative

4. Create Obsidian tracking note with:
   - Last verification date for each critical source
   - Next verification due date
   - Notes on updates needed
```

**Save as**: `Research/CEDS-SWOT/Citation-Maintenance-Schedule.md`

---

### Step 16: Generate Citation-Ready SWOT Drafts

**For each SWOT section**:

**Prompt**:
```
Generate a properly cited draft for the STRENGTHS section of Whatcom County CEDS SWOT.

Requirements:
1. Use sources from my Zotero library only
2. Cite in APA format (Author, Year) inline
3. Each factual claim must have citation
4. Include full bibliography at end
5. Use multiple sources for major claims
6. Note where evidence is strong vs. needs strengthening

Format:
- Narrative paragraph style (not bullet points)
- Professional tone appropriate for economic development plan
- Specific data points with citations
- Synthesize information from multiple sources

Aim for 300-400 words for this section.
```

**Repeat for**: Weaknesses, Opportunities, Threats sections

---

## Testing & Validation Checklist

Use these tests to verify the Citation & Source Verification skill is working correctly for your project:

### Basic Functionality Tests

- [ ] **Test 1**: Can extract citations from existing documents
  ```
  "Review document X and extract all citations"
  ```

- [ ] **Test 2**: Can identify unsourced claims
  ```
  "Identify claims in document X that need citations"
  ```

- [ ] **Test 3**: Can add sources to Zotero
  ```
  "Help me add this source to my Zotero library: [source details]"
  ```

- [ ] **Test 4**: Can search Zotero library
  ```
  "Search my Zotero library for sources about Whatcom County employment"
  ```

- [ ] **Test 5**: Can run source verification
  ```
  "Run 5-Point Verification Protocol on [source name]"
  ```

### Advanced Integration Tests

- [ ] **Test 6**: Can create literature notes in Obsidian
  ```
  "Create an Obsidian literature note for Zotero item [KEY]"
  ```

- [ ] **Test 7**: Can find supporting sources
  ```
  "Find sources in my library that support this claim: [claim]"
  ```

- [ ] **Test 8**: Can identify citation gaps
  ```
  "Review my SWOT Strengths section and identify gaps in citations"
  ```

- [ ] **Test 9**: Can cross-reference sources
  ```
  "Compare what these 3 sources say about Whatcom County population growth"
  ```

- [ ] **Test 10**: Can generate properly cited text
  ```
  "Draft a paragraph about Whatcom County economic strengths with proper citations"
  ```

---

## Expected Outcomes

### Immediate (End of Phase 1-2)
- Complete inventory of existing citations in CEDS project
- 20-40 sources added to organized Zotero library
- Clear understanding of citation gaps
- Prioritized list of sources to find

### Short-term (End of Phase 3-4)
- All major sources verified for quality
- Literature notes created for top sources
- Citation map showing relationships
- Synthesis notes connecting sources to SWOT components
- Draft SWOT sections with proper citations

### Long-term (Ongoing)
- Systematic citation management system
- Regular source updates and verification
- Growing knowledge base in Obsidian
- High-quality, well-sourced CEDS SWOT analysis
- Reusable citation infrastructure for future projects

---

## Time Investment Summary

| Phase | Activity | Time Estimate |
|-------|----------|---------------|
| 1 | Assessment & Extraction | 30-45 min |
| 2 | Zotero Library Setup | 45-60 min |
| 3 | Source Verification | 30-45 min |
| 4 | Obsidian Integration | 30-45 min |
| 5 | Enhancement | Ongoing |
| **Total Initial** | **Phases 1-4** | **2-3 hours** |

---

## Success Metrics

You'll know the implementation is successful when:

1. **Coverage**: Every factual claim in SWOT has a citation
2. **Quality**: All sources pass 5-Point Verification Protocol
3. **Organization**: Can quickly find sources by topic/SWOT component
4. **Efficiency**: Can add new sources and citations in <5 minutes
5. **Synthesis**: Can generate cited paragraphs from Zotero library
6. **Maintenance**: Have system for keeping citations current
7. **Confidence**: Trust that your CEDS SWOT is well-sourced and defensible

---

## Common Issues & Solutions

### Issue: "Too many sources to process at once"
**Solution**: Work in batches of 5-10 sources. Start with highest priority.

### Issue: "Source metadata incomplete or missing"
**Solution**: Use prompts to help find missing information. Document what's available.

### Issue: "Can't find authoritative source for claim"
**Solution**: Flag for review. May need to modify claim or conduct new research.

### Issue: "Sources contradict each other"
**Solution**: Document both views. Use verification protocol to assess which is more reliable.

### Issue: "Zotero library getting disorganized"
**Solution**: Regular maintenance. Use collections and tags consistently.

---

## Next Steps After Implementation

Once your CEDS SWOT citations are organized:

1. **Apply to other sections**: Use same system for full CEDS document
2. **Share with team**: Export bibliography, share Zotero collection
3. **Create templates**: Reuse for future economic development projects
4. **Build on knowledge base**: Obsidian becomes ongoing resource
5. **Establish expertise**: Well-cited work establishes credibility

---

## Resources

### Whatcom County-Specific Sources to Consider
- Whatcom County Comprehensive Plan
- Port of Bellingham Strategic Plan
- Bellingham/Whatcom Economic Partnership reports
- Western Washington University economic impact studies
- WA State Office of Financial Management - Whatcom County data
- US Census Bureau - Whatcom County profiles
- Opportunity Council community assessments

### Citation Style Resources
- **APA 7th Edition**: https://apastyle.apa.org/
- **Chicago Manual**: https://www.chicagomanualofstyle.org/

### Zotero Resources
- **Zotero Quick Start**: https://www.zotero.org/support/quick_start_guide
- **Adding Items**: https://www.zotero.org/support/adding_items_to_zotero

---

**Document Version**: 1.0
**Created**: 2025-11-11
**For Project**: Whatcom County CEDS SWOT Analysis
**Skill**: Citation & Source Verification

---

**Ready to start?** Begin with Phase 1, Step 1 and work through systematically. The skill will guide you through each step!
