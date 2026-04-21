"""Parsing utilities for Zotero scripts."""

from typing import List, Dict, Any

def parse_author_name(name: str) -> Dict[str, str]:
    """Parse author name into firstName and lastName.

    Handles formats:
    - "Last, First Middle"
    - "First Middle Last"
    - "Last, F. M."

    Returns dict with 'firstName' and 'lastName' keys.
    """
    name = name.strip()

    # Format: "Last, First Middle" or "Last, F. M."
    if ',' in name:
        parts = name.split(',', 1)
        last_name = parts[0].strip()
        first_name = parts[1].strip() if len(parts) > 1 else ''
        return {
            'creatorType': 'author',
            'lastName': last_name,
            'firstName': first_name
        }

    # Format: "First Middle Last"
    parts = name.split()
    if len(parts) == 1:
        # Single name (treat as last name)
        return {
            'creatorType': 'author',
            'lastName': parts[0],
            'firstName': ''
        }
    else:
        # Multiple parts: everything except last is first name
        return {
            'creatorType': 'author',
            'firstName': ' '.join(parts[:-1]),
            'lastName': parts[-1]
        }

def parse_author_list(authors_str: str) -> List[Dict[str, str]]:
    """Parse semicolon or comma-separated author list.

    Examples:
    - "Smith, John; Doe, Jane"
    - "John Smith; Jane Doe"
    - "Smith, J.; Doe, J."

    Returns list of author dicts suitable for Zotero.
    """
    # Split on semicolon or ' and '
    if ';' in authors_str:
        authors = [a.strip() for a in authors_str.split(';')]
    elif ' and ' in authors_str:
        authors = [a.strip() for a in authors_str.split(' and ')]
    else:
        # Single author
        authors = [authors_str.strip()]

    return [parse_author_name(author) for author in authors if author]

def parse_tags(tags_str: str) -> List[str]:
    """Parse comma-separated tag string.

    Examples:
    - "tag1, tag2, tag3"
    - "climate-change,whatcom-county"

    Returns list of tag strings.
    """
    if not tags_str:
        return []

    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]


def parse_creator_string(creator_str: str) -> Dict[str, str]:
    """Parse a single creator string into Zotero creator format.

    Handles:
    - "Lastname, Firstname" -> individual author
    - "Firstname Lastname" -> individual author
    - "Organization Name" (no comma) -> organizational author

    Args:
        creator_str: Creator string to parse

    Returns:
        Dictionary with creator fields for Zotero

    Examples:
        >>> parse_creator_string("Smith, John")
        {'creatorType': 'author', 'lastName': 'Smith', 'firstName': 'John'}

        >>> parse_creator_string("World Health Organization")
        {'creatorType': 'author', 'name': 'World Health Organization'}
    """
    creator_str = creator_str.strip()

    # Check for "Lastname, Firstname" format
    if ',' in creator_str:
        parts = [p.strip() for p in creator_str.split(',', 1)]
        return {
            'creatorType': 'author',
            'lastName': parts[0],
            'firstName': parts[1] if len(parts) > 1 else ''
        }

    # Check for "Firstname Lastname" (single word = organizational)
    words = creator_str.split()
    if len(words) == 1:
        # Single word = organizational
        return {
            'creatorType': 'author',
            'name': creator_str
        }
    elif len(words) >= 3 or any(word[0].isupper() and len(word) > 1 and not word[1].islower() for word in words):
        # Multiple capital words or acronyms = organizational
        return {
            'creatorType': 'author',
            'name': creator_str
        }
    else:
        # Assume "Firstname Lastname"
        return {
            'creatorType': 'author',
            'firstName': ' '.join(words[:-1]),
            'lastName': words[-1]
        }


def parse_creators(creators_str: str) -> List[Dict[str, str]]:
    """Parse semicolon-separated creator string into list of creators.

    Args:
        creators_str: Semicolon-separated creators

    Returns:
        List of creator dictionaries

    Example:
        >>> parse_creators("Smith, John; Doe, Jane; WHO")
        [{'creatorType': 'author', 'lastName': 'Smith', 'firstName': 'John'},
         {'creatorType': 'author', 'lastName': 'Doe', 'firstName': 'Jane'},
         {'creatorType': 'author', 'name': 'WHO'}]
    """
    creators = []
    for creator_str in creators_str.split(';'):
        creator_str = creator_str.strip()
        if creator_str:
            creators.append(parse_creator_string(creator_str))
    return creators
