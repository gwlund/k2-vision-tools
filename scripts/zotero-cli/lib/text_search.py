"""
Text search using Zotero's character extraction.

This uses the same character data that Zotero uses internally, ensuring
coordinate compatibility.
"""

from pathlib import Path
from typing import List
from dataclasses import dataclass

from pdf_text_extraction import extract_pdf_pages_data


@dataclass
class SearchMatch:
    """A text search match with position information."""
    page_index: int
    text: str
    rects: List[List[float]]
    char_start: int
    char_end: int


def search_text_in_pdf(
    pdf_path: Path | str,
    search_text: str,
    page_index: int | None = None
) -> List[SearchMatch]:
    """Search for text in PDF using Zotero's character extraction.

    This ensures coordinates match what Zotero expects, unlike PDF.js
    which can have coordinate offsets.

    Args:
        pdf_path: Path to PDF file
        search_text: Text to search for (case-insensitive)
        page_index: Optional page index to search (None = all pages)

    Returns:
        List of SearchMatch objects with matched text and positions
    """
    pdf_path = Path(pdf_path)

    # Determine which pages to extract
    if page_index is not None:
        pages_to_extract = [page_index]
    else:
        # Extract all pages (this could be slow for large PDFs)
        # In the future, we could add page count detection
        pages_to_extract = list(range(100))  # Max 100 pages

    # Extract character data
    pdf_pages = extract_pdf_pages_data(pdf_path, pages_to_extract)

    matches = []
    search_lower = search_text.lower()

    for page_idx, page_data in pdf_pages.items():
        chars = page_data['chars']

        # Build text string and track character indices
        text_buffer = ""
        char_map = []  # Maps text position to character index

        for i, char in enumerate(chars):
            if not char.get('ignorable', False):
                text_buffer += char['c']
                char_map.append(i)

                # Add spaces
                if char.get('spaceAfter') or char.get('lineBreakAfter'):
                    text_buffer += ' '
                    char_map.append(None)  # Space doesn't map to a char

        # Search for matches
        import re
        for match in re.finditer(re.escape(search_lower), text_buffer.lower()):
            start_pos = match.start()
            end_pos = match.end() - 1

            # Map text positions back to character indices
            # Skip None entries (spaces)
            valid_char_map = [(i, char_map[i]) for i in range(len(char_map))
                             if char_map[i] is not None]

            if start_pos >= len(valid_char_map) or end_pos >= len(valid_char_map):
                continue

            char_start_idx = valid_char_map[start_pos][1]
            char_end_idx = valid_char_map[end_pos][1]

            # Get character rects
            matched_chars = chars[char_start_idx:char_end_idx + 1]

            # Calculate bounding rects by line
            rects = _get_rects_from_chars(matched_chars)

            # Get actual matched text
            matched_text = ''.join(
                c['c'] for c in matched_chars
                if not c.get('ignorable', False)
            )

            matches.append(SearchMatch(
                page_index=page_idx,
                text=matched_text,
                rects=rects,
                char_start=char_start_idx,
                char_end=char_end_idx
            ))

    return matches


def _get_rects_from_chars(chars: List[dict]) -> List[List[float]]:
    """Get bounding rectangles from characters, grouped by line.

    This matches Zotero's getRectsFromChars() behavior.
    """
    if not chars:
        return []

    line_rects = []
    current_rect = None

    for char in chars:
        if char.get('ignorable', False):
            continue

        char_rect = char.get('inlineRect', char['rect'])

        if current_rect is None:
            current_rect = char_rect[:]
        else:
            # Expand current rect to include this character
            current_rect = [
                min(current_rect[0], char_rect[0]),
                min(current_rect[1], char_rect[1]),
                max(current_rect[2], char_rect[2]),
                max(current_rect[3], char_rect[3])
            ]

        # Check for line break
        if char.get('lineBreakAfter', False):
            line_rects.append(current_rect)
            current_rect = None

    # Add final rect if exists
    if current_rect is not None:
        line_rects.append(current_rect)

    return line_rects
