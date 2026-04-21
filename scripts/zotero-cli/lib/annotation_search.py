"""Annotation search functionality.

This module provides functions to search annotations by text content
with various filters and formatting options.
"""

from typing import Optional
import re


def search_annotations(api, query: str,
                      collection: Optional[str] = None,
                      tag: Optional[str] = None,
                      item_key: Optional[str] = None) -> list[dict]:
    """Search annotations by text content.

    Args:
        api: ZoteroAPI instance
        query: Search query
        collection: Optional collection filter
        tag: Optional tag filter
        item_key: Optional single item filter

    Returns:
        list: [
            {
                'item_key': item_key,
                'item_title': title,
                'annotation_key': ann_key,
                'text': highlighted_text,
                'comment': annotation_comment,
                'page': page_number,
                'tags': [tags],
                'match_context': context_around_match
            }
        ]
    """
    results = []

    # Get items to search
    if item_key:
        # Search single item
        items = [api.get_item(item_key)]
    elif collection:
        # Search collection
        collection_key = api.get_collection_key(collection)
        if not collection_key:
            return []
        items = api.get_collection_items(collection)
    else:
        # Search all items
        items = api.zot.everything(api.zot.items())

    # Normalize query for case-insensitive search
    query_lower = query.lower()

    # Search annotations in each item
    for item in items:
        if not item:
            continue

        curr_item_key = item['key']
        item_title = item['data'].get('title', 'Untitled')

        # Get annotations
        annotations = api.get_pdf_annotations(curr_item_key, tag_filter=tag)

        for ann in annotations:
            # Search in text
            text = ann.get('text', '')
            comment = ann.get('comment', '')

            # Check if query matches
            if query_lower in text.lower() or query_lower in comment.lower():
                # Extract context around match
                context = _extract_match_context(text, comment, query)

                results.append({
                    'item_key': curr_item_key,
                    'item_title': item_title,
                    'annotation_key': ann['key'],
                    'text': text,
                    'comment': comment,
                    'page': ann.get('page', '?'),
                    'tags': ann.get('tags', []),
                    'match_context': context
                })

    return results


def _extract_match_context(text: str, comment: str, query: str, context_chars: int = 100) -> str:
    """Extract context around match.

    Args:
        text: Highlighted text
        comment: Comment text
        query: Search query
        context_chars: Characters of context on each side

    Returns:
        str: Context snippet with match
    """
    # Try to find in text first
    search_in = text if query.lower() in text.lower() else comment

    query_lower = query.lower()
    text_lower = search_in.lower()

    # Find match position
    match_pos = text_lower.find(query_lower)

    if match_pos == -1:
        # No match (shouldn't happen)
        return search_in[:200]

    # Extract context
    start = max(0, match_pos - context_chars)
    end = min(len(search_in), match_pos + len(query) + context_chars)

    context = search_in[start:end]

    # Add ellipsis if truncated
    if start > 0:
        context = '...' + context
    if end < len(search_in):
        context = context + '...'

    return context


def highlight_search_matches(text: str, query: str) -> str:
    """Highlight search query in text using Rich markup.

    Args:
        text: Text to highlight
        query: Query to highlight

    Returns:
        str: Text with [bold yellow] markup around matches
    """
    # Case-insensitive replacement
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(lambda m: f'[bold yellow]{m.group()}[/bold yellow]', text)


def format_search_results(results: list[dict], context_lines: int = 0) -> str:
    """Format search results for display.

    Args:
        results: Search results
        context_lines: Additional context lines (not used in current implementation)

    Returns:
        str: Formatted results
    """
    if not results:
        return "No matches found"

    lines = []

    for i, result in enumerate(results, 1):
        lines.append(f"\n[{i}] {result['item_title']} (Page {result['page']})")
        lines.append(f"    [dim]Item: {result['item_key']} | Annotation: {result['annotation_key']}[/dim]")

        # Show context
        if result['match_context']:
            lines.append(f"    {result['match_context']}")

        # Show comment if present
        if result['comment']:
            lines.append(f"    [dim]Note: {result['comment']}[/dim]")

        # Show tags
        if result['tags']:
            tag_names = [t['tag'] for t in result['tags']]
            tag_str = ', '.join(tag_names)
            lines.append(f"    [dim]Tags: {tag_str}[/dim]")

    return '\n'.join(lines)
