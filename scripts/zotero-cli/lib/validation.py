"""Validation utilities for Zotero metadata."""

from typing import List, Dict


def validate_fields_for_item_type(item_type: str, updates: Dict) -> List[str]:
    """Validate that fields are appropriate for item type.

    Returns list of validation warnings (not errors - still allows update).

    Args:
        item_type: The Zotero item type (e.g., 'report', 'journalArticle')
        updates: Dictionary of field updates to validate

    Returns:
        List of warning messages for fields that may not apply to the item type
    """
    warnings = []

    # Define valid fields per item type
    valid_fields = {
        'report': ['institution', 'reportType', 'place', 'reportNumber', 'series'],
        'journalArticle': ['publicationTitle', 'volume', 'issue', 'pages'],
        'book': ['publisher', 'place', 'series', 'volume', 'numPages'],
        'conferencePaper': ['conferenceName', 'place', 'proceedingsTitle'],
    }

    report_only_fields = ['institution', 'reportType', 'reportNumber']

    if item_type in valid_fields:
        for field in updates.keys():
            if field in report_only_fields and item_type != 'report':
                warnings.append(f"'{field}' is typically used for reports, not {item_type}")

    return warnings
