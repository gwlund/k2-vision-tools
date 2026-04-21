---
name: learning-loop
description: Continuous learning workflow with two commands - /advise (before work) queries prior learnings for relevant experiments, failure patterns, and working configurations; /retrospective (after work) extracts learnings from the session and saves to the learnings registry. Use at the start and end of development sessions.
argument-hint: advise | retrospective
---

# Learning Loop

Transform ephemeral session knowledge into searchable institutional memory. Inspired by the [Kai History System](https://github.com/danielmiessler/Personal_AI_Infrastructure/blob/main/Packs/kai-history-system.md).

## Core Value

**`/llr` (retrospective) is the essential command.** It ensures learnings are stored in a consistent, searchable format. Without proper format, learnings exist but can't be found by future `/lla` queries.

`/lla` (advise) queries those stored learnings before starting new work.

## Commands

| Command | When | Purpose |
|---------|------|---------|
| `/lla` | Before work | Query prior learnings for relevant knowledge |
| `/llr` | After work | **Extract and save learnings in searchable format** |

---

## /lla - Advise (Before Work)

**Purpose:** Surface relevant past knowledge before starting work.

**Workflow:**

1. **Identify the topic** - What project/technology/problem are you working on?

2. **Search learnings directory** at `~/.claude/skills/learning-loop/learnings/`:
   - Search by keyword, project name, or tags
   - Check recent months for relevant files

3. **Read and summarize** relevant learnings:
   - Failure Patterns - What to avoid
   - Working Configurations - What works
   - Recommendations - What to do differently

4. **Report findings** or state "new topic area" if nothing found.

---

## /llr - Retrospective (After Work)

**Purpose:** Extract structured learnings and save in a format that future `/lla` queries can find.

### Why Format Matters

Future `/lla` queries search by:
- **YAML frontmatter** - tags, project fields for filtering
- **Filename date prefix** - for finding recent learnings
- **Standard section headers** - `## What Failed`, `## Recommendations` for grep

Without this structure, learnings exist but can't be discovered.

### Workflow

1. **Review the entire conversation** - Scan for:
   - Problems encountered and solutions discovered
   - Failed approaches and successful patterns
   - Key configurations that worked

2. **Extract structured learning** with these sections:

   | Section | Content |
   |---------|---------|
   | Context | What was being attempted |
   | What Worked | Successful approaches, patterns, tools |
   | What Failed | Unsuccessful approaches and why |
   | Failure Patterns | Anti-patterns to avoid in future |
   | Working Configurations | Specific configs, commands, settings |
   | Recommendations | Advice for future similar work |
   | Session Summary | Brief 1-2 sentence summary |

3. **Create month directory if needed**:
   ```bash
   mkdir -p ~/.claude/skills/learning-loop/learnings/$(date +%Y-%m)
   ```

4. **Write learning file** with this template:

   ```markdown
   ---
   date: YYYY-MM-DD
   project: project-name
   topic: Brief Topic Title
   tags: [tag1, tag2, tag3]
   ---

   # Topic Title

   ## Context
   What was being attempted...

   ## What Worked
   - Successful approach 1

   ## What Failed
   - Failed approach 1 (reason)

   ## Failure Patterns
   - Anti-pattern to avoid...

   ## Working Configurations
   - Specific config that works...

   ## Recommendations
   - Do this next time...

   ## Session Summary
   Brief summary of what was accomplished and learned.
   ```

5. **Confirm to user** - State filename and key learnings extracted.

### Validation Checklist

Before saving, verify:
- [ ] File location: `~/.claude/skills/learning-loop/learnings/YYYY-MM/`
- [ ] Filename format: `YYYY-MM-DD_topic-slug.md`
- [ ] YAML frontmatter with: date, project, topic, tags
- [ ] Required sections: What Worked, What Failed, Failure Patterns, Recommendations

---

## File Naming Convention

**Pattern:** `YYYY-MM-DD_topic-slug.md`

| Component | Format | Example |
|-----------|--------|---------|
| Date | `YYYY-MM-DD` | `2026-01-03` |
| Separator | `_` | `_` |
| Topic slug | lowercase, hyphen-separated | `budget-categorization` |

**Examples:**
- `2026-01-03_budget-categorization.md`
- `2026-03-09_skill-creator-patterns.md`

---

## Directory Structure

```
~/.claude/skills/learning-loop/
├── SKILL.md                           # This file
└── learnings/                         # Time-based learning storage
    ├── 2026-01/                       # Monthly directories
    │   ├── 2026-01-03_topic-one.md
    │   └── 2026-01-05_topic-two.md
    └── 2026-03/
        └── ...
```

---

## Usage Examples

**Starting a session:**
```
User: /lla
Claude: [Searches learnings directory]
Claude: "Based on prior learnings about pandas:
- Batch processing patterns work well
- Avoid magic strings - use config files..."
```

**Ending a session:**
```
User: /llr
Claude: [Reviews conversation, extracts learnings]
Claude: "Saved to learnings/2026-03/2026-03-09_async-httpx-migration.md:
- What worked: httpx AsyncClient
- What failed: requests blocking event loop
- Key pattern: Always use async-native HTTP libraries in async code"
```

**Note:** `/lla` and `/llr` are standalone shortcut skills.

---

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Zero manual effort** | Claude extracts and saves automatically |
| **Human-readable** | Plain markdown, no special tooling needed |
| **Unix-searchable** | grep/find work out of the box |
| **Time-organized** | Monthly directories for natural cleanup |
| **Structured metadata** | YAML frontmatter for filtering |
