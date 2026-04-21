"""
PDF.js Text Extraction via Node.js

Extracts text with coordinates using PDF.js (the same library Zotero uses)
to ensure coordinate compatibility with Zotero's PDF renderer.
"""

import json
import subprocess
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class TextItem:
    """A single text element from PDF."""
    text: str
    x: float
    y: float
    width: float
    height: float
    font_name: str = ''


@dataclass
class SearchResult:
    """Result of text search."""
    page_index: int
    text: str
    rects: List[List[float]]  # [[x1, y1, x2, y2], ...]


class PDFJSExtractor:
    """Extract text using PDF.js via Node.js subprocess."""

    def __init__(self, node_scripts_dir: Optional[Path] = None):
        """Initialize extractor.

        Args:
            node_scripts_dir: Path to node_scripts directory.
                            If None, uses default location.

        Raises:
            RuntimeError: If Node.js is not installed or dependencies missing
        """
        self.node_scripts_dir = node_scripts_dir or (
            Path(__file__).parent.parent / 'node_scripts'
        )

        self._check_node_installed()
        self._check_dependencies_installed()

    def extract_text(
        self,
        pdf_path: Path,
        page_index: Optional[int] = None
    ) -> List[TextItem]:
        """Extract all text items from PDF page(s).

        Args:
            pdf_path: Path to PDF file
            page_index: Specific page to extract (None = all pages)

        Returns:
            List of TextItem objects with coordinates

        Raises:
            RuntimeError: If extraction fails
        """
        script_path = self.node_scripts_dir / 'extract_text.js'

        cmd = ['node', str(script_path), str(pdf_path)]
        if page_index is not None:
            cmd.append(str(page_index))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )

            data = json.loads(result.stdout)
            items = []

            for page in data['pages']:
                for item_data in page['items']:
                    items.append(TextItem(
                        text=item_data['text'],
                        x=item_data['x'],
                        y=item_data['y'],
                        width=item_data['width'],
                        height=item_data['height'],
                        font_name=item_data.get('font_name', '')
                    ))

            return items

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PDF.js extraction failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse PDF.js output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("PDF.js extraction timed out after 30 seconds")

    def search_text(
        self,
        pdf_path: Path,
        search_text: str,
        page_index: Optional[int] = None
    ) -> List[SearchResult]:
        """Search for text and get bounding rectangles.

        Args:
            pdf_path: Path to PDF file
            search_text: Text to search for
            page_index: Specific page to search (None = all pages)

        Returns:
            List of SearchResult objects with rects

        Raises:
            RuntimeError: If search fails
        """
        script_path = self.node_scripts_dir / 'search_text.js'

        cmd = ['node', str(script_path), str(pdf_path), search_text]
        if page_index is not None:
            cmd.append(str(page_index))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )

            data = json.loads(result.stdout)
            results = []

            for result_data in data['results']:
                results.append(SearchResult(
                    page_index=result_data['page_index'],
                    text=result_data['text'],
                    rects=result_data['rects']
                ))

            return results

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PDF.js search failed: {e.stderr}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse PDF.js output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("PDF.js search timed out after 30 seconds")

    def _check_node_installed(self) -> None:
        """Verify Node.js is installed.

        Raises:
            RuntimeError: If Node.js is not found
        """
        if not shutil.which('node'):
            raise RuntimeError(
                "Node.js is required for PDF.js integration.\n"
                "Install from: https://nodejs.org/\n"
                "Or on macOS: brew install node"
            )

    def _check_dependencies_installed(self) -> None:
        """Verify npm packages are installed.

        Raises:
            RuntimeError: If node_modules not found
        """
        node_modules = self.node_scripts_dir / 'node_modules'
        if not node_modules.exists():
            raise RuntimeError(
                "PDF.js dependencies not installed.\n"
                f"Run: cd {self.node_scripts_dir} && npm install"
            )


# Convenience function for quick searching
def search_and_get_rects_pdfjs(
    pdf_path: Path,
    search_text: str,
    page_index: Optional[int] = None
) -> List[dict]:
    """Search for text using PDF.js and return results in PyMuPDF-compatible format.

    Args:
        pdf_path: Path to PDF file
        search_text: Text to search for
        page_index: Optional specific page to search

    Returns:
        list: [
            {
                'page_index': int,
                'rects': [[x1, y1, x2, y2], ...],
                'text': str
            },
            ...
        ]
    """
    extractor = PDFJSExtractor()
    results = extractor.search_text(pdf_path, search_text, page_index)

    return [
        {
            'page_index': r.page_index,
            'rects': r.rects,
            'text': r.text
        }
        for r in results
    ]
