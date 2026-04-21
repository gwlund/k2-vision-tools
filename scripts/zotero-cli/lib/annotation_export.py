"""Annotation export to markdown.

This module provides functions to export Zotero annotations to markdown files
with support for Obsidian templates and various export modes.
"""

from pathlib import Path
from typing import Optional
import re


def get_all_annotations(api, item_key: str, tag_filter: Optional[str] = None) -> list[dict]:
    """Get all annotations for an item, optionally filtered by tag.

    Args:
        api: ZoteroAPI instance
        item_key: Item key
        tag_filter: Optional tag to filter annotations

    Returns:
        list: Annotations with metadata
    """
    return api.get_pdf_annotations(item_key, tag_filter)


def format_annotation_markdown(annotation: dict, item_metadata: dict) -> str:
    """Format single annotation as markdown.

    Default format:
        ## Topic/Section (page N)

        > Highlighted text

        *Note: annotation comment*

        Tags: #tag1 #tag2

    Args:
        annotation: Annotation dictionary
        item_metadata: Parent item metadata

    Returns:
        str: Formatted markdown
    """
    md = []

    # Header with page number
    page = annotation.get('page', '?')
    md.append(f"## Page {page}\n")

    # Highlighted text as blockquote
    if annotation.get('text'):
        text = annotation['text'].strip()
        md.append(f"> {text}\n")

    # Comment/note
    if annotation.get('comment'):
        comment = annotation['comment'].strip()
        md.append(f"*{comment}*\n")

    # Tags
    if annotation.get('tags'):
        tag_str = ' '.join([f"#{t['tag']}" for t in annotation['tags']])
        md.append(f"**Tags:** {tag_str}\n")

    md.append("---\n")

    return '\n'.join(md)


def export_item_annotations(api, item_key: str,
                           output_path: Path,
                           tag_filter: Optional[str] = None,
                           template_path: Optional[Path] = None) -> int:
    """Export annotations for single item to markdown file.

    Args:
        api: ZoteroAPI instance
        item_key: Item key
        output_path: Output file path
        tag_filter: Optional tag filter
        template_path: Optional template file

    Returns:
        int: Number of annotations exported
    """
    # Get item metadata
    item = api.get_item(item_key)
    item_data = item['data']

    # Get annotations
    annotations = get_all_annotations(api, item_key, tag_filter)

    if not annotations:
        return 0

    # Apply template if provided
    if template_path and template_path.exists():
        content = apply_obsidian_template(annotations, item_data, template_path)
    else:
        # Default format
        content = _format_default_export(annotations, item_data)

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)

    return len(annotations)


def _format_default_export(annotations: list[dict], item_metadata: dict) -> str:
    """Format annotations with default template.

    Args:
        annotations: List of annotations
        item_metadata: Item metadata

    Returns:
        str: Formatted markdown
    """
    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f"title: {item_metadata.get('title', 'Untitled')}")

    if 'creators' in item_metadata and item_metadata['creators']:
        creator = item_metadata['creators'][0]
        creator_name = creator.get('name', '') or f"{creator.get('firstName', '')} {creator.get('lastName', '')}".strip()
        lines.append(f"creator: {creator_name}")

    if 'date' in item_metadata:
        lines.append(f"date: {item_metadata['date']}")

    lines.append(f"zotero_key: {item_metadata.get('key', '')}")
    lines.append("type: zotero-annotations")
    lines.append("---\n")

    # Title
    lines.append(f"# {item_metadata.get('title', 'Untitled')}\n")

    # Metadata
    if 'creators' in item_metadata and item_metadata['creators']:
        creator = item_metadata['creators'][0]
        creator_name = creator.get('name', '') or f"{creator.get('firstName', '')} {creator.get('lastName', '')}".strip()
        lines.append(f"**Author:** {creator_name}")

    if 'date' in item_metadata:
        lines.append(f"**Date:** {item_metadata['date']}")

    lines.append(f"\n[Open in Zotero](zotero://select/items/{item_metadata.get('key', '')})\n")
    lines.append("---\n")

    # Annotations
    lines.append(f"## Annotations ({len(annotations)})\n")

    for ann in annotations:
        lines.append(format_annotation_markdown(ann, item_metadata))

    return '\n'.join(lines)


