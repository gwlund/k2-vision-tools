# Citation & Source Verification - Test Prompts

Test prompts to validate the Citation & Source Verification skill is working correctly with zotero-cli and Obsidian.

---

## Test 1: Zotero API Connection

**Purpose**: Verify zotero-cli is properly connected

**Prompt**:
```
Show me the first 5 items in my Zotero library.
For each, display:
- Title
- Authors
- Year
- Item key
```

**Expected Result**:
- Returns 5 actual items from your Zotero library
- All metadata fields populated
- No error messages

**If Failed**:
- Verify zotero-cli is installed: `zotero-verify-api`
- Verify environment variables: `echo $ZOTERO_API_KEY`
- Check Zotero sync status

---

## Test 2: Basic Search Functionality

**Purpose**: Test searching Zotero library by keyword

**Prompt**:
```
Search my Zotero library for papers about "climate" or "adaptation".
Show the titles and years of papers found.
```

**Expected Result**:
- Returns relevant papers from your library
- Search works across title, abstract, and tags
- Results are accurate

**If Failed**:
- Try more specific search term
- Check if papers exist in your library
- Verify search is not case-sensitive

---

## Test 3: Get Full Metadata

**Purpose**: Retrieve complete citation information

**Prompt**:
```
For the most recently added item in my Zotero library, show me:
- Complete bibliographic information
- All tags
- Any notes attached
- Abstract (if available)
- Item key for linking
```

**Expected Result**:
- Complete metadata displayed
- All fields populated
- Item key provided

---

## Test 4: Citation Format Generation

**Purpose**: Generate citations in different styles

**Prompt**:
```
Take the first paper in my Zotero library and generate citations in:
1. APA 7th edition
2. Chicago style
3. MLA format

Show both the inline citation and full bibliography entry for each.
```

**Expected Result**:
- Properly formatted citations in all three styles
- Inline and bibliography entries both correct
- Formatting matches official style guides

---

## Test 5: Source Quality Assessment

**Purpose**: Run 5-Point Verification Protocol

**Prompt**:
```
I want to verify the quality of this source: [pick a paper from your library]

Run the 5-Point Verification Protocol:
1. Authority - Assess author credentials
2. Currency - Check if information is up-to-date
3. Accuracy - Cross-reference key claims
4. Purpose - Identify potential biases
5. Coverage - Evaluate comprehensiveness

Provide a final recommendation: cite with confidence, cite with caveats, or do not cite.
```

**Expected Result**:
- Systematic assessment of each criterion
- Specific findings for each point
- Clear recommendation with rationale

---

## Test 6: Obsidian Integration (if Local REST API configured)

**Purpose**: Create literature note in Obsidian

**Prompt**:
```
For this paper in my Zotero library: [Paper Title]

Create an Obsidian literature note at:
Path: Research/Test/Literature-Note-Test.md

Include:
- Frontmatter with Zotero key
- Bibliographic information
- Space for summary and key findings
- Link back to Zotero
```

**Expected Result**:
- Note created in correct location
- Frontmatter properly formatted
- Zotero link functional

**If Failed**:
- Check Obsidian Local REST API plugin is running
- Verify API key is configured
- Check folder path exists

---

## Test 7: Collection Organization

**Purpose**: Test Zotero collection management

**Prompt**:
```
In my Zotero library:
1. List all my collections
2. Show how many items are in each
3. Identify any uncollected items

Then suggest an organizational structure based on my content.
```

**Expected Result**:
- Complete list of collections
- Accurate item counts
- Useful organizational suggestions

---

## Test 8: Literature Search Expansion

**Purpose**: Identify missing sources

**Prompt**:
```
Based on the papers in my Zotero library about [your topic],
identify 5 important papers I'm likely missing.

For each suggestion:
- Why it's important
- How to find it (DOI if possible)
- How it relates to my existing collection
```

**Expected Result**:
- Relevant, high-quality suggestions
- Clear rationale for each
- Findable sources (real DOIs)

---

## Test 9: Fact-Checking Workflow

**Purpose**: Verify a specific claim

**Prompt**:
```
I found this claim: "[Make up a plausible claim from one of your papers]"

Help me verify it:
1. Find the original source in my Zotero
2. Check if I'm representing it accurately
3. Find other sources that confirm or contradict it
4. Assess the quality of evidence
5. Recommend how to cite it (if at all)
```

**Expected Result**:
- Finds source in your library
- Thorough verification process
- Multiple-source cross-reference
- Clear citation recommendation

---

## Test 10: Literature Review Synthesis

**Purpose**: Generate thematic synthesis

**Prompt**:
```
Analyze the papers in my Zotero library (or a specific collection) and:
1. Identify 3-5 major themes
2. For each theme, list relevant papers
3. Summarize the state of knowledge
4. Note any debates or contradictions
5. Identify gaps

Create a synthesis framework I can use for writing.
```

**Expected Result**:
- Meaningful themes identified
- Papers correctly categorized
- Useful synthesis for writing
- Gaps clearly identified

---

## Test 11: Citation Network Analysis

**Purpose**: Find influential and missing papers

