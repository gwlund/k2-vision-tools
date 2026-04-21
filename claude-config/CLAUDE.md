# Claude AI Assistant - Global Configuration

This document provides universal guidelines for AI assistants (like Claude) when working across all my projects. Project-specific instructions should be added in project-level `claude.md` files.

## About Me

- **Name**: [Your Name]
- **Location**: [Your Location]
- **Focus Areas**: [Your focus areas — update as you learn what projects you work on]

## General Working Principles

### Communication Style
- **Direct and Clear**: Use straightforward language, avoid unnecessary jargon
- **Factual and Neutral**: Present information objectively, especially for civic/community content
- **Professional but Accessible**: Appropriate for both technical and non-technical audiences
- **Concise Documentation**: Focus on clarity over verbosity

### Quality Standards
- **Accuracy First**: Verify facts when possible, cite sources. Clearly state when facts cannot be verified
- **Completeness**: Provide sufficient context for standalone understanding
- **Consistency**: Follow established patterns within each project
- **Maintainability**: Create documentation and code that others can understand and maintain

## File Management Conventions

### File Naming Standards
- **Use descriptive names**: Filename should indicate content without opening the file
- **Date prefixes for time-based content**: `YYYY-MM-DD-Event-Name.md` (ISO 8601 format)
- **Proper capitalization**: Title Case for proper nouns, descriptive names
- **Hyphens preferred**: Use hyphens or spaces, NOT underscores
- **No special characters**: Avoid `:`, `?`, `/`, `\`, `*`, `|`, `<`, `>`

**Good Examples:**
- ✅ `2025-11-01-Meeting-Notes.md`
- ✅ `Network-Configuration-Guide.md`
- ✅ `John-Doe-Profile.md`

**Bad Examples:**
- ❌ `meeting_notes_11_1.md`
- ❌ `networkConfig.md`
- ❌ `john.md`

### Directory Organization
- **Logical grouping**: Group related files in clearly named directories
- **Flat when possible**: Avoid excessive nesting unless justified by scale
- **Special folders**: Use consistent names like `docs/`, `background/`, `images/`, `templates/`, `archive/`
- **Repo standrds**: Use widely used standards for github repo folder structures like `src/` , `docs/`, `scripts/`, `data/`, ...
- **README files**: Include README.md or START-HERE.md for navigation in complex projects

## Markdown & Documentation Standards

### Markdown Formatting
- **Headers**: Use `##` for main sections, `###` for subsections
- **Lists**: Use `-` for unordered, `1.` for ordered lists
- **Emphasis**: `**bold**` for important terms, `*italics*` for emphasis
- **Code blocks**: Always specify language for syntax highlighting
- **Links**: Use descriptive text, include URLs at point of reference

### Documentation Structure
Always include:
1. **Clear title** (H1 header)
2. **Brief overview/purpose** (1-2 sentences)
3. **Structured sections** with logical hierarchy
4. **Sources/references** when citing external information
5. **Last updated date** for time-sensitive content

### YAML Frontmatter (when applicable)
For projects using frontmatter (Obsidian, static sites, etc.):
- Use proper YAML syntax
- Place at the very top of the file
- Enclose in triple dashes `---`
- Use consistent field names across project

## Git & Version Control

Always create and use repos in my repo at https://github.com/gwlund unless told otherwise

### Commit Message Style
Use descriptive commit messages following this format:

```
type: Brief description

Detailed explanation if needed
```

**Common types:**
- `add`: New content, features, or files
- `update`: Changes to existing content
- `fix`: Corrections, bug fixes, typo fixes
- `docs`: Documentation-only changes
- `refactor`: Restructuring without functionality change
- `meta`: Changes to configuration, structure, metadata

**Good Examples:**
```
add: Network performance monitoring scripts

update: John Doe biography with new position

fix: Corrected broken links in Climate Action page

docs: Added API documentation for user endpoints
```

