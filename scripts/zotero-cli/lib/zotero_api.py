"""Shared Zotero API wrapper for all CLI scripts."""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from pyzotero import zotero
from rich.console import Console

# Import positioning module for visible annotations
try:
    from pdf_positioning import create_positioned_highlight, create_positioned_note
    POSITIONED_ANNOTATIONS_AVAILABLE = True
except ImportError:
    POSITIONED_ANNOTATIONS_AVAILABLE = False

console = Console()

class ZoteroAPI:
    """Wrapper around pyzotero with error handling and convenience methods."""

    def __init__(self):
        """Initialize API client from environment variables."""
        self.api_key = os.getenv('ZOTERO_API_KEY')
        self.user_id = os.getenv('ZOTERO_USER_ID')

        if not self.api_key or not self.user_id:
            raise ValueError(
                "Missing Zotero credentials. Set ZOTERO_API_KEY and "
                "ZOTERO_USER_ID in environment."
            )

        self.zot = zotero.Zotero(self.user_id, 'user', self.api_key)

    def get_collection_key(self, collection_name: str) -> Optional[str]:
        """Get collection key by name. Returns None if not found."""
        collections = self.zot.collections()
        for coll in collections:
            if coll['data']['name'] == collection_name:
                return coll['data']['key']
        return None

    def collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists."""
        return self.get_collection_key(collection_name) is not None

    def create_collection(self, name: str, parent_key: Optional[str] = None) -> str:
        """Create collection and return its key."""
        collection_data = {
            'name': name,
            'parentCollection': parent_key if parent_key else False
        }

        result = self.zot.create_collections([collection_data])

        # pyzotero returns dict with 'successful' key containing created items
        if result and 'successful' in result and '0' in result['successful']:
            return result['successful']['0']['key']

        raise ValueError(f"Failed to create collection: {result}")

    def add_item(self, item_data: Dict[str, Any], collection_key: Optional[str] = None) -> str:
        """Add item to library and optionally to a collection. Returns item key."""

        # Create item
        result = self.zot.create_items([item_data])

        if not result or 'successful' not in result or '0' not in result['successful']:
            raise ValueError(f"Failed to create item: {result}")

        item_key = result['successful']['0']['key']

        # Add to collection if specified
        if collection_key:
            self.zot.addto_collection(collection_key, result['successful']['0'])

        return item_key

    def add_tags_to_item(self, item_key: str, tags: List[str]) -> bool:
        """Add tags to existing item. Preserves existing tags."""

        # Get current item
        item = self.zot.item(item_key)

        # Get existing tags
        existing_tags = [tag['tag'] for tag in item['data'].get('tags', [])]

        # Merge with new tags (deduplicate)
        all_tags = list(set(existing_tags + tags))

        # Update item
        item['data']['tags'] = [{'tag': tag} for tag in all_tags]

        result = self.zot.update_item(item)
        return bool(result)

    def update_item(self, item_key: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields of an item. Preserves other fields."""

        # Get current item
        item = self.zot.item(item_key)

        # Update specified fields
        for field, value in updates.items():
            item['data'][field] = value

        result = self.zot.update_item(item)
        return bool(result)

    def search_items(self, query: str, limit: int = 20, collection_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search library for items matching query.

        Args:
            query: Search query string
            limit: Maximum results to return
            collection_key: Optional collection key to search within

        Returns:
            List of item dictionaries
        """
        if collection_key:
            return self.zot.collection_items(collection_key, q=query, limit=limit)
        else:
            return self.zot.top(q=query, limit=limit)

    def get_all_items(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all top-level items (not in trash)."""
        return self.zot.top(limit=limit)

    def get_collection_items(self, collection_key: str) -> List[Dict[str, Any]]:
        """Get all items in a specific collection."""
        return self.zot.collection_items(collection_key)

    def get_item(self, item_key: str) -> Dict[str, Any]:
        """Get item by key."""
        return self.zot.item(item_key)

    def get_all_collections(self) -> List[Dict[str, Any]]:
        """Get all collections with their metadata."""
        return self.zot.collections()

    def get_collection_tree(self) -> Dict[str, Any]:
        """Get collections organized as tree structure."""
        collections = self.zot.collections()

        # Build tree structure
        tree = {'top_level': [], 'children': {}}

        for coll in collections:
            data = coll['data']
            key = data['key']
            parent = data.get('parentCollection')

            coll_info = {
                'key': key,
                'name': data['name'],
                'parent': parent,
                'num_items': data.get('meta', {}).get('numItems', 0)
            }

            if not parent:
                tree['top_level'].append(coll_info)
            else:
                if parent not in tree['children']:
                    tree['children'][parent] = []
                tree['children'][parent].append(coll_info)

        return tree

    def _normalize_tags(self, tags_response) -> List[Dict[str, Any]]:
        """Convert tags response to consistent dict format."""
        if not tags_response:
            return []
        # Check if we got simple strings or dicts
        if isinstance(tags_response[0], str):
            return [{'tag': t, 'meta': {}} for t in tags_response]
        return tags_response

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """Get all tags from library with usage counts."""
        return self._normalize_tags(self.zot.tags())

    def get_collection_tags(self, collection_key: str) -> List[Dict[str, Any]]:
        """Get all tags used in a specific collection."""
        return self._normalize_tags(self.zot.collection_tags(collection_key))

    def get_item_tags(self, item_key: str) -> List[str]:
        """Get tags for a specific item."""
        item = self.zot.item(item_key)
        return [tag['tag'] for tag in item['data'].get('tags', [])]

    # Better BibTeX Integration
    BBT_ENDPOINT = "http://127.0.0.1:23119/better-bibtex/json-rpc"

    def check_better_bibtex_available(self) -> bool:
        """Check if Better BibTeX is available via JSON-RPC API.

        Returns:
            True if Better BibTeX is available, False otherwise
        """
        try:
            import requests
            response = requests.post(
                self.BBT_ENDPOINT,
                json={
                    "jsonrpc": "2.0",
                    "method": "user.groups",
                    "params": [],
                    "id": 1
                },
                timeout=2
            )
            return response.status_code == 200
        except Exception:
            return False

    def _parse_citation_key_from_extra(self, extra: str) -> Optional[str]:
        """Parse citation key from Zotero extra field.

        Looks for patterns:
        - Citation Key: <key>
        - bibtex: <key>
        - tex.citationkey: <key>

        Args:
            extra: The extra field content

        Returns:
            Citation key if found, None otherwise
        """
        if not extra:
            return None

        import re
        patterns = [
            r'Citation Key:\s*(\S+)',
            r'bibtex:\s*(\S+)',
            r'tex\.citationkey:\s*(\S+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, extra, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def get_citation_key(self, item_key: str) -> Optional[str]:
        """Get Better BibTeX citation key for an item.

        Tries Better BibTeX API first, falls back to parsing extra field.

        Args:
            item_key: Zotero item key

        Returns:
            Citation key if found, None otherwise
        """
        # Try Better BibTeX API first
        if self.check_better_bibtex_available():
            try:
                import requests
                response = requests.post(
                    self.BBT_ENDPOINT,
                    json={
                        "jsonrpc": "2.0",
                        "method": "item.citationkey",
                        "params": [[item_key]],
                        "id": 1
                    },
                    timeout=5
                )

                if response.status_code == 200:
                    result = response.json().get('result', {})
                    return result.get(item_key)
            except Exception:
                pass

        # Fallback: parse from extra field
        try:
            item = self.get_item(item_key)
            extra = item.get('data', {}).get('extra', '')
            return self._parse_citation_key_from_extra(extra)
        except Exception:
            return None

    def get_citation_keys(self, item_keys: List[str]) -> Dict[str, str]:
        """Get Better BibTeX citation keys for multiple items.

        Args:
            item_keys: List of Zotero item keys

        Returns:
            Dictionary mapping item keys to citation keys
        """
        result = {}

        # Try Better BibTeX API for batch request
        if self.check_better_bibtex_available():
            try:
                import requests
                response = requests.post(
                    self.BBT_ENDPOINT,
                    json={
                        "jsonrpc": "2.0",
                        "method": "item.citationkey",
                        "params": [item_keys],
                        "id": 1
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    return response.json().get('result', {})
            except Exception:
                pass

        # Fallback: get citation keys individually
        for item_key in item_keys:
            citekey = self.get_citation_key(item_key)
            if citekey:
                result[item_key] = citekey

        return result

    # Collection Path and Recursive Operations

    def get_collection_by_path(self, path: str) -> Optional[str]:
        """Get collection key by hierarchical path.

        Args:
            path: Collection path like "Research/Papers/Climate"

        Returns:
            Collection key if found, None otherwise
        """
        parts = path.split('/')
        collections = self.get_all_collections()

        # Build name -> key mapping for each parent
        name_to_keys: Dict[Optional[str], Dict[str, str]] = {}
        for coll in collections:
            data = coll['data']
            parent = data.get('parentCollection') or None
            name = data['name']
            key = data['key']

            if parent not in name_to_keys:
                name_to_keys[parent] = {}
            name_to_keys[parent][name] = key

        # Traverse path
        current_parent = None
        for part in parts:
            if current_parent not in name_to_keys:
                return None
            if part not in name_to_keys[current_parent]:
                return None
            current_parent = name_to_keys[current_parent][part]

        return current_parent

    def get_all_subcollection_keys(self, collection_key: str) -> List[str]:
        """Get all subcollection keys recursively.

        Args:
            collection_key: Starting collection key

        Returns:
            List of all collection keys including the starting collection
        """
        tree = self.get_collection_tree()
        result = [collection_key]

        def collect_children(parent_key: str):
            if parent_key in tree['children']:
                for child in tree['children'][parent_key]:
                    result.append(child['key'])
                    collect_children(child['key'])

        collect_children(collection_key)
        return result

    def search_items_recursive(self, query: str, collection_key: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search items recursively through collection and all subcollections.

        Args:
            query: Search query string
            collection_key: Starting collection key
            limit: Maximum results to return

        Returns:
            List of unique item dictionaries matching query
        """
        # Get all subcollection keys including parent
        collection_keys = self.get_all_subcollection_keys(collection_key)

        # Collect items from all collections
        seen_keys = set()
        results = []

        for coll_key in collection_keys:
            items = self.zot.collection_items(coll_key, q=query, limit=limit)

            for item in items:
                item_key = item['data']['key']
                if item_key not in seen_keys:
                    seen_keys.add(item_key)
                    results.append(item)

                    if len(results) >= limit:
                        return results

        return results

    def rename_collection(self, collection_key: str, new_name: str) -> bool:
        """Rename a collection.

        Args:
            collection_key: Collection key to rename
            new_name: New name for the collection

        Returns:
            True if successful
        """
        collection = self.zot.collection(collection_key)
        collection['data']['name'] = new_name
        result = self.zot.update_collection(collection)
        return bool(result)

    def move_collection(self, collection_key: str, new_parent_key: Optional[str]) -> bool:
        """Move collection to a different parent.

        Args:
            collection_key: Collection key to move
            new_parent_key: New parent collection key (None for top level)

        Returns:
            True if successful
        """
        collection = self.zot.collection(collection_key)
        collection['data']['parentCollection'] = new_parent_key if new_parent_key else False
        result = self.zot.update_collection(collection)
        return bool(result)

    def delete_collection(self, collection_key: str) -> bool:
        """Delete a collection.

        Note: Zotero API will delete all subcollections recursively.
        Items in the collection are NOT deleted, only removed from collection.

        Args:
            collection_key: Collection key to delete

        Returns:
            True if successful
        """
        collection = self.zot.collection(collection_key)
        result = self.zot.delete_collection(collection)
        return bool(result)

    # DOI Search and Duplicate Detection

    def _normalize_doi(self, doi: str) -> str:
        """Normalize DOI to consistent format.

        Strips common prefixes and whitespace.

        Args:
            doi: Raw DOI string

        Returns:
            Normalized DOI (just the identifier part)
        """
        doi = doi.strip()
        # Remove common prefixes
        prefixes = ['https://doi.org/', 'http://doi.org/', 'doi:', 'DOI:']
        for prefix in prefixes:
            if doi.lower().startswith(prefix.lower()):
                doi = doi[len(prefix):]
        return doi.strip()

    def find_item_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """Find item by DOI across multiple fields.

        Search strategy:
        1. Search DOI field (most reliable)
        2. Search URL field for doi.org/{doi}
        3. Search Extra field for DOI patterns

        Args:
            doi: DOI to search for (e.g., "10.1234/example")

        Returns:
            Item dict if found, None otherwise
        """
        doi = self._normalize_doi(doi)

        # 1. Search DOI field (most reliable)
        items = self.zot.items(q=f'DOI:{doi}')
        if items:
            return items[0]

        # 2. Search for DOI in URL field
        url_pattern = f"doi.org/{doi}"
        items = self.zot.items(q=url_pattern)
        for item in items:
            url = item['data'].get('url', '')
            if url_pattern in url.lower():
                return item

        # 3. Search Extra field for DOI patterns
        items = self.zot.items(q=doi)
        for item in items:
            extra = item['data'].get('extra', '')
            # Check for DOI patterns in extra field
            if doi in extra:
                return item

        return None

    def find_duplicates_by_doi(self) -> Dict[str, List[Dict[str, Any]]]:
        """Find all items with duplicate DOIs.

        Returns:
            Dictionary mapping DOI -> list of items with that DOI
            Only includes DOIs that appear more than once
        """
        from collections import defaultdict

        # Get all items
        all_items = self.zot.everything(self.zot.items())

        # Group by DOI
        doi_map = defaultdict(list)

        for item in all_items:
            # Skip non-regular items (notes, attachments)
            if item['data'].get('itemType') in ['note', 'attachment']:
                continue

            # Get DOI from various fields
            doi = None

            # Check DOI field
            if 'DOI' in item['data'] and item['data']['DOI']:
                doi = self._normalize_doi(item['data']['DOI'])
            # Check URL field
            elif 'url' in item['data'] and 'doi.org/' in item['data']['url'].lower():
                url = item['data']['url']
                doi = url.split('doi.org/')[-1].strip('/')
                doi = self._normalize_doi(doi)
            # Check Extra field
            elif 'extra' in item['data']:
                extra = item['data']['extra']
                import re
                match = re.search(r'DOI:\s*(\S+)', extra, re.IGNORECASE)
                if match:
                    doi = self._normalize_doi(match.group(1))

            if doi:
                doi_map[doi].append(item)

        # Return only DOIs with duplicates
        return {doi: items for doi, items in doi_map.items() if len(items) > 1}

    def find_item_by_title(self, title: str, item_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Find item by exact title match.

        Args:
            title: Exact title to search for
            item_type: Optional item type to filter by (e.g., 'journalArticle', 'book')

        Returns:
            Item dict if found, None otherwise
        """
        # Search for title
        items = self.zot.items(q=title, limit=50)

        for item in items:
            item_data = item['data']

            # Skip non-regular items (notes, attachments)
            if item_data.get('itemType') in ['note', 'attachment']:
                continue

            # Check for exact title match (case-insensitive)
            if item_data.get('title', '').lower() == title.lower():
                # If item_type specified, check that it matches
                if item_type and item_data.get('itemType') != item_type:
                    continue
                return item

        return None

    def delete_item(self, item_key: str) -> bool:
        """Delete an item from library.

        Args:
            item_key: Item key to delete

        Returns:
            True if successful
        """
        item = self.zot.item(item_key)
        result = self.zot.delete_item(item)
        return bool(result)

    def merge_items(self, primary_key: str, secondary_key: str,
                   preserve_citation_key: Optional[str] = None) -> bool:
        """Merge two items, keeping primary and deleting secondary.

        Merges collections, tags, notes, and attachments from secondary into primary.

        Args:
            primary_key: Item to keep
            secondary_key: Item to delete after merging
            preserve_citation_key: Optional citation key to preserve in Extra field

        Returns:
            True if successful
        """
        # Get both items
        primary = self.zot.item(primary_key)
        secondary = self.zot.item(secondary_key)

        # Merge tags
        primary_tags = set(t['tag'] for t in primary['data'].get('tags', []))
        secondary_tags = set(t['tag'] for t in secondary['data'].get('tags', []))
        all_tags = primary_tags | secondary_tags

        primary['data']['tags'] = [{'tag': tag} for tag in sorted(all_tags)]

        # Preserve citation key in extra if specified
        if preserve_citation_key:
            extra = primary['data'].get('extra', '')
            if preserve_citation_key not in extra:
                if extra:
                    extra += f"\nAlternate Citation Key: {preserve_citation_key}"
                else:
                    extra = f"Alternate Citation Key: {preserve_citation_key}"
                primary['data']['extra'] = extra

        # Update primary item
        self.zot.update_item(primary)

        # Get collections from both items
        all_collections = self.get_all_collections()
        secondary_collections = []

        for coll in all_collections:
            coll_items = self.get_collection_items(coll['data']['key'])
            if secondary_key in [item['data']['key'] for item in coll_items]:
                secondary_collections.append(coll['data']['key'])

        # Add primary to secondary's collections
        for coll_key in secondary_collections:
            self.zot.addto_collection(coll_key, primary)

        # Delete secondary item
        self.delete_item(secondary_key)

        return True

    def calculate_item_score(self, item: dict) -> int:
        """Calculate score for item quality (for auto-merge decisions).

        Higher score = better item to keep as primary.

        Args:
            item: Item dictionary

        Returns:
            Quality score (higher is better)
        """
        score = 0
        data = item['data']

        # Has citation key (check via get_citation_key)
        if self.get_citation_key(data['key']):
            score += 100

        # Number of tags
        score += len(data.get('tags', [])) * 5

        # Has abstract
        if data.get('abstractNote'):
            score += 20

        # Number of fields filled
        filled_fields = sum(1 for v in data.values() if v)
        score += filled_fields

        # Has attachments/notes (would need children check - placeholder)
        # score += count_children * 10

        return score

    # Library Metadata Suggestions (for PDF upload)

    def suggest_creators(self, partial: str, limit: int = 5) -> List[str]:
        """Suggest existing creators from library matching partial string.

        Args:
            partial: Partial creator name
            limit: Maximum suggestions to return

        Returns:
            list: Existing creator names sorted by frequency
        """
        if not partial:
            return []

        # Get all items
        items = self.zot.everything(self.zot.items())

        # Extract all creators
        creator_counts = {}
        for item in items:
            data = item.get('data', {})
            creators = data.get('creators', [])

            for creator in creators:
                # Handle different creator formats
                if 'name' in creator:
                    # Institution/organization
                    name = creator['name']
                else:
                    # Person
                    first = creator.get('firstName', '')
                    last = creator.get('lastName', '')
                    name = f"{first} {last}".strip()

                if not name:
                    continue

                # Case-insensitive partial matching
                if partial.lower() in name.lower():
                    creator_counts[name] = creator_counts.get(name, 0) + 1

        # Sort by frequency, then alphabetically
        sorted_creators = sorted(
            creator_counts.items(),
            key=lambda x: (-x[1], x[0])
        )

        return [name for name, count in sorted_creators[:limit]]

    def suggest_publishers(self, partial: str, limit: int = 5) -> List[str]:
        """Suggest existing publishers from library matching partial string.

        Args:
            partial: Partial publisher name
            limit: Maximum suggestions to return

        Returns:
            list: Existing publisher names sorted by frequency
        """
        return self._suggest_field_values('publisher', partial, limit)

    def suggest_places(self, partial: str, limit: int = 5) -> List[str]:
        """Suggest existing places from library matching partial string.

        Args:
            partial: Partial place name
            limit: Maximum suggestions to return

        Returns:
            list: Existing place names sorted by frequency
        """
        return self._suggest_field_values('place', partial, limit)

    def suggest_tags(self, partial: str, limit: int = 5) -> List[str]:
        """Suggest existing tags from library matching partial string.

        Args:
            partial: Partial tag name
            limit: Maximum suggestions to return

        Returns:
            list: Existing tag names sorted by frequency
        """
        if not partial:
            return []

        # Get all tags from library
        all_tags = self.zot.tags()

        # Filter by partial match
        matching_tags = {}
        for tag_obj in all_tags:
            tag = tag_obj.get('tag', '')
            if partial.lower() in tag.lower():
                # Note: Zotero API doesn't provide tag counts easily
                # Just return alphabetically for now
                matching_tags[tag] = 1

        # Sort alphabetically
        sorted_tags = sorted(matching_tags.keys())

        return sorted_tags[:limit]

    def _suggest_field_values(self, field_name: str, partial: str, limit: int) -> List[str]:
        """Generic helper for suggesting field values.

        Args:
            field_name: Zotero field name
            partial: Partial string to match
            limit: Maximum results

        Returns:
            list: Matching values sorted by frequency
        """
        if not partial:
            return []

        # Get all items
        items = self.zot.everything(self.zot.items())

        # Count occurrences
        value_counts = {}
        for item in items:
            data = item.get('data', {})
            value = data.get(field_name, '')

            if not value:
                continue

            # Case-insensitive partial matching
            if partial.lower() in value.lower():
                value_counts[value] = value_counts.get(value, 0) + 1

        # Sort by frequency, then alphabetically
        sorted_values = sorted(
            value_counts.items(),
            key=lambda x: (-x[1], x[0])
        )

        return [value for value, count in sorted_values[:limit]]

    def get_metadata_field_values(self, field_name: str) -> Dict[str, int]:
        """Get all unique values for a metadata field with frequency counts.

        Args:
            field_name: Zotero field name (e.g., 'publisher', 'place')

        Returns:
            dict: {value: count} sorted by count descending
        """
        # Get all items
        items = self.zot.everything(self.zot.items())

        # Count occurrences
        value_counts = {}
        for item in items:
            data = item.get('data', {})
            value = data.get(field_name, '')

            if value:
                value_counts[value] = value_counts.get(value, 0) + 1

        # Sort by frequency
        return dict(sorted(value_counts.items(), key=lambda x: -x[1]))

    # PDF Attachment Support

    def add_item_with_attachment(self, item_data: dict, pdf_path: Path,
                                 collection_key: str = None) -> str:
        """Create Zotero item and attach PDF file.

        Args:
            item_data: Zotero item metadata
            pdf_path: Path to PDF file
            collection_key: Optional collection to add to

        Returns:
            str: Item key of created item
        """
        # Create parent item
        result = self.zot.create_items([item_data])

        if not result or 'successful' not in result or not result['successful']:
            raise ValueError("Failed to create item")

        item_key = result['successful']['0']['key']

        # Upload PDF as attachment
        if pdf_path and pdf_path.exists():
            self.zot.attachment_simple([str(pdf_path)], item_key)

        # Add to collection if specified
        if collection_key:
            self.zot.addto_collection(collection_key, result['successful']['0'])

        return item_key

    def update_item_metadata(self, item_key: str, metadata: dict):
        """Update metadata fields for existing item.

        Preserves existing tags, collections, attachments.
        Only updates specified metadata fields.

        Args:
            item_key: Item key to update
            metadata: Fields to update
        """
        # Get current item
        item = self.zot.item(item_key)

        # Update data fields
        for key, value in metadata.items():
            item['data'][key] = value

        # Update version is required for Zotero API
        self.zot.update_item(item)

    #
    # Annotation methods (Phase B)
    #

    def create_highlight(self, item_key: str, highlight_data: dict) -> str:
        """Create highlight annotation in Zotero PDF.

        IMPORTANT: Creates metadata-only annotation without visual position data.
        The annotation will:
        - ✅ Export to markdown/JSON with all metadata
        - ✅ Appear in annotation search results
        - ✅ Include in generated notes
        - ❌ NOT appear as visual highlight in Zotero's PDF reader

        For visual highlights in PDF viewer, create manually in Zotero.
        See ANNOTATION_LIMITATIONS.md for details.

        Args:
            item_key: Item key of PDF parent item or PDF attachment
            highlight_data: {
                'text': 'text to highlight',
                'page': page_number,
                'color': '#ffd400' (hex color),
                'comment': 'annotation comment',
                'tags': ['tag1', 'tag2']
            }

        Returns:
            str: Annotation key

        Example:
            >>> api = ZoteroAPI()
            >>> api.create_highlight('ABC123', {
            ...     'text': 'Important finding about tourism',
            ...     'page': 15,
            ...     'comment': 'Key economic indicator',
            ...     'color': '#ffd400'
            ... })
            'XYZ789'
        """
        # Build annotation item
        annotation = {
            'itemType': 'annotation',
            'parentItem': item_key,
            'annotationType': 'highlight',
            'annotationText': highlight_data.get('text', ''),
            'annotationComment': highlight_data.get('comment', ''),
            'annotationPageLabel': str(highlight_data.get('page', 1)),
            'annotationColor': highlight_data.get('color', '#ffd400'),  # yellow default
            'annotationSortIndex': '00000|000000|00000',  # Required field to prevent sync errors
        }

        # Add tags if provided
        if 'tags' in highlight_data and highlight_data['tags']:
            annotation['tags'] = [{'tag': t} for t in highlight_data['tags']]

        # Create annotation
        result = self.zot.create_items([annotation])

        if result['successful']:
            return result['successful']['0']['key']
        else:
            raise RuntimeError(f"Failed to create highlight: {result.get('failed', {})}")

    def create_note_annotation(self, item_key: str, note_data: dict) -> str:
        """Create note annotation in Zotero PDF.

        Args:
            item_key: Item key of PDF parent item
            note_data: {
                'text': 'note text',
                'page': page_number,
                'comment': 'note comment',
                'tags': ['tag1', 'tag2']
            }

        Returns:
            str: Annotation key
        """
        # Build annotation item
        annotation = {
            'itemType': 'annotation',
            'parentItem': item_key,
            'annotationType': 'note',
            'annotationText': note_data.get('text', ''),
            'annotationComment': note_data.get('comment', ''),
            'annotationPageLabel': str(note_data.get('page', 1)),
            'annotationSortIndex': '00000|000000|00000',  # Required field to prevent sync errors
        }

        # Add tags if provided
        if 'tags' in note_data and note_data['tags']:
            annotation['tags'] = [{'tag': t} for t in note_data['tags']]

        # Create annotation
        result = self.zot.create_items([annotation])

        if result['successful']:
            return result['successful']['0']['key']
        else:
            raise RuntimeError(f"Failed to create note: {result.get('failed', {})}")

    def get_pdf_annotations(self, item_key: str, tag_filter: str = None) -> list[dict]:
        """Get all annotations for a PDF item.

        Args:
            item_key: Item key of PDF parent item or PDF attachment
            tag_filter: Optional tag to filter annotations

        Returns:
            list: [
                {
                    'key': annotation_key,
                    'type': 'highlight|note|image',
                    'text': highlighted_text,
                    'comment': user_comment,
                    'tags': [tag_objects],
                    'page': page_number
                }
            ]
        """
        # Get all children (including annotations and attachments)
        children = self.zot.children(item_key)

        annotations = []

        # First, check if direct children are annotations (item_key is PDF attachment)
        # OR if children include PDF attachments (item_key is parent item)
        for child in children:
            if child['data'].get('itemType') == 'annotation':
                # Direct annotation child
                annotation = {
                    'key': child['key'],
                    'type': child['data'].get('annotationType', 'unknown'),
                    'text': child['data'].get('annotationText', ''),
                    'comment': child['data'].get('annotationComment', ''),
                    'tags': child['data'].get('tags', []),
                    'page': child['data'].get('annotationPageLabel', '1')
                }

                # Filter by tag if specified
                if tag_filter:
                    tag_names = [t['tag'] for t in annotation['tags']]
                    if tag_filter in tag_names:
                        annotations.append(annotation)
                else:
                    annotations.append(annotation)

            elif child['data'].get('contentType') == 'application/pdf':
                # PDF attachment - check its children for annotations
                pdf_children = self.zot.children(child['key'])
                for pdf_child in pdf_children:
                    if pdf_child['data'].get('itemType') == 'annotation':
                        annotation = {
                            'key': pdf_child['key'],
                            'type': pdf_child['data'].get('annotationType', 'unknown'),
                            'text': pdf_child['data'].get('annotationText', ''),
                            'comment': pdf_child['data'].get('annotationComment', ''),
                            'tags': pdf_child['data'].get('tags', []),
                            'page': pdf_child['data'].get('annotationPageLabel', '1')
                        }

                        # Filter by tag if specified
                        if tag_filter:
                            tag_names = [t['tag'] for t in annotation['tags']]
                            if tag_filter in tag_names:
                                annotations.append(annotation)
                        else:
                            annotations.append(annotation)

        return annotations

    def update_annotation_tags(self, annotation_key: str, tags: list[str]):
        """Add or update tags on an annotation.

        Args:
            annotation_key: Annotation item key
            tags: List of tag names to set
        """
        # Get annotation
        annotation = self.zot.item(annotation_key)

        # Update tags
        annotation['data']['tags'] = [{'tag': t} for t in tags]

        # Update in Zotero
        self.zot.update_item(annotation)

    #
    # Positioned annotation methods (Phase C - visible annotations)
    #

    def create_positioned_highlight(
        self,
        item_key: str,
        pdf_path: Path | str,
        page_index: int,
        rects: list[list[float]],
        text: str = '',
        color: str = '#ffd400',
        comment: str = '',
        tags: Optional[list[str]] = None
    ) -> str:
        """Create positioned highlight annotation visible in Zotero PDF reader.

        This creates a FULL annotation with annotationSortIndex and annotationPosition
        fields, making it visible in Zotero's PDF reader, desktop app, and web interface.

        Comparison with create_highlight():
        - create_highlight(): Metadata-only, invisible in PDF reader
        - create_positioned_highlight(): Full annotation, visible everywhere

        Args:
            item_key: Item key of PDF parent item or PDF attachment
            pdf_path: Path to PDF file (needed to extract character data)
            page_index: Zero-based page index (page 1 = index 0)
            rects: Bounding rectangles [[x1, y1, x2, y2], ...]
                   PDF coordinates: origin at bottom-left, y-axis points up
            text: Text being highlighted
            color: Hex color code (default: yellow #ffd400)
            comment: Annotation comment/note
            tags: Optional list of tag strings

        Returns:
            str: Annotation key

        Raises:
            ImportError: If pdf_positioning module not available
            ValueError: If PDF cannot be read or page not found

        Example:
            >>> api = ZoteroAPI()
            >>> api.create_positioned_highlight(
            ...     item_key='ABC123',
            ...     pdf_path=Path('document.pdf'),
            ...     page_index=0,
            ...     rects=[[100, 200, 300, 210]],
            ...     text='Important finding',
            ...     comment='Key result'
            ... )
            'XYZ789'
        """
        if not POSITIONED_ANNOTATIONS_AVAILABLE:
            raise ImportError(
                "pdf_positioning module not available. "
                "Cannot create positioned annotations."
            )

        # Generate positioning data
        positioning_data = create_positioned_highlight(
            pdf_path=pdf_path,
            page_index=page_index,
            rects=rects,
            text=text,
            color=color,
            comment=comment,
            tags=tags
        )

        # Build annotation item with positioning fields
        annotation = {
            'itemType': 'annotation',
            'parentItem': item_key,
            'annotationType': 'highlight',
            'annotationText': positioning_data['text'],
            'annotationComment': positioning_data['comment'],
            'annotationPageLabel': positioning_data['pageLabel'],
            'annotationColor': positioning_data['color'],
            'annotationSortIndex': positioning_data['sortIndex'],  # NEW: enables visibility
            'annotationPosition': positioning_data['position'],     # NEW: enables visibility
        }

        # Add tags if provided
        if positioning_data['tags']:
            annotation['tags'] = [{'tag': t} for t in positioning_data['tags']]

        # Create annotation
        result = self.zot.create_items([annotation])

        if result['successful']:
            return result['successful']['0']['key']
        else:
            raise RuntimeError(f"Failed to create positioned highlight: {result.get('failed', {})}")

    def create_positioned_note(
        self,
        item_key: str,
        pdf_path: Path | str,
        page_index: int,
        rects: list[list[float]],
        comment: str = '',
        tags: Optional[list[str]] = None
    ) -> str:
        """Create positioned note annotation visible in Zotero PDF reader.

        Args:
            item_key: Item key of PDF parent item or PDF attachment
            pdf_path: Path to PDF file
            page_index: Zero-based page index
            rects: Bounding rectangles [[x1, y1, x2, y2], ...]
            comment: Note text
            tags: Optional list of tag strings

        Returns:
            str: Annotation key

        Raises:
            ImportError: If pdf_positioning module not available
            ValueError: If PDF cannot be read or page not found
        """
        if not POSITIONED_ANNOTATIONS_AVAILABLE:
            raise ImportError(
                "pdf_positioning module not available. "
                "Cannot create positioned annotations."
            )

        # Generate positioning data
        positioning_data = create_positioned_note(
            pdf_path=pdf_path,
            page_index=page_index,
            rects=rects,
            comment=comment,
            tags=tags
        )

        # Build annotation item with positioning fields
        annotation = {
            'itemType': 'annotation',
            'parentItem': item_key,
            'annotationType': 'note',
            # Note: 'annotationText' is NOT included for note annotations
            'annotationComment': positioning_data['comment'],
            'annotationPageLabel': positioning_data['pageLabel'],
            'annotationSortIndex': positioning_data['sortIndex'],
            'annotationPosition': positioning_data['position'],
        }

        # Add tags if provided
        if positioning_data['tags']:
            annotation['tags'] = [{'tag': t} for t in positioning_data['tags']]

        # Create annotation
        result = self.zot.create_items([annotation])

        if result['successful']:
            return result['successful']['0']['key']
        else:
            raise RuntimeError(f"Failed to create positioned note: {result.get('failed', {})}")

    def create_note_from_annotations(self, item_key: str,
                                     tag_filter: str = None) -> str:
        """Create Zotero note from annotations.

        Mimics Zotero's "Create Note from Annotations" feature.

        Args:
            item_key: PDF item key
            tag_filter: Only include annotations with this tag

        Returns:
            str: Note item key
        """
        # Get annotations
        annotations = self.get_pdf_annotations(item_key, tag_filter)

        if not annotations:
            raise ValueError(f"No annotations found for item {item_key}")

        # Get item metadata for note title
        item = self.zot.item(item_key)
        title = item['data'].get('title', 'Untitled')

        # Build note content (HTML format for Zotero)
        note_content = f"<h1>{title}</h1>\n"
        note_content += f"<p><em>Annotations ({len(annotations)})</em></p>\n"

        for ann in annotations:
            note_content += f"<p><strong>Page {ann['page']}</strong></p>\n"

            if ann['text']:
                note_content += f"<blockquote>{ann['text']}</blockquote>\n"

            if ann['comment']:
                note_content += f"<p>{ann['comment']}</p>\n"

            if ann['tags']:
                tag_str = ', '.join([t['tag'] for t in ann['tags']])
                note_content += f"<p><em>Tags: {tag_str}</em></p>\n"

            note_content += "<hr/>\n"

        # Create note item
        note = {
            'itemType': 'note',
            'parentItem': item_key,
            'note': note_content
        }

        result = self.zot.create_items([note])

        if result['successful']:
            return result['successful']['0']['key']
        else:
            raise RuntimeError(f"Failed to create note: {result.get('failed', {})}")

    def get_standalone_attachments(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all standalone PDF attachments (attachments without parent items).

        Standalone attachments are PDFs that were added directly to the library
        without being attached to a bibliographic entry.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of standalone attachment items

        Example:
            >>> api = ZoteroAPI()
            >>> standalone = api.get_standalone_attachments()
            >>> for item in standalone:
            ...     print(f"{item['key']}: {item['data']['title']}")
        """
        all_items = self.zot.top(limit=limit)

        standalone = []
        for item in all_items:
            data = item.get('data', {})

            # Must be an attachment
            if data.get('itemType') != 'attachment':
                continue

            # Must be PDF
            if data.get('contentType') != 'application/pdf':
                continue

            # Must not have a parent
            if 'parentItem' in data:
                continue

            standalone.append(item)

        return standalone

    def create_parent_item(self, attachment_key: str, metadata: Dict[str, Any]) -> str:
        """Create parent bibliographic item and link PDF as child attachment.

        This converts a standalone PDF attachment into a properly structured
        bibliographic entry with the PDF as a child attachment.

        Args:
            attachment_key: Key of standalone PDF attachment
            metadata: Bibliographic metadata for parent item

        Returns:
            Key of created parent item

        Raises:
            ValueError: If attachment doesn't exist or already has parent

        Example:
            >>> api = ZoteroAPI()
            >>> metadata = {
            ...     'itemType': 'report',
            ...     'title': 'Climate Report 2024',
            ...     'creators': [{'creatorType': 'author', 'name': 'IPCC'}],
            ...     'date': '2024'
            ... }
            >>> parent_key = api.create_parent_item('ABC123', metadata)
        """
        # Verify attachment exists and is standalone
        attachment = self.zot.item(attachment_key)
        if attachment['data'].get('itemType') != 'attachment':
            raise ValueError(f"Item {attachment_key} is not an attachment")
        if 'parentItem' in attachment['data']:
            raise ValueError(f"Attachment {attachment_key} already has a parent")

        # Create parent item
        result = self.zot.create_items([metadata])

        if not result.get('successful'):
            raise Exception("Failed to create parent item")

        parent_key = result['successful']['0']['key']

        # Link PDF to parent
        attachment['data']['parentItem'] = parent_key
        self.zot.update_item(attachment)

        return parent_key
