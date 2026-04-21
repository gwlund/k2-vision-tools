---
type: literature-note
title: "{{title}}"
authors: {{authors}}
year: {{date | format("YYYY")}}
citekey: {{citekey}}
zotero-key: {{itemKey}}
---

Tags: #literature

# {{title}}

## Metadata

- **Authors:** {{authors}}
- **Year:** {{date | format("YYYY")}}
- **Type:** {{itemType}}
{{#if publicationTitle}}- **Publication:** {{publicationTitle}}{{/if}}
{{#if DOI}}- **DOI:** [{{DOI}}](https://doi.org/{{DOI}}){{/if}}
{{#if url}}- **URL:** {{url}}{{/if}}
- **Zotero:** [Open in Zotero]({{desktopURI}})

## Abstract

{{abstractNote}}

## Key Findings

1.
2.
3.

## Methodology

{{#if methods}}
{{methods}}
{{else}}
[Describe research methodology]
{{/if}}

## Relevance to Project

[How this relates to your research]

## Strengths

-

## Limitations

-

## Key Quotes

> "Quote here" (p. XX)

## Personal Notes

{{notes}}

## Related Literature

- [[]]

## Tags

{{tags}}

## Attachments

{{#each attachments}}
- [{{title}}]({{path}})
{{/each}}

---

**Created:** {{importDate | format("YYYY-MM-DD")}}
**Zotero Key:** {{itemKey}}
**Citation:** {{citation}}
