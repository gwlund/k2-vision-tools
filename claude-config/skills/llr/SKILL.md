---
name: llr
description: Shortcut for /learning-loop retrospective - extract and save learnings after completing work. Captures what worked, what failed, failure patterns, and recommendations for future sessions. This is the essential learning-loop command - ensures learnings are stored in a searchable format.
---

# /llr - Learning Loop Retrospective (Shortcut)

This is a shortcut for `/learning-loop retrospective`.

**Purpose:** Extract structured learnings and save in a format that future `/lla` queries can find.

## Why This Matters

Future `/lla` queries search by:
- **YAML frontmatter** - tags, project fields for filtering
- **Filename date prefix** - for finding recent learnings
- **Standard section headers** - `## What Failed`, `## Recommendations`

Without proper format, learnings exist but can't be discovered.

## Workflow

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

4. **Write learning file** to `~/.claude/skills/learning-loop/learnings/YYYY-MM/`:

   ```markdown
   ---
   date: YYYY-MM-DD
   project: project-name
   topic: Brief Topic Title
   tags: [tag1, tag2, tag3]
   ---

   # Topic Title

   ## Context
   ## What Worked
   ## What Failed
   ## Failure Patterns
   ## Working Configurations
   ## Recommendations
   ## Session Summary
   ```

5. **Confirm to user** - State filename and key learnings extracted.

## Validation Checklist

Before saving, verify:
- [ ] Location: `~/.claude/skills/learning-loop/learnings/YYYY-MM/`
- [ ] Filename: `YYYY-MM-DD_topic-slug.md`
- [ ] YAML frontmatter: date, project, topic, tags
- [ ] Required sections present
