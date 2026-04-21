"""PDF text extraction for LLM analysis and Zotero annotations.

This module provides functions to:
1. Extract full text, tables, and images from PDFs for LLM analysis
2. Extract character-level text data for Zotero positioned annotations
"""

from pathlib import Path
from typing import Optional
import subprocess


def extract_full_text(pdf_path: Path, use_ocr: bool = True,
                     tesseract_path: str = '/opt/homebrew/bin/tesseract') -> str:
    """Extract all text from PDF.

    Args:
        pdf_path: Path to PDF
        use_ocr: Whether to use OCR for scanned pages
        tesseract_path: Path to Tesseract binary

    Returns:
        str: Full text content from all pages
    """
    from pypdf import PdfReader

    text_parts = []
    reader = PdfReader(str(pdf_path))

    for page_num, page in enumerate(reader.pages):
        # Try to extract text directly
        page_text = page.extract_text()

        # If very little text extracted and OCR enabled, try OCR
        if use_ocr and len(page_text.strip()) < 50:
            try:
                from pdf2image import convert_from_path
                import pytesseract

                # Set tesseract path
                pytesseract.pytesseract.tesseract_cmd = tesseract_path

                # Convert this page to image
                images = convert_from_path(
                    str(pdf_path),
                    first_page=page_num + 1,
                    last_page=page_num + 1
                )

                if images:
                    # Run OCR on image
                    ocr_text = pytesseract.image_to_string(images[0])
                    if len(ocr_text) > len(page_text):
                        page_text = ocr_text

            except (ImportError, Exception):
                # If OCR fails, use what we have
                pass

        text_parts.append(page_text)

    return '\n\n'.join(text_parts)


def extract_text_with_pages(pdf_path: Path, use_ocr: bool = True,
                            tesseract_path: str = '/opt/homebrew/bin/tesseract') -> dict[int, str]:
    """Extract text with page number mapping.

    Args:
        pdf_path: Path to PDF
        use_ocr: Whether to use OCR for scanned pages
        tesseract_path: Path to Tesseract binary

    Returns:
        dict: {page_num: text_content} (1-indexed page numbers)
    """
    from pypdf import PdfReader

    pages_dict = {}
    reader = PdfReader(str(pdf_path))

    for page_num, page in enumerate(reader.pages, start=1):
        # Try to extract text directly
        page_text = page.extract_text()

        # If very little text extracted and OCR enabled, try OCR
        if use_ocr and len(page_text.strip()) < 50:
            try:
                from pdf2image import convert_from_path
                import pytesseract

                # Set tesseract path
                pytesseract.pytesseract.tesseract_cmd = tesseract_path

                # Convert this page to image
                images = convert_from_path(
                    str(pdf_path),
                    first_page=page_num,
                    last_page=page_num
                )

                if images:
                    # Run OCR on image
                    ocr_text = pytesseract.image_to_string(images[0])
                    if len(ocr_text) > len(page_text):
                        page_text = ocr_text

            except (ImportError, Exception):
                # If OCR fails, use what we have
                pass

        pages_dict[page_num] = page_text

    return pages_dict


def extract_tables(pdf_path: Path) -> list[dict]:
    """Extract tables from PDF.

    Args:
        pdf_path: Path to PDF

    Returns:
        list: [
            {
                'page': page_num,
                'table_data': pandas_dataframe,
                'bbox': (x, y, width, height)
            }
        ]
    """
    tables = []

    try:
        import tabula

        # Extract all tables from PDF
        dfs = tabula.read_pdf(
            str(pdf_path),
            pages='all',
            multiple_tables=True,
            lattice=True,  # Better for tables with lines
            stream=True     # Better for tables without lines
        )

        for i, df in enumerate(dfs):
            tables.append({
                'page': 1,  # tabula doesn't always provide page numbers reliably
                'table_data': df,
                'bbox': None  # Would need camelot for bbox
            })

    except (ImportError, Exception):
        # If tabula not available or fails, try camelot
        try:
            import camelot

            table_list = camelot.read_pdf(str(pdf_path), pages='all')

            for table in table_list:
                tables.append({
                    'page': table.page,
                    'table_data': table.df,
                    'bbox': table._bbox if hasattr(table, '_bbox') else None
                })

        except (ImportError, Exception):
            # No table extraction available
            pass

    return tables


