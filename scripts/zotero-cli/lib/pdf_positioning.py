"""
PDF Annotation Positioning for Zotero

Generates annotationSortIndex and annotationPosition fields required for
annotations to be visible in Zotero's PDF reader.

This module implements the positioning algorithms reverse-engineered from
Zotero's reader/src/pdf/selection.js. See docs/zotero-algorithm-research.md
for complete algorithm documentation.

Usage:
    from lib.pdf_positioning import create_positioned_highlight
    from pathlib import Path

    # Create positioned highlight
    result = create_positioned_highlight(
        pdf_path=Path('document.pdf'),
        page_index=0,
        rects=[[100, 200, 300, 210]],
        text='highlighted text',
        color='#ffd400',
        comment='My comment'
    )

    # Result contains all Zotero annotation fields
    annotation = {
        'itemType': 'annotation',
        'annotationType': 'highlight',
        'annotationText': result['text'],
        'annotationColor': result['color'],
        'annotationComment': result['comment'],
        'annotationSortIndex': result['sortIndex'],  # NEW: enables visibility
        'annotationPosition': result['position'],     # NEW: enables visibility
        'annotationPageLabel': result['pageLabel'],
        ...
    }
"""

import json
import math
from pathlib import Path
from typing import Optional

from pdf_text_extraction import extract_pdf_pages_data


# =============================================================================
# Rect Utilities
# =============================================================================

def expand_rect(rect: list[float], padding: float = 0.5) -> list[float]:
    """Expand a rectangle by padding on all sides.

    This ensures that character center points fall within the rect bounds,
    which is required for Zotero's getRangeByHighlight() to successfully
    match text characters.

    See CRITICAL-FINDING-highlight-to-area-conversion.md for details.

    Args:
        rect: Rectangle [x1, y1, x2, y2] in PDF coordinates
        padding: Units to expand on each side (default: 2.0)

    Returns:
        Expanded rectangle [x1-pad, y1-pad, x2+pad, y2+pad]

    Example:
        >>> expand_rect([100, 200, 150, 210], padding=2)
        [98.0, 198.0, 152.0, 212.0]
    """
    return [
        rect[0] - padding,
        rect[1] - padding,
        rect[2] + padding,
        rect[3] + padding
    ]


def expand_rects(rects: list[list[float]], padding: float = 2.0) -> list[list[float]]:
    """Expand multiple rectangles by padding on all sides.

    Args:
        rects: List of rectangles [[x1, y1, x2, y2], ...]
        padding: Units to expand on each side (default: 2.0)

    Returns:
        List of expanded rectangles
    """
    return [expand_rect(rect, padding) for rect in rects]


def flip_y_coordinates(
    rects: list[list[float]],
    page_height: float
) -> list[list[float]]:
    """Flip Y-coordinates from bottom-up to top-down coordinate system.

    PDF character data uses bottom-up coordinates (y=0 at bottom), but Zotero's
    annotation system uses top-down coordinates (y=0 at top). This function
    converts between the two systems.

    Args:
        rects: List of rectangles in bottom-up coordinates [[x1, y1, x2, y2], ...]
        page_height: Height of the page in PDF units

    Returns:
        List of rectangles in top-down coordinates

    Example:
        >>> flip_y_coordinates([[100, 200, 150, 210]], page_height=792)
        [[100.0, 582.0, 150.0, 592.0]]
    """
    flipped = []
    for rect in rects:
        x1, y1, x2, y2 = rect
        # Flip Y coordinates: new_y = page_height - old_y
        # Note: y1 and y2 swap because coordinate system flips
        flipped_rect = [
            x1,
            page_height - y2,  # Top becomes bottom
            x2,
            page_height - y1   # Bottom becomes top
        ]
        flipped.append(flipped_rect)
    return flipped


# =============================================================================
# Core Positioning Algorithms (ported from Zotero JavaScript)
# =============================================================================

