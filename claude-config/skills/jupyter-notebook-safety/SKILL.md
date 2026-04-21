---
name: jupyter-notebook-safety
description: >-
  MANDATORY safety guardrails for Jupyter notebook (.ipynb) editing. Use whenever
  editing, writing, modifying, creating, or performing find-and-replace on any .ipynb
  file using ANY method (Edit tool, Write tool, Python scripts, or JSON manipulation).
  Prevents catastrophic notebook corruption where cell source arrays split into
  single-character arrays. Also use when renaming variables/columns/identifiers that
  appear in notebook cells, or when running programmatic notebook modifications via
  nbconvert or papermill. If you are about to touch a .ipynb file in any way, invoke
  this skill first.
tags: [jupyter, notebook, ipynb, safety, corruption-prevention]
version: 1.1.0
author: Gil Lund
created: 2026-04-07
updated: 2026-04-10
requires_mcp: none
---

# Jupyter Notebook Safety

## Why This Exists

Jupyter notebooks (.ipynb) are structured JSON. Each cell's `source` field is an **array of strings** (one per line), not a single string. Text-level editing tools — the Edit tool, sed, awk — treat the file as flat text and can split those strings into individual characters. The result: every character renders on its own line, destroying the notebook. This corruption is silent — no tool warns you it happened.

This skill exists because this exact failure destroyed 7 cells in a production notebook. The rules below prevent it from happening again.

## Decision Tree

Determine your modification type, then follow the corresponding safe method:

1. **Editing cell content** (changing code or text within existing cells)?
   - NotebookEdit tool available? Use it. (Preferred — handles JSON structure correctly)
   - Not available? Use the json.load/modify/json.dump pattern below.

2. **Creating a new notebook from scratch?**
   - Use the Write tool with complete, valid .ipynb JSON structure.
   - Or use the `nbformat` Python library to construct programmatically.

3. **Renaming identifiers** (variables, columns, function names) that appear in notebooks?
   - Use the json.load/modify/json.dump pattern.
   - Also re-export any CSV or data files the notebook loads — stale column headers cause `KeyError` even when all code references are updated.

4. **Executing a notebook non-interactively?**
   - `uv run jupyter nbconvert --to notebook --execute NOTEBOOK.ipynb --output /tmp/test-output.ipynb`

## Forbidden Operations

These operations cause corruption. Do not use them on .ipynb files under any circumstances.

**1. Edit tool on .ipynb files** — The Edit tool (including `replace_all`) treats .ipynb as plain text. Any replacement can break the JSON source array structure, splitting strings into single-character arrays. This is the most common corruption vector.

**2. sed, awk, or grep-based replacement on .ipynb files** — Same flat-text problem. These tools have no awareness of JSON structure.

**3. Calling `.replace()` on a cell's source list** — `cell['source']` is a `list[str]`, not a `str`. Calling `.replace()` on the list itself does not do what you expect. You must iterate the list and replace within each individual line string.

## Safe Editing Methods

### Method 1: NotebookEdit Tool (Preferred)

Use when available. It understands notebook JSON structure and modifies cells safely.

### Method 2: json.load / modify / json.dump

The reliable manual approach. Iterate source lines individually — never operate on the source list as a whole.

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

for cell in nb['cells']:
    # Replace within each line string individually
    cell['source'] = [line.replace('old_text', 'new_text') for line in cell['source']]

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

### Method 3: nbformat Library

For programmatic notebook creation or complex structural changes:

```python
import nbformat
nb = nbformat.read('notebook.ipynb', as_version=4)
# Modify cells via nb.cells[i].source (string, not list — nbformat handles conversion)
nbformat.write(nb, 'notebook.ipynb')
```

## Post-Edit Verification Checklist

After every programmatic notebook edit, complete ALL of these steps:

**1. Integrity check** — detect corruption:
```python
import json
with open('notebook.ipynb') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    src = cell.get('source', [])
    if src and any(len(s) == 1 and s != '\n' for s in src[:5]):
        print(f"CORRUPTED: Cell {i}")
```

**2. Execution check** — verify the notebook runs cleanly:
```bash
uv run jupyter nbconvert --to notebook --execute NOTEBOOK.ipynb --output /tmp/test-output.ipynb
```
This catches errors that visual inspection misses — stale column names, invalid arguments, import errors.

**3. VS Code cache warning** — If the user has the notebook open in VS Code, tell them to **close and reopen the notebook tab**. VS Code caches notebook files in memory and will not pick up on-disk changes to an already-open file.

## Corruption Detection and Repair

If corruption has already occurred (cells show one character per line), use this repair pattern:

```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    src = cell.get('source', [])
    if src and any(len(s) == 1 and s != '\n' for s in src[:5]):
        # Rejoin single characters back into original text
        full_text = ''.join(src)
        # Re-split on newlines to restore proper source array
        cell['source'] = [line + '\n' for line in full_text.split('\n')]
        # Clean up trailing empty/newline entries
        if cell['source'] and cell['source'][-1] == '\n':
            cell['source'][-1] = ''
        if cell['source'] and cell['source'][-1] == '':
            cell['source'].pop()
        print(f"Repaired cell {i}")

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

After repair, run both the integrity check and execution check from the verification checklist above.

## Git Commit Rules for Notebooks

**Always clear all cell outputs before committing notebooks to git.**

Notebook outputs (rendered HTML tables, Plotly JSON, matplotlib images) can be hundreds of KB to several MB. They bloat the repo, create noisy diffs, and may contain sensitive data. The source cells are what matter — outputs are regenerated on execution.

**Before staging any .ipynb for commit:**
```bash
uv run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to notebook --output NOTEBOOK.ipynb NOTEBOOK.ipynb
```

Or programmatically:
```python
import json

with open('notebook.ipynb') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

with open('notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

**Why:** A single Plotly Sankey chart with 63 nodes can add 150KB+ of JSON to the notebook. A matplotlib chart embeds a base64-encoded PNG. Over multiple commits, outputs accumulate into MB of binary diff noise that `git diff` cannot display usefully.