def export_collection_annotations(api, collection: str,
                                 output_dir: Path,
                                 tag_filter: Optional[str] = None) -> dict[str, int]:
    """Export annotations for all items in collection.

    Args:
        api: ZoteroAPI instance
        collection: Collection name
        output_dir: Output directory
        tag_filter: Optional tag filter

    Returns:
        dict: {item_key: annotation_count}
    """
    # Get collection key
    collection_key = api.get_collection_key(collection)
    if not collection_key:
        raise ValueError(f"Collection '{collection}' not found")

    # Get items in collection
    items = api.get_collection_items(collection)

    results = {}
    output_dir.mkdir(parents=True, exist_ok=True)

    for item in items:
        item_key = item['key']
        title = item['data'].get('title', 'Untitled')

        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        output_path = output_dir / f"{safe_title}.md"

        # Export annotations
        count = export_item_annotations(api, item_key, output_path, tag_filter)
        results[item_key] = count

    return results


def export_cross_document_by_tag(api, tag: str,
                                output_path: Path,
                                collection: Optional[str] = None) -> int:
    """Export annotations with specific tag from multiple documents.

    Groups annotations by tag across all documents.

    Args:
        api: ZoteroAPI instance
        tag: Tag to filter by
        output_path: Output file path
        collection: Optional collection to limit search

    Returns:
        int: Total annotations exported
    """
    # Get items
    if collection:
        collection_key = api.get_collection_key(collection)
        if not collection_key:
            raise ValueError(f"Collection '{collection}' not found")
        items = api.get_collection_items(collection)
    else:
        # Get all items
        items = api.zot.everything(api.zot.items())

    # Collect all annotations with tag
    all_annotations = []

    for item in items:
        item_key = item['key']
        item_title = item['data'].get('title', 'Untitled')

        # Get annotations
        annotations = get_all_annotations(api, item_key, tag_filter=tag)

        # Add source information
        for ann in annotations:
            ann['source_title'] = item_title
            ann['source_key'] = item_key

        all_annotations.extend(annotations)

    if not all_annotations:
        return 0

    # Format output
    lines = []
    lines.append("---")
    lines.append(f"title: Annotations tagged '{tag}'")
    lines.append(f"tag: {tag}")
    lines.append("type: cross-document-annotations")
    lines.append("---\n")

    lines.append(f"# Annotations: {tag}\n")
    lines.append(f"**Total:** {len(all_annotations)} annotations\n")
    lines.append("---\n")

    # Group by source document
    by_source = {}
    for ann in all_annotations:
        source_key = ann['source_key']
        if source_key not in by_source:
            by_source[source_key] = {
                'title': ann['source_title'],
                'annotations': []
            }
        by_source[source_key]['annotations'].append(ann)

    # Output grouped annotations
    for source_key, data in by_source.items():
        lines.append(f"## {data['title']}\n")
        lines.append(f"[Open in Zotero](zotero://select/items/{source_key})\n")

        for ann in data['annotations']:
            page = ann.get('page', '?')
            lines.append(f"### Page {page}\n")

            if ann.get('text'):
                lines.append(f"> {ann['text']}\n")

            if ann.get('comment'):
                lines.append(f"*{ann['comment']}*\n")

            lines.append("---\n")

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    return len(all_annotations)


def apply_obsidian_template(annotations: list[dict],
                           item_metadata: dict,
                           template_path: Path) -> str:
    """Apply Obsidian template to generate markdown.

    Template variables:
        {{title}}, {{creator}}, {{date}}, {{tags}}, {{zotero_key}}
        {{annotations}} - list of annotations

    Args:
        annotations: List of annotations
        item_metadata: Item metadata
        template_path: Path to template file

    Returns:
        str: Rendered markdown
    """
    # Load template
    with open(template_path, 'r') as f:
        template = f.read()

    # Extract metadata
    title = item_metadata.get('title', 'Untitled')

    creator_name = ''
    if 'creators' in item_metadata and item_metadata['creators']:
        creator = item_metadata['creators'][0]
        creator_name = creator.get('name', '') or f"{creator.get('firstName', '')} {creator.get('lastName', '')}".strip()

    date = item_metadata.get('date', '')
    place = item_metadata.get('place', '')
    zotero_key = item_metadata.get('key', '')

    # Get tags from metadata
    tags = []
    if 'tags' in item_metadata:
        tags = [t['tag'] for t in item_metadata['tags']]
    tag_str = ', '.join(tags)

    # Simple template substitution
    output = template
    output = output.replace('{{title}}', title)
    output = output.replace('{{creator}}', creator_name)
    output = output.replace('{{date}}', date)
    output = output.replace('{{place}}', place)
    output = output.replace('{{tags}}', tag_str)
    output = output.replace('{{zotero_key}}', zotero_key)

    # Format annotations
    annotation_md = []
    for ann in annotations:
        annotation_md.append(format_annotation_markdown(ann, item_metadata))

    output = output.replace('{{annotations}}', '\n'.join(annotation_md))

    return output