def extract_images(pdf_path: Path, output_dir: Optional[Path] = None) -> list[dict]:
    """Extract images from PDF.

    Args:
        pdf_path: Path to PDF
        output_dir: Directory to save extracted images (optional)

    Returns:
        list: [
            {
                'page': page_num,
                'image_path': saved_image_path,
                'bbox': (x, y, width, height)
            }
        ]
    """
    from pypdf import PdfReader
    import io

    if output_dir is None:
        output_dir = Path('/tmp/pdf_images')

    output_dir.mkdir(exist_ok=True, parents=True)

    images = []
    reader = PdfReader(str(pdf_path))

    for page_num, page in enumerate(reader.pages, start=1):
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()

            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    try:
                        # Extract image data
                        data = xObject[obj].get_data()

                        # Determine image format
                        if '/Filter' in xObject[obj]:
                            filter_type = xObject[obj]['/Filter']
                            if filter_type == '/DCTDecode':
                                ext = '.jpg'
                            elif filter_type == '/FlateDecode':
                                ext = '.png'
                            else:
                                ext = '.png'
                        else:
                            ext = '.png'

                        # Save image
                        image_path = output_dir / f'page{page_num}_{obj[1:]}{ext}'
                        with open(image_path, 'wb') as img_file:
                            img_file.write(data)

                        images.append({
                            'page': page_num,
                            'image_path': str(image_path),
                            'bbox': None  # Would need more complex extraction for bbox
                        })

                    except Exception:
                        # Skip images that can't be extracted
                        continue

    return images


def prepare_document_for_llm(pdf_path: Path,
                             include_tables: bool = False,
                             include_images: bool = False,
                             use_ocr: bool = True,
                             tesseract_path: str = '/opt/homebrew/bin/tesseract') -> dict:
    """Prepare document content for LLM analysis.

    Args:
        pdf_path: Path to PDF
        include_tables: Whether to extract tables
        include_images: Whether to extract images
        use_ocr: Whether to use OCR for text extraction
        tesseract_path: Path to Tesseract binary

    Returns:
        dict: {
            'text': full_text,
            'pages': {page_num: text},
            'tables': [...] (if requested),
            'images': [...] (if requested)
        }
    """
    result = {}

    # Extract full text
    result['text'] = extract_full_text(pdf_path, use_ocr, tesseract_path)

    # Extract text with page mapping
    result['pages'] = extract_text_with_pages(pdf_path, use_ocr, tesseract_path)

    # Extract tables if requested
    if include_tables:
        result['tables'] = extract_tables(pdf_path)
    else:
        result['tables'] = []

    # Extract images if requested
    if include_images:
        result['images'] = extract_images(pdf_path)
    else:
        result['images'] = []

    return result


# =============================================================================
# Character-Level Text Extraction for Zotero Positioned Annotations
# =============================================================================

def extract_page_chars(pdf_path: Path | str, page_index: int) -> list[dict]:
    """
    Extract character-level text data from a PDF page for Zotero annotations.

    Zotero's annotation positioning algorithm requires character-level data
    to calculate the 'offset' component of annotationSortIndex. This function
    uses PyMuPDF to extract characters with their bounding boxes and converts
    them to Zotero's expected format.

    Args:
        pdf_path: Path to the PDF file
        page_index: Zero-based page index

    Returns:
        List of character dictionaries in Zotero format:
        [{'c': 'A', 'rect': [x1, y1, x2, y2], 'rotation': 0}, ...]

    Raises:
        FileNotFoundError: If PDF does not exist
        IndexError: If page_index is out of range

    Example:
        >>> chars = extract_page_chars('document.pdf', 0)
        >>> len(chars)
        1167
        >>> chars[0]
        {'c': 'P', 'rect': [42.0, 46.2, 47.87, 57.55], 'rotation': 0}
    """
    import fitz  # PyMuPDF

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(str(pdf_path))

    try:
        if page_index < 0 or page_index >= len(doc):
            raise IndexError(f"Page index {page_index} out of range (PDF has {len(doc)} pages)")

        page = doc[page_index]
        chars = _extract_chars_from_page(page)
        return chars
    finally:
        doc.close()


def _extract_chars_from_page(page) -> list[dict]:
    """
    Extract and convert character data from a PyMuPDF page.

    Args:
        page: PyMuPDF page object (fitz.Page)

    Returns:
        List of characters in Zotero format
    """
    chars = []
    text_dict = page.get_text("rawdict")

    for block in text_dict.get('blocks', []):
        if block.get('type') == 0:  # Text block (type 0), not image block (type 1)
            for line in block.get('lines', []):
                # Get rotation from line direction vector
                line_rotation = _calculate_rotation_from_dir(line.get('dir', (1.0, 0.0)))

                for span in line.get('spans', []):
                    for char_data in span.get('chars', []):
                        char = _convert_char_to_zotero_format(char_data, span, line_rotation)
                        chars.append(char)

    return chars