**Prompt**:
```
Analyze citation patterns in my Zotero collection on [topic]:
1. Which papers in my collection are most influential?
2. Are there frequently-cited papers I don't have?
3. Identify clusters of related papers
4. Find bridge papers connecting different areas
```

**Expected Result**:
- Identifies influential papers
- Suggests missing sources
- Shows relationships
- Useful for expanding collection

---

## Test 12: Multi-Format Export

**Purpose**: Export citations for different uses

**Prompt**:
```
For these 3 papers in my Zotero: [List 3 papers]

Export as:
1. BibTeX (for LaTeX)
2. RIS (for EndNote)
3. Plain text bibliography (APA)
4. Formatted for insertion in Word document
```

**Expected Result**:
- All formats generated correctly
- Ready to use in respective applications
- No formatting errors

---

## Integration Test: Complete Workflow

**Purpose**: Test entire workflow from discovery to citation

**Workflow**:

### Step 1: Find New Source
```
I need papers on [topic]. Search my library first, then suggest
high-quality papers I should add.
```

### Step 2: Add to Zotero
```
Add this paper to my Zotero:
DOI: [actual DOI]
Add tags: [relevant tags]
Add to collection: [collection name]
Add note: [why this is relevant]
```

### Step 3: Verify Quality
```
Run the 5-Point Verification Protocol on the paper I just added.
Should I cite this with confidence?
```

### Step 4: Create Literature Note
```
Create an Obsidian literature note for this paper including:
- Summary
- Key findings
- Relevance to my research
- Link to Zotero
```

### Step 5: Generate Citation
```
I'm citing this paper in my manuscript. Generate:
- APA inline citation
- Full bibliography entry
- A sample sentence showing proper usage
```

### Step 6: Cross-Reference
```
Find 2-3 other papers in my library that relate to this paper.
Create an Obsidian synthesis note connecting them.
```

**Expected Result**: Smooth workflow from discovery through citation with all steps functioning.

---

## Troubleshooting Tests

### Test: API Connection Issues

**Prompt**:
```
Help me troubleshoot my Zotero API connection:
1. Verify zotero-cli is installed and working
2. Verify my API credentials are working
3. Test basic read operations
4. Test search functionality
```

### Test: Metadata Quality

**Prompt**:
```
Review the metadata quality in my Zotero library:
1. Find items with missing information
2. Identify items without PDFs
3. Find items without tags
4. Suggest improvements
```

### Test: Obsidian Sync Status

**Prompt**:
```
Check the status of my Obsidian integration:
1. Can we read notes?
2. Can we create notes?
3. Can we search notes?
4. Test the zotero:// link format
```

---

## Performance Benchmarks

### Speed Test
**Prompt**: "Search my Zotero library for papers on [common topic]"
**Expected**: Response within 2-3 seconds

### Accuracy Test
**Prompt**: "Find all papers by [specific author]"
**Expected**: 100% of papers by that author returned

### Completeness Test
**Prompt**: "Show all metadata for [specific paper]"
**Expected**: All available fields populated

---

## Validation Checklist

After running all tests, verify:

- [ ] Zotero API responds to queries (via zotero-cli)
- [ ] Search functionality works accurately
- [ ] Full metadata retrievable
- [ ] Citation formats generate correctly
- [ ] Source verification protocol functional
- [ ] Obsidian integration working (if configured)
- [ ] Collections manageable
- [ ] Literature expansion suggestions useful
- [ ] Fact-checking workflow functional
- [ ] Synthesis generation meaningful
- [ ] Citation network analysis insightful
- [ ] Export formats correct
- [ ] Complete workflow smooth
- [ ] Troubleshooting tools effective
- [ ] Performance acceptable

---

## Test Results Template

Use this template to document test results:

```markdown
# Citation & Source Verification Skill - Test Results

**Date**: [Date]
**Tester**: [Your Name]
**Environment**:
- zotero-cli Version: [version]
- Obsidian Version: [version] (if applicable)
- Claude Code Version: [version]

## Test Results

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Zotero API Connection | ✅ / ❌ | |
| 2 | Basic Search | ✅ / ❌ | |
| 3 | Full Metadata | ✅ / ❌ | |
| 4 | Citation Formats | ✅ / ❌ | |
| 5 | Source Verification | ✅ / ❌ | |
| 6 | Obsidian Integration | ✅ / ❌ / N/A | |
| 7 | Collection Organization | ✅ / ❌ | |
| 8 | Literature Expansion | ✅ / ❌ | |
| 9 | Fact-Checking | ✅ / ❌ | |
| 10 | Literature Synthesis | ✅ / ❌ | |
| 11 | Citation Network | ✅ / ❌ | |
| 12 | Multi-Format Export | ✅ / ❌ | |
| 13 | Complete Workflow | ✅ / ❌ | |

## Overall Assessment

**Pass Rate**: [X/13 tests passed]

**Critical Issues**:
-

**Minor Issues**:
-

**Recommendations**:
-

**Skill Ready for Use**: YES / NO / WITH CAVEATS

## Additional Notes

[Any other observations or comments]
```

---

**Created**: 2025-11-10
**Updated**: 2025-12-18
**Version**: 1.1.0
**Maintainer**: Gil Lund
**Note**: Updated for zotero-cli (MCP references removed)
