"""PDF metadata extraction from multiple sources.

This module provides functions to extract metadata from PDFs using:
1. Embedded PDF metadata
2. OCR text extraction with Tesseract
3. Title page text parsing
4. Combination and prioritization of sources
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None


def extract_embedded_metadata(pdf_path: Path) -> Dict[str, str]:
    """Extract metadata from PDF's internal metadata fields.

    Args:
        pdf_path: Path to PDF file

    Returns:
        dict: {title, author, subject, keywords, creator, producer, creation_date}
    """
    if not PdfReader:
        return {}

    metadata = {}

    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            info = reader.metadata

            if info:
                # Extract standard fields
                metadata['title'] = info.get('/Title', '').strip()
                metadata['author'] = info.get('/Author', '').strip()
                metadata['subject'] = info.get('/Subject', '').strip()
                metadata['keywords'] = info.get('/Keywords', '').strip()
                metadata['creator'] = info.get('/Creator', '').strip()
                metadata['producer'] = info.get('/Producer', '').strip()

                # Extract creation date
                creation_date = info.get('/CreationDate', '')
                if creation_date:
                    metadata['creation_date'] = creation_date

    except Exception as e:
        # Silently fail - we'll try other extraction methods
        pass

    # Remove empty values
    return {k: v for k, v in metadata.items() if v}


def extract_text_from_pages(pdf_path: Path, pages: List[int] = None,
                            tesseract_path: str = '/opt/homebrew/bin/tesseract') -> str:
    """Extract text from specified pages using Tesseract OCR.

    Args:
        pdf_path: Path to PDF file
        pages: List of page numbers (0-indexed) to extract, default [0, 1]
        tesseract_path: Path to tesseract binary

    Returns:
        str: Extracted text from all specified pages
    """
    if not convert_from_path:
        return ""

    if pages is None:
        pages = [0, 1]  # Default: first two pages

    all_text = []

    try:
        # Convert PDF pages to images
        # pages are 0-indexed in our API but 1-indexed for pdf2image
        first_page = min(pages) + 1
        last_page = max(pages) + 1

        images = convert_from_path(
            str(pdf_path),
            first_page=first_page,
            last_page=last_page,
            dpi=300
        )

        # OCR each image
        for i, image in enumerate(images):
            page_num = first_page - 1 + i
            if page_num not in pages:
                continue

            # Save image temporarily
            temp_img = f"/tmp/pdf_page_{page_num}.png"
            image.save(temp_img, 'PNG')

            # Run tesseract
            result = subprocess.run(
                [tesseract_path, temp_img, 'stdout'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                all_text.append(result.stdout)

            # Cleanup
            Path(temp_img).unlink(missing_ok=True)

    except Exception as e:
        # Silently fail - return whatever we got
        pass

    return '\n\n'.join(all_text)


def parse_title_page_metadata(text: str) -> Dict[str, str]:
    """Parse metadata from title page text.

    Common patterns for CEDS reports and planning documents:
    - Title: Usually first 1-3 lines, all caps or title case
    - Organization: Look for "prepared by", "by:", etc.
    - Date: YYYY or YYYY-YYYY patterns
    - Place: City, State patterns

    Args:
        text: Extracted text from title page

    Returns:
        dict: {title, creator, date, place}
    """
    metadata = {}
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    if not lines:
        return metadata

    # Extract title (usually first significant line)
    # Look for lines with 3+ words and proper capitalization
    for i, line in enumerate(lines[:10]):  # Check first 10 lines
        words = line.split()
        if len(words) >= 3 and len(line) > 15:
            # Skip lines that look like headers/footers
            if not re.match(r'^\d+$', line) and 'page' not in line.lower():
                metadata['title'] = line
                break

    # Extract organization/creator
    org_patterns = [
        r'(?:prepared\s+by|by):?\s*(.+)',
        r'(?:prepared\s+for):?\s*(.+)',
        r'(.+(?:council|commission|department|district|authority))',
    ]

    for line in lines:
        for pattern in org_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                metadata['creator'] = match.group(1).strip()
                break
        if 'creator' in metadata:
            break

    # Extract date (YYYY or YYYY-YYYY)
    # Try year range first, then single year
    for line in lines:
        # Year range pattern (must come first)
        range_match = re.search(r'\b(20\d{2})\s*-\s*(20\d{2})\b', line)
        if range_match:
            metadata['date'] = f"{range_match.group(1)}-{range_match.group(2)}"
            break

        # Single year
        year_match = re.search(r'\b(20\d{2})\b', line)
        if year_match:
            metadata['date'] = year_match.group(1)
            break

        # Older docs
        old_year_match = re.search(r'\b(19\d{2})\b', line)
        if old_year_match:
            metadata['date'] = old_year_match.group(1)
            break

    # Extract place (City, State or City, ST)
    # Match: "City Name, State Name" or "City, ST"
    place_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?|[A-Z]{2})'

    for line in lines:
        match = re.search(place_pattern, line)
        if match:
            metadata['place'] = f"{match.group(1)}, {match.group(2)}"
            break

    return metadata


def combine_metadata_sources(embedded: Dict[str, str],
                             parsed: Dict[str, str],
                             user_provided: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Merge metadata from multiple sources with priority.

    Priority: user_provided > parsed > embedded

    Args:
        embedded: Metadata from PDF metadata fields
        parsed: Metadata from title page parsing
        user_provided: User-specified metadata (overrides all)

    Returns:
        dict: Combined metadata with confidence scores
    """
    combined = {}

    # Field mapping: normalize different field names
    field_map = {
        'title': 'title',
        'author': 'creator',
        'creator': 'creator',
        'subject': 'subject',
        'date': 'date',
        'creation_date': 'date',
        'place': 'place',
        'keywords': 'keywords',
    }

    # Start with embedded (lowest priority)
    for key, value in embedded.items():
        normalized_key = field_map.get(key, key)
        if value and normalized_key not in combined:
            combined[normalized_key] = value

    # Override with parsed (medium priority)
    for key, value in parsed.items():
        normalized_key = field_map.get(key, key)
        if value:
            combined[normalized_key] = value

    # Override with user-provided (highest priority)
    if user_provided:
        for key, value in user_provided.items():
            normalized_key = field_map.get(key, key)
            if value:
                combined[normalized_key] = value

    return combined


def normalize_zotero_item_type(document_type: str) -> str:
    """Map document types to Zotero item types.

    Args:
        document_type: Document type (e.g., "CEDS", "Housing Element")

    Returns:
        str: Zotero item type
    """
    type_map = {
        'ceds': 'report',
        'comprehensive economic development strategy': 'report',
        'housing element': 'report',
        'comprehensive plan': 'report',
        'general plan': 'report',
        'strategic plan': 'report',
        'master plan': 'report',
        'policy document': 'report',
        'white paper': 'report',
        'technical report': 'report',
        'research report': 'report',
    }

    doc_type_lower = document_type.lower().strip()
    return type_map.get(doc_type_lower, 'document')
