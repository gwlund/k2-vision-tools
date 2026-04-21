# Page Templates Reference

Complete templates for all five page types used by the obsidian-vault-keeper skill. Each template defines the exact YAML frontmatter and body section structure to use when creating pages during vault ingest operations.

---

## 1. Entity

**Folder:** `entities/`
**Purpose:** Named things — tools, people, organizations, projects, technologies

### YAML Frontmatter

```yaml
---
type: entity                          # required — always "entity"
title: "Tool or Entity Name"          # required — canonical display name
aliases:                              # required — alternative names (can be empty list)
  - "Alternate Name"
  - "Abbreviation"
created: 2026-04-07                   # required — ISO 8601, date page was first created
updated: 2026-04-07                   # required — ISO 8601, date page was last modified
status: stub                          # required — stub | developing | mature
source_count: 1                       # required — integer, number of sources referencing this entity
tags_yaml:                            # required — YAML array for Dataview queries
  - entity
  - tool                              # add domain tags: tool | person | org | project | technology
---
```

### Body

```markdown
Tags: #entity #tool

## Overview

Brief description of what this entity is and its primary purpose or role.

## Key Details

| Attribute | Value |
|-----------|-------|
| Type      |       |
| Domain    |       |
| Status    |       |
| Website   |       |

Add or remove rows as relevant. Keep only attributes with known values.

## Relationships

- Related to [[Entity Name]] — brief reason for relationship
- Used by [[Entity Name]]
- Part of [[Entity Name]]

## Source References

- [[Source Page Title]] — what this source says about the entity
- [[Source Page Title]]

## Additional Notes

Any context, caveats, or notes that don't fit the sections above.
```

---

## 2. Concept

**Folder:** `concepts/`
**Purpose:** Patterns, principles, ideas, methodologies

### YAML Frontmatter

```yaml
---
type: concept                         # required — always "concept"
title: "Concept Name"                 # required — canonical name for the concept
aliases:                              # required — alternative names or phrasings (can be empty list)
  - "Alternative Phrasing"
created: 2026-04-07                   # required — ISO 8601
updated: 2026-04-07                   # required — ISO 8601
status: stub                          # required — stub | developing | mature
source_count: 1                       # required — integer
tags_yaml:                            # required — YAML array for Dataview queries
  - concept
  - methodology                       # add domain tags: pattern | principle | methodology | framework | technique
---
```

### Body

```markdown
Tags: #concept #methodology

## Definition

A clear, concise definition of the concept. One to three sentences.

## Key Principles

- First principle or characteristic
- Second principle or characteristic
- Third principle or characteristic

## Related Concepts

- [[Concept Name]] — how it relates
- [[Concept Name]] — how it differs or connects

## Applications

Where and how this concept is applied in practice. Use bullet points or short paragraphs.

## Source References

- [[Source Page Title]] — how this source addresses the concept
- [[Source Page Title]]

## Additional Notes

Any nuance, debate, or context not covered above.
```

---

## 3. Source

**Folder:** `sources/`
**Purpose:** One summary page per ingested raw document

### YAML Frontmatter

```yaml
---
type: source                          # required — always "source"
title: "Document Title"               # required — title of the original document
source_file: "filename.pdf"           # required — original filename or path of the ingested file
source_type: article                  # required — article | paper | documentation | book | video | transcript | code
date_ingested: 2026-04-07             # required — ISO 8601, when the document was ingested into the vault
created: 2026-04-07                   # required — ISO 8601, when this page was created
updated: 2026-04-07                   # required — ISO 8601
tags_yaml:                            # required — YAML array for Dataview queries
  - source
  - article                           # repeat source_type value here as a tag
---
```

**Note:** Source pages do not have `status` or `source_count` fields — those belong to entity/concept/synthesis pages.

### Body

