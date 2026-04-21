"""Interactive metadata entry with smart suggestions.

This module provides functions for prompting users to enter metadata
with context-aware defaults and suggestions from existing library data.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()


def prompt_with_suggestions(field_name: str,
                           suggestions: List[str],
                           default: Optional[str] = None,
                           required: bool = False) -> str:
    """Prompt user with numbered suggestions or free-form input.

    Behavior:
    - If default and high confidence: "Creator: Land of Sky [Y/n]?"
    - If multiple suggestions: Show numbered list [1] [2] [3] [New...]
    - If no suggestions: Free-form input

    Args:
        field_name: Display name for field
        suggestions: List of suggested values
        default: Default value (if confidence high)
        required: Whether field is required

    Returns:
        str: User's choice or new value
    """
    # High confidence default (exact match from extraction)
    if default and not suggestions:
        if Confirm.ask(f"{field_name}: {default}", default=True):
            return default
        else:
            return Prompt.ask(f"Enter {field_name}", default="")

    # Multiple suggestions available
    if suggestions:
        console.print(f"\n[bold]{field_name}:[/bold]")

        # Show suggestions
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"  [{i}] {suggestion}")
        console.print(f"  [0] Enter new value")

        if default:
            console.print(f"\n  [dim]Extracted: {default}[/dim]")

        choice = Prompt.ask(
            "Choose",
            choices=[str(i) for i in range(len(suggestions) + 1)],
            default="1" if not default else "0"
        )

        if choice == "0":
            return Prompt.ask(f"Enter {field_name}", default=default or "")
        else:
            return suggestions[int(choice) - 1]

    # No suggestions - free-form
    prompt_text = f"{field_name}" + (" (required)" if required else "")
    value = Prompt.ask(prompt_text, default=default or "")

    while required and not value:
        console.print(f"[yellow]⚠[/yellow] {field_name} is required")
        value = Prompt.ask(prompt_text)

    return value


def prompt_metadata_interactive(extracted: Dict[str, str],
                                suggestions: Dict[str, List[str]],
                                template: Optional[Dict] = None) -> Dict[str, str]:
    """Interactive metadata entry with smart defaults.

    Args:
        extracted: Metadata from PDF extraction
        suggestions: Suggestions from library for each field
        template: Template defaults (if using --template)

    Returns:
        dict: Complete Zotero item metadata
    """
    metadata = {}

    # Use template defaults if available
    if template:
        metadata['itemType'] = template.get('itemType', 'report')
        if 'reportType' in template:
            metadata['reportType'] = template['reportType']

        required_fields = template.get('required_fields', [])
        optional_fields = template.get('optional_fields', [])
    else:
        required_fields = ['title', 'creator', 'date']
        optional_fields = ['place', 'publisher', 'url', 'abstractNote']

    # Prompt for required fields
    for field in required_fields:
        extracted_value = extracted.get(field)
        field_suggestions = suggestions.get(field, [])

        value = prompt_with_suggestions(
            field.capitalize(),
            field_suggestions,
            extracted_value,
            required=True
        )

        if value:
            # Handle creator field specially (needs to be object)
            if field == 'creator':
                metadata['creators'] = [{'creatorType': 'author', 'name': value}]
            else:
                metadata[field] = value

    # Prompt for optional fields
    console.print("\n[dim]Optional fields (press Enter to skip):[/dim]")

    for field in optional_fields:
        extracted_value = extracted.get(field)
        field_suggestions = suggestions.get(field, [])

        value = prompt_with_suggestions(
            field.capitalize(),
            field_suggestions,
            extracted_value,
            required=False
        )

        if value:
            metadata[field] = value

    # Add item type
    if 'itemType' not in metadata:
        metadata['itemType'] = 'report'

    return metadata


def load_template(template_name: str) -> Optional[Dict]:
    """Load metadata template.

    Templates stored in: lib/templates/{template_name}.yaml

    Args:
        template_name: Name of template (e.g., 'ceds')

    Returns:
        dict: Template configuration or None if not found
    """
    # Try multiple locations
    template_paths = [
        Path(__file__).parent / 'templates' / f'{template_name}.yaml',
        Path('lib/templates') / f'{template_name}.yaml',
        Path('templates') / f'{template_name}.yaml',
    ]

    for template_path in template_paths:
        if template_path.exists():
            with open(template_path, 'r') as f:
                return yaml.safe_load(f)

    console.print(f"[yellow]⚠[/yellow] Template '{template_name}' not found")
    return None


def show_template_info(template: Dict):
    """Display template information."""
    console.print(f"\n[bold cyan]Template: {template.get('name')}[/bold cyan]")
    console.print(f"Type: {template.get('itemType')}")

    if 'reportType' in template:
        console.print(f"Report Type: {template['reportType']}")

    if 'suggested_tags' in template:
        tags = ', '.join(template['suggested_tags'])
        console.print(f"Suggested tags: {tags}")

    if 'suggested_collections' in template:
        colls = ', '.join(template['suggested_collections'])
        console.print(f"Suggested collections: {colls}")

    console.print()