### Git Workflow
- **Commit frequently**: Small, logical commits are better than large batches
- **Descriptive messages**: Future readers should understand why the change was made
- **Review before commit**: Check what's being committed (`git status`, `git diff`)
- **Branch for features**: Use feature branches for significant changes
- **Clean history**: Squash commits when appropriate before merging

### Git LFS (Large File Storage)
For repositories with large files:
- **Track media files**: Images (`*.jpg`, `*.png`), videos, PDFs
- **Track binary files**: Office documents (`*.docx`, `*.xlsx`, `*.pptx`)
- **Monitor usage**: Stay within free tier limits when possible
- **Document tracking**: Note in project README which files use LFS

## Privacy & Sensitivity

### Personal Information
- **Public figures**: OK to document public activities, official roles, public statements
- **Private individuals**: Require explicit consent before including personal information
- **Contact information**: Only include publicly available contact details
- **Discretion**: Use judgment with controversial or sensitive material

### Data Classification
- ✅ **Public**: Published documents, public meetings, official statements
- ⚠️ **Sensitive**: Handle with care, verify appropriateness before including
- ❌ **Confidential**: Never include private communications, unpublished data without permission

## Project-Specific Instructions

**Each project should have its own `claude.md` file that includes:**
- Project purpose and scope
- Technology stack and tools
- Project-specific directory structure
- Custom naming conventions (if different from global)
- Specific metadata schemas (tags, topics, etc.)
- Domain-specific terminology and abbreviations
- Local context and background information
- Project-specific git workflow or branching strategy

**The project-level `claude.md` takes precedence over this global file.**

## Working with Claude Code

### When Starting a Task
1. **Understand context**: Review relevant `claude.md` files (global + project)
2. **Check existing patterns**: Look at existing files for style and structure
3. **Ask clarifying questions**: When unsure, ask before making assumptions
4. **Plan before executing**: For complex tasks, outline approach first

### Quality Checklist
Before completing work, verify:
- [ ] Files follow naming conventions
- [ ] Content is well-structured and clear
- [ ] Sources are cited appropriately
- [ ] Formatting is consistent with project standards
- [ ] No sensitive/private information included without permission
- [ ] Git commits are descriptive and logical
- [ ] Project-specific requirements are met

### Efficiency Preferences
- **Direct tool usage**: Use appropriate tools (Read, Edit, Grep) rather than bash when possible
- **Parallel operations**: When multiple independent operations are needed, run them in parallel
- **Minimal confirmation**: Proceed with clear tasks unless there's ambiguity or risk
- **Sub-agent model selection**: Never dispatch sub-agents using the haiku model. Always use sonnet or better (opus). Haiku output quality is insufficient for my work.

### Jupyter Notebook Safety Rules
**Invoke the `jupyter-notebook-safety` skill before editing any .ipynb file.** It contains complete guardrails, safe editing patterns, verification checklists, and corruption repair procedures. Key backstop rule: NEVER use the Edit tool or text-level replacement (sed, awk, `replace_all`) on .ipynb files — they corrupt cell source arrays.

## Custom Skills

### Learning Loop Skill

The `learning-loop` skill enables continuous learning across sessions. Located at `~/.claude/skills/learning-loop/`.

**Commands:**

| Command | Shortcut | When | Purpose |
|---------|----------|------|---------|
| `/advise` | `/lla` | Before work | Query prior learnings for relevant knowledge, failure patterns, working configurations |
| `/retrospective` | `/llr` | After work | Extract learnings from session and save to registry |

**Usage:**
- **Start of session**: Run `/advise` to surface relevant prior learnings
- **End of session**: Run `/retrospective` to capture what worked/failed

**Learnings Storage:**
- Location: `~/.claude/skills/learning-loop/learnings/YYYY-MM/`
- Format: Markdown files with YAML frontmatter
- Naming: `YYYY-MM-DD_topic-slug.md`

**Searching Learnings:**
```bash
# Find by keyword
grep -r "keyword" ~/.claude/skills/learning-loop/learnings/

# Find by project
grep -l "project: project-name" ~/.claude/skills/learning-loop/learnings/**/*.md

# Recent learnings
ls -lt ~/.claude/skills/learning-loop/learnings/$(date +%Y-%m)/ | head -5
```

