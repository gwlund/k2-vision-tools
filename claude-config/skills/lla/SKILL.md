---
name: lla
description: Shortcut for /learning-loop advise - query prior learnings before starting work. Surfaces relevant failure patterns, working configurations, and recommendations from previous sessions.
---

# /lla - Learning Loop Advise (Shortcut)

This is a shortcut for `/learning-loop advise`.

**Purpose:** Surface relevant past knowledge before starting work.

## Workflow

1. **Identify the topic** - What project/technology/problem?

2. **Search learnings directory** at `~/.claude/skills/learning-loop/learnings/`:
   - Search by keyword, project name, or tags
   - Check recent months for relevant files

3. **Read and summarize** relevant learnings:
   - Failure Patterns - What to avoid
   - Working Configurations - What works
   - Recommendations - What to do differently

4. **Report findings** or state "new topic area" if nothing found.

## Search Examples

```bash
# By keyword
grep -r "KEYWORD" ~/.claude/skills/learning-loop/learnings/

# By project
grep -l "project: PROJECT" ~/.claude/skills/learning-loop/learnings/**/*.md

# Recent learnings
ls -lt ~/.claude/skills/learning-loop/learnings/$(date +%Y-%m)/
```