```markdown
Tags: #source #article

## Summary

A 2–5 sentence summary of the document's main argument, purpose, or content.

## Key Takeaways

- Most important point or finding
- Second important point
- Third important point
- Add as many as are meaningful; avoid trivial points

## Entities Mentioned

- [[Entity Name]] — brief context for why it appears
- [[Entity Name]]

## Concepts Covered

- [[Concept Name]] — how the source treats this concept
- [[Concept Name]]

## Notable Quotes / Data

> "Direct quote from the source." (p. X or timestamp)

Include statistics, key data points, or verbatim passages worth preserving.

## Additional Notes

Caveats about the source, its age, author perspective, or anything that affects how it should be weighted.
```

---

## 4. Synthesis

**Folder:** `synthesis/`
**Purpose:** Comparisons, analyses, filed query results

### YAML Frontmatter

```yaml
---
type: synthesis                       # required — always "synthesis"
title: "Synthesis Title"              # required — descriptive title, often phrased as a question or topic
synthesis_type: analysis              # required — comparison | analysis | overview | question-answer
created: 2026-04-07                   # required — ISO 8601
updated: 2026-04-07                   # required — ISO 8601
status: stub                          # required — stub | developing | mature
source_count: 3                       # required — integer, number of sources consulted for this synthesis
tags_yaml:                            # required — YAML array for Dataview queries
  - synthesis
  - analysis                          # repeat synthesis_type value here as a tag
---
```

### Body

```markdown
Tags: #synthesis #analysis

## Question / Purpose

State the driving question or purpose of this synthesis in 1–2 sentences. What prompted it?

## Analysis

The main body of reasoning. Use subsections (###) if the analysis covers multiple angles. Integrate evidence from sources by referencing them inline or in Source References below.

## Findings

- Key finding one
- Key finding two
- Key finding three

For comparisons, a table may be more appropriate than a bullet list:

| Attribute | Option A | Option B |
|-----------|----------|----------|
|           |          |          |

## Sources Consulted

- [[Source Page Title]]
- [[Source Page Title]]
- [[Entity Name]] or [[Concept Name]] pages if relevant

## Conclusion

A direct answer to the question or a summary of what the synthesis established. 2–4 sentences.

## Additional Notes

Open questions, areas needing more sources, or limitations of this synthesis.
```

---

## 5. Event

**Folder:** `events/`
**Purpose:** Dated events, releases, decisions, milestones

### YAML Frontmatter

```yaml
---
type: event                           # required — always "event"
title: "Event Name or Description"    # required — short descriptive title
event_date: 2026-04-07                # required — ISO 8601, when the event occurred
event_type: release                   # required — release | decision | milestone | incident
created: 2026-04-07                   # required — ISO 8601, when this page was created
updated: 2026-04-07                   # required — ISO 8601
tags_yaml:                            # required — YAML array for Dataview queries
  - event
  - release                           # repeat event_type value here as a tag
---
```

**Note:** Event pages do not have `status`, `source_count`, or `aliases` fields.

### Body

```markdown
Tags: #event #release

## Summary

A 2–3 sentence description of what happened, when, and who was involved.

## Context

Background that explains why this event occurred or why it matters.

## Impact

What changed as a result of this event. Use bullet points for multiple impacts.

- Impact one
- Impact two

## Related Entities

- [[Entity Name]] — role in the event
- [[Entity Name]]

## Source References

- [[Source Page Title]] — what this source says about the event
- [[Source Page Title]]

## Additional Notes

Follow-up, unresolved questions, or links to subsequent events.
```

---

## Field Reference Summary

| Field | Entity | Concept | Source | Synthesis | Event |
|-------|--------|---------|--------|-----------|-------|
| `type` | required | required | required | required | required |
| `title` | required | required | required | required | required |
| `aliases` | required | required | — | — | — |
| `created` | required | required | required | required | required |
| `updated` | required | required | required | required | required |
| `status` | required | required | — | required | — |
| `source_count` | required | required | — | required | — |
| `source_file` | — | — | required | — | — |
| `source_type` | — | — | required | — | — |
| `date_ingested` | — | — | required | — | — |
| `synthesis_type` | — | — | — | required | — |
| `event_date` | — | — | — | — | required |
| `event_type` | — | — | — | — | required |
| `tags_yaml` | required | required | required | required | required |

---

*Last updated: 2026-04-07*