**Design:** Inspired by the [Kai History System](https://github.com/danielmiessler/Personal_AI_Infrastructure/blob/main/Packs/kai-history-system.md) - time-based directories, markdown with YAML frontmatter, Unix-searchable.

## Global Tools and Utilities

### Zotero CLI

Globally installed Python CLI for programmatic access to Zotero research library. Available across all projects.

**Installation Status:** ✅ Deployed 2026-01-27
**Location:** `~/.local/bin/zotero-*` (23 commands)
**Source Code:** `/Users/gil-lund/Documents/Projects/000-Claude-Code-Templates/scripts/zotero-cli/`
**Full Documentation:** `~/.local/lib/zotero-cli/README.md`
**Quick Reference:** `~/.claude/ZOTERO-CLI-REFERENCE.md`

**Environment Requirements:**
```bash
export ZOTERO_API_KEY=your_api_key
export ZOTERO_USER_ID=your_user_id
```
Get credentials at: https://www.zotero.org/settings/keys

**Most Common Commands:**

Import paper by DOI (recommended for research):
```bash
zotero-import-doi 10.1234/example --collection "Project Name" --tags "topic,keywords"
```

Search library:
```bash
zotero-search-items "search term"
```

Create collection:
```bash
zotero-create-collection "Collection Name"
```

Tag items:
```bash
zotero-add-tags ITEM_KEY tag1 tag2 tag3
```

List all available commands:
```bash
ls ~/.local/bin/zotero-*
```

**When to Use:**
- Adding research sources during literature reviews
- Organizing citations by project phase
- Tagging papers for cross-reference analysis
- Searching previously saved research
- Exporting annotations for note-taking

**Integration with Research Projects:**
All research-heavy projects (CEDS, climate action, etc.) should use zotero-cli for:
1. Importing sources via DOI (fastest method)
2. Organizing by research phase/topic
3. Tagging for SWOT/analysis categories
4. Citation generation with [@citekey] notation

**Claude Code Usage:**
When working on research projects, Claude can invoke zotero-cli commands via Bash to:
- Find existing papers in library
- Import new papers from DOI
- Tag and organize citations
- Generate bibliographies

See project-specific CLAUDE.md files for integration patterns.

### macOS Clipboard (pbcopy/pbpaste)

Native macOS command-line utilities for clipboard access. Use these to copy content directly to clipboard for pasting into other applications.

**Commands:**
```bash
# Copy text to clipboard
echo "text to copy" | pbcopy

# Copy file contents to clipboard
cat file.txt | pbcopy

# Copy multi-line content using heredoc
cat << 'EOF' | pbcopy
Line 1
Line 2
Line 3
EOF

# Paste clipboard contents
pbpaste

# Paste to file
pbpaste > output.txt
```

**Use Case:** When user needs to paste content into Outlook or other apps, use `pbcopy` to put clean plain text on the clipboard - avoids formatting issues from copying rendered markdown.

**Note:** These are macOS-only commands. On Windows use `clip` (copy) or PowerShell.

## Getting Help

### Claude Code Resources
- **Documentation**: https://docs.claude.com/en/docs/claude-code
- **Getting Started**: https://docs.claude.com/en/docs/claude-code/getting-started
- **Report Issues**: https://github.com/anthropics/claude-code/issues
- **Help Command**: Type `/help` in Claude Code CLI

### When to Ask Questions
- Requirements are unclear or ambiguous
- Multiple valid approaches exist (ask for preference)
- Potentially destructive operations (confirm before proceeding)
- Privacy or sensitivity concerns
- Deviating from established patterns

---

**Version**: 1.2.2
**Last Updated**: 2026-03-06
**Status**: Active

*This document should be updated as new patterns and preferences emerge.*
- make sure the skill citation-source-verification is used for all citation work and using the zotero-cli.  Verify that this skill does not mention using the zotero mcp server which I have disabled