def rects_dist(rect_a: list[float], rect_b: list[float]) -> float:
    """Calculate minimum distance between two rectangles.

    Ported from: third-party/zotero/reader/src/pdf/selection.js::rectsDist()

    Args:
        rect_a: Rectangle [x1, y1, x2, y2]
        rect_b: Rectangle [x1, y1, x2, y2]

    Returns:
        float: Minimum distance between rectangles (0 if overlapping)
    """
    ax1, ay1, ax2, ay2 = rect_a
    bx1, by1, bx2, by2 = rect_b

    left = bx2 < ax1
    right = ax2 < bx1
    bottom = by2 < ay1
    top = ay2 < by1

    # Diagonal corners - Euclidean distance
    if top and left:
        return math.hypot(ax1 - bx2, ay2 - by1)
    elif left and bottom:
        return math.hypot(ax1 - bx2, ay1 - by2)
    elif bottom and right:
        return math.hypot(ax2 - bx1, ay1 - by2)
    elif right and top:
        return math.hypot(ax2 - bx1, ay2 - by1)

    # Edge-to-edge distances
    elif left:
        return ax1 - bx2
    elif right:
        return bx1 - ax2
    elif bottom:
        return ay1 - by2
    elif top:
        return by1 - ay2

    # Overlapping or touching
    return 0.0


def get_closest_offset(chars: list[dict], rect: list[float]) -> int:
    """Find index of character closest to given rectangle.

    Ported from: third-party/zotero/reader/src/pdf/selection.js::getClosestOffset()

    Args:
        chars: Array of character objects with 'rect' property
        rect: Target rectangle [x1, y1, x2, y2]

    Returns:
        int: Index of closest character (0 if chars is empty)
    """
    if not chars:
        return 0

    min_dist = float('inf')
    closest_idx = 0

    for i, ch in enumerate(chars):
        distance = rects_dist(ch['rect'], rect)
        if distance < min_dist:
            min_dist = distance
            closest_idx = i

    return closest_idx


def get_topmost_rect_from_position(position: dict) -> Optional[list[float]]:
    """Get rectangle with highest y2 value (topmost in PDF coordinates).

    Ported from: third-party/zotero/reader/src/pdf/selection.js

    Args:
        position: Position object with 'rects' array

    Returns:
        Topmost rectangle or None if no rects
    """
    rects = position.get('rects', [])
    if not rects:
        return None

    # Sort by y2 descending (highest y2 = topmost)
    return max(rects, key=lambda r: r[3])


def get_position_bounding_rect(position: dict) -> Optional[list[float]]:
    """Get bounding rectangle that contains all rects in position.

    Args:
        position: Position object with 'rects' array

    Returns:
        Bounding rectangle [x1, y1, x2, y2] or None
    """
    rects = position.get('rects', [])
    if not rects:
        return None

    x1 = min(r[0] for r in rects)
    y1 = min(r[1] for r in rects)
    x2 = max(r[2] for r in rects)
    y2 = max(r[3] for r in rects)

    return [x1, y1, x2, y2]


def generate_sort_index(
    page_index: int,
    rects: list[list[float]],
    chars: Optional[list[dict]] = None,
    view_box: Optional[list[float]] = None
) -> str:
    """Generate Zotero annotationSortIndex.

    Ported from: third-party/zotero/reader/src/pdf/selection.js::getSortIndex()

    Args:
        page_index: 0-based page index
        rects: Bounding rectangles [[x1, y1, x2, y2], ...]
        chars: Optional list of character objects with 'rect' property
        view_box: Optional PDF viewBox [minX, minY, maxX, maxY]

    Returns:
        str: Sort index like "00014|000103|00823"

    Algorithm:
        Format: "{pageIndex:05d}|{offset:06d}|{top:05d}"
        1. Page: Zero-pad page_index to 5 digits
        2. Offset: Find closest character offset from chars array (0 if not available)
        3. Top: Calculate distance from page top (pageHeight - rect[3])
    """
    offset = 0
    top = 0

    if view_box is not None and rects:
        position = {'pageIndex': page_index, 'rects': rects}

        # Get topmost rect (highest y2 value)
        rect = get_topmost_rect_from_position(position) or get_position_bounding_rect(position)

        # Calculate offset from chars if available
        if chars and len(chars) > 0:
            offset = get_closest_offset(chars, rect)

        # Calculate top position
        page_height = view_box[3] - view_box[1]
        top = page_height - rect[3]
        if top < 0:
            top = 0

    # Format: pageIndex(5) | offset(6) | top(5)
    return '|'.join([
        str(page_index).zfill(5)[:5],
        str(offset).zfill(6)[:6],
        str(int(top)).zfill(5)[:5]
    ])


def generate_position_json(page_index: int, rects: list[list[float]]) -> str:
    """Generate Zotero annotationPosition JSON string.

    Ported from: third-party/zotero/reader/src/pdf/selection.js

    Args:
        page_index: 0-based page index
        rects: Bounding rectangles [[x1, y1, x2, y2], ...]

    Returns:
        str: JSON string like '{"pageIndex":14,"rects":[[144.02,518.23,535.49,529.27]]}'
    """
    position = {
        'pageIndex': page_index,
        'rects': rects
    }
    return json.dumps(position, separators=(',', ':'))


