"""Zotero item templates for common item types."""

from typing import Dict, Any, List

def journal_article_template(
    title: str,
    authors: List[Dict[str, str]],
    year: str,
    publication: str = '',
    volume: str = '',
    issue: str = '',
    pages: str = '',
    doi: str = '',
    url: str = '',
    abstract: str = '',
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create journal article item template."""

    item = {
        'itemType': 'journalArticle',
        'title': title,
        'creators': authors,
        'date': year,
        'publicationTitle': publication,
        'volume': volume,
        'issue': issue,
        'pages': pages,
        'DOI': doi,
        'url': url,
        'abstractNote': abstract,
        'tags': [{'tag': tag} for tag in (tags or [])]
    }

    # Remove empty fields
    return {k: v for k, v in item.items() if v}

def book_template(
    title: str,
    authors: List[Dict[str, str]],
    year: str,
    publisher: str = '',
    place: str = '',
    isbn: str = '',
    pages: str = '',
    url: str = '',
    abstract: str = '',
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create book item template."""

    item = {
        'itemType': 'book',
        'title': title,
        'creators': authors,
        'date': year,
        'publisher': publisher,
        'place': place,
        'ISBN': isbn,
        'numPages': pages,
        'url': url,
        'abstractNote': abstract,
        'tags': [{'tag': tag} for tag in (tags or [])]
    }

    return {k: v for k, v in item.items() if v}

def webpage_template(
    title: str,
    url: str,
    authors: List[Dict[str, str]] = None,
    date: str = '',
    website_title: str = '',
    abstract: str = '',
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create webpage item template."""

    item = {
        'itemType': 'webpage',
        'title': title,
        'url': url,
        'creators': authors or [],
        'date': date,
        'websiteTitle': website_title,
        'abstractNote': abstract,
        'tags': [{'tag': tag} for tag in (tags or [])]
    }

    return {k: v for k, v in item.items() if v}

def report_template(
    title: str,
    authors: List[Dict[str, str]],
    year: str,
    institution: str = '',
    report_number: str = '',
    place: str = '',
    url: str = '',
    abstract: str = '',
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create report item template."""

    item = {
        'itemType': 'report',
        'title': title,
        'creators': authors,
        'date': year,
        'institution': institution,
        'reportNumber': report_number,
        'place': place,
        'url': url,
        'abstractNote': abstract,
        'tags': [{'tag': tag} for tag in (tags or [])]
    }

    return {k: v for k, v in item.items() if v}

def conference_paper_template(
    title: str,
    authors: List[Dict[str, str]],
    year: str,
    conference_name: str = '',
    place: str = '',
    proceedings_title: str = '',
    doi: str = '',
    url: str = '',
    abstract: str = '',
    tags: List[str] = None
) -> Dict[str, Any]:
    """Create conference paper item template."""

    item = {
        'itemType': 'conferencePaper',
        'title': title,
        'creators': authors,
        'date': year,
        'conferenceName': conference_name,
        'place': place,
        'proceedingsTitle': proceedings_title,
        'DOI': doi,
        'url': url,
        'abstractNote': abstract,
        'tags': [{'tag': tag} for tag in (tags or [])]
    }

    return {k: v for k, v in item.items() if v}