def _calculate_rotation_from_dir(dir_vector: tuple[float, float]) -> int:
    """
    Calculate text rotation in degrees from PyMuPDF line direction vector.

    PyMuPDF line['dir'] is a direction vector (x, y):
    - (1.0, 0.0)  = horizontal left-to-right = 0°
    - (0.0, 1.0)  = vertical bottom-to-top   = 90°
    - (-1.0, 0.0) = horizontal right-to-left = 180°
    - (0.0, -1.0) = vertical top-to-bottom   = 270°

    Args:
        dir_vector: Direction vector (x, y) from PyMuPDF

    Returns:
        int: Rotation in degrees (0, 90, 180, or 270)
    """
    import math

    x, y = dir_vector

    # Calculate angle in degrees from direction vector
    # atan2(y, x) gives angle in radians, convert to degrees
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)

    # Normalize to 0-360 range
    if angle_deg < 0:
        angle_deg += 360

    # Round to nearest 90 degrees
    # 0°, 90°, 180°, 270°
    rotation = round(angle_deg / 90) * 90

    # Normalize to 0-270 range
    if rotation == 360:
        rotation = 0

    return int(rotation)


def _convert_char_to_zotero_format(char_data: dict, span: dict, rotation: int = 0) -> dict:
    """
    Convert PyMuPDF character data to Zotero format.

    PyMuPDF format:
        char_data = {
            'c': 'A',
            'bbox': (x0, y0, x1, y1),  # Tuple
            'origin': (x, y),
            ...
        }
        span = {
            'font': 'TimesNewRoman',
            'size': 12.0,
            'flags': 0,
            ...
        }

    Zotero format:
        {
            'c': 'A',
            'rect': [x0, y0, x1, y1],  # List
            'rotation': 0
        }

    Args:
        char_data: Character data from PyMuPDF
        span: Parent span data (contains font info, etc.)
        rotation: Text rotation in degrees (0, 90, 180, 270) from line direction

    Returns:
        Character dictionary in Zotero format
    """
    # Convert bbox tuple to rect list
    bbox = char_data.get('bbox', (0, 0, 0, 0))
    rect = list(bbox)  # Convert tuple to list: (x0, y0, x1, y1) → [x0, y0, x1, y1]

    return {
        'c': char_data.get('c', ''),
        'rect': rect,
        'rotation': rotation
    }


def extract_pdf_pages_data(pdf_path: Path | str, page_indices: Optional[list[int]] = None) -> dict:
    """
    Extract character and viewBox data for multiple pages.

    This creates the pdfPages structure expected by Zotero's getSortIndex algorithm:
    pdfPages = [
        {
            'chars': [...],
            'viewBox': [x1, y1, x2, y2]
        },
        ...
    ]

    Args:
        pdf_path: Path to the PDF file
        page_indices: List of page indices to extract (None = all pages)

    Returns:
        Dictionary mapping page index to page data:
        {
            0: {'chars': [...], 'viewBox': [0, 0, 612, 792]},
            1: {'chars': [...], 'viewBox': [0, 0, 612, 792]},
            ...
        }

    Example:
        >>> pdf_pages = extract_pdf_pages_data('document.pdf', [0, 1])
        >>> len(pdf_pages)
        2
        >>> pdf_pages[0].keys()
        dict_keys(['chars', 'viewBox'])
    """
    import fitz  # PyMuPDF

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(str(pdf_path))

    try:
        if page_indices is None:
            page_indices = list(range(len(doc)))

        pdf_pages = {}

        for page_idx in page_indices:
            if page_idx < 0 or page_idx >= len(doc):
                continue

            page = doc[page_idx]
            chars = _extract_chars_from_page(page)

            # Get viewBox from page rect
            # PyMuPDF rect is (x0, y0, x1, y1) where origin is bottom-left
            # This matches PDF coordinate system used by Zotero
            rect = page.rect
            view_box = [rect.x0, rect.y0, rect.x1, rect.y1]

            pdf_pages[page_idx] = {
                'chars': chars,
                'viewBox': view_box
            }

        return pdf_pages
    finally:
        doc.close()