# =============================================================================
# High-Level API for Creating Positioned Annotations
# =============================================================================

def create_positioned_highlight(
    pdf_path: Path | str,
    page_index: int,
    rects: list[list[float]],
    text: str = '',
    color: str = '#ffd400',
    comment: str = '',
    tags: Optional[list[str]] = None
) -> dict:
    """Create positioned highlight annotation data for Zotero.

    This extracts character data from the PDF and generates the annotationSortIndex
    and annotationPosition fields required for the highlight to be visible in
    Zotero's PDF reader.

    Args:
        pdf_path: Path to PDF file
        page_index: Zero-based page index (page 1 = index 0)
        rects: Bounding rectangles for highlight [[x1, y1, x2, y2], ...]
               PDF coordinates: origin at bottom-left, y-axis points up
        text: Text being highlighted
        color: Hex color code (default: yellow #ffd400)
        comment: Annotation comment/note
        tags: Optional list of tag strings

    Returns:
        dict: Annotation data ready for Zotero API:
        {
            'text': str,
            'color': str,
            'comment': str,
            'tags': list[str],
            'pageLabel': str,
            'sortIndex': str,    # annotationSortIndex for Zotero
            'position': str,     # annotationPosition for Zotero
        }

    Example:
        >>> result = create_positioned_highlight(
        ...     pdf_path='document.pdf',
        ...     page_index=0,
        ...     rects=[[230.202, 578.879, 275.478, 585.817]],
        ...     text='This is important',
        ...     comment='Key finding'
        ... )
        >>> result['sortIndex']
        '00000|000873|00206'
        >>> result['position']
        '{"pageIndex":0,"rects":[[230.202,578.879,275.478,585.817]]}'
    """
    pdf_path = Path(pdf_path)

    # Expand rects by 0.5 units to ensure character center points fall within bounds.
    # This provides a safety margin for Zotero's getRangeByHighlight() character matching.
    # Note: This does NOT fix the area annotation display issue - API-created annotations
    # display as area annotations regardless of expansion. See docs/API-ANNOTATION-AREA-ISSUE.md
    expanded_rects = expand_rects(rects, padding=0.5)

    # Extract character data from PDF page
    pdf_pages = extract_pdf_pages_data(pdf_path, [page_index])

    if page_index not in pdf_pages:
        raise ValueError(f"Could not extract page {page_index} from PDF")

    page_data = pdf_pages[page_index]
    chars = page_data['chars']
    view_box = page_data['viewBox']
    page_height = view_box[3] - view_box[1]

    # Generate sort index using expanded rects (still in bottom-up coordinates)
    # Sort index calculation needs to match against character data which uses bottom-up
    sort_index = generate_sort_index(
        page_index=page_index,
        rects=expanded_rects,
        chars=chars,
        view_box=view_box
    )

    # CRITICAL FIX: Flip Y-coordinates from PDF bottom-up to Zotero top-down
    # PDF uses y=0 at bottom, Zotero annotations use y=0 at top
    # This must happen AFTER sort index generation
    flipped_rects = flip_y_coordinates(expanded_rects, page_height)

    # Generate position JSON using flipped rects
    position = generate_position_json(page_index, flipped_rects)

    # Page label is 1-indexed (page 1, not page 0)
    page_label = str(page_index + 1)

    return {
        'text': text,
        'color': color,
        'comment': comment,
        'tags': tags or [],
        'pageLabel': page_label,
        'sortIndex': sort_index,
        'position': position
    }


def create_positioned_note(
    pdf_path: Path | str,
    page_index: int,
    rects: list[list[float]],
    comment: str = '',
    tags: Optional[list[str]] = None
) -> dict:
    """Create positioned note annotation data for Zotero.

    Similar to create_positioned_highlight but for note annotations.
    Notes don't have highlighted text, just a comment at a position.

    Args:
        pdf_path: Path to PDF file
        page_index: Zero-based page index
        rects: Bounding rectangles [[x1, y1, x2, y2], ...]
        comment: Note text
        tags: Optional list of tag strings

    Returns:
        dict: Annotation data ready for Zotero API
    """
    # Use same logic as highlight, just without text
    result = create_positioned_highlight(
        pdf_path=pdf_path,
        page_index=page_index,
        rects=rects,
        text='',
        comment=comment,
        tags=tags
    )

    # Notes don't have color
    result.pop('color', None)

    return result
