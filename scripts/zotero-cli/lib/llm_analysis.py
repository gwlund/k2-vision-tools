"""LLM integration for PDF analysis.

This module provides LLM provider implementations for analyzing PDF documents
and generating structured highlight suggestions.
"""

import os
import json
from typing import Protocol, Literal, Optional
from pathlib import Path
import yaml


class LLMProvider(Protocol):
    """Protocol for LLM providers."""

    def analyze_document(self, text: str, prompt: str) -> dict:
        """Analyze document and return structured results.

        Args:
            text: Document text to analyze
            prompt: Analysis prompt

        Returns:
            dict: {
                'highlights': [
                    {
                        'text': 'excerpt to highlight',
                        'page': page_number,
                        'reason': 'why this is relevant',
                        'type': 'text|table|image'
                    }
                ]
            }
        """
        ...


class ClaudeProvider:
    """Claude (Anthropic) LLM provider."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", max_tokens: int = 4096):
        """Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens

    def analyze_document(self, text: str, prompt: str) -> dict:
        """Send document to Claude for analysis.

        Args:
            text: Document text
            prompt: Analysis prompt

        Returns:
            dict: Structured analysis results with highlights
        """
        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=self.api_key)

            # Build full prompt with structured output request
            full_prompt = f"""{prompt}

Document text:
{text}

Please analyze the document and return a JSON object with this structure:
{{
    "highlights": [
        {{
            "text": "exact text excerpt to highlight (50-200 words)",
            "page": estimated_page_number,
            "reason": "brief explanation of why this is relevant",
            "type": "text"
        }}
    ]
}}

Return ONLY the JSON object, no additional commentary."""

            message = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text
            # Try to find JSON in response (Claude sometimes adds markdown)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            return json.loads(response_text)

        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")


class OpenAIProvider:
    """OpenAI GPT-4 provider."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", max_tokens: int = 4096):
        """Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens

    def analyze_document(self, text: str, prompt: str) -> dict:
        """Send document to OpenAI for analysis.

        Args:
            text: Document text
            prompt: Analysis prompt

        Returns:
            dict: Structured analysis results with highlights
        """
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            # Build full prompt with structured output request
            full_prompt = f"""{prompt}

Document text:
{text}

Please analyze the document and return a JSON object with this structure:
{{
    "highlights": [
        {{
            "text": "exact text excerpt to highlight (50-200 words)",
            "page": estimated_page_number,
            "reason": "brief explanation of why this is relevant",
            "type": "text"
        }}
    ]
}}

Return ONLY the JSON object, no additional commentary."""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a research assistant that analyzes documents and identifies key passages."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")


class OllamaProvider:
    """Local Ollama provider."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """Initialize Ollama provider.

        Args:
            base_url: Ollama server URL
            model: Model name to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model

    def analyze_document(self, text: str, prompt: str) -> dict:
        """Send document to Ollama for analysis.

        Args:
            text: Document text
            prompt: Analysis prompt

        Returns:
            dict: Structured analysis results with highlights
        """
        try:
            import requests

            # Build full prompt with structured output request
            full_prompt = f"""{prompt}

Document text:
{text}

Please analyze the document and return a JSON object with this structure:
{{
    "highlights": [
        {{
            "text": "exact text excerpt to highlight (50-200 words)",
            "page": estimated_page_number,
            "reason": "brief explanation of why this is relevant",
            "type": "text"
        }}
    ]
}}

Return ONLY the JSON object, no additional commentary."""

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=300  # 5 minute timeout for analysis
            )
            response.raise_for_status()

            result = response.json()
            return json.loads(result['response'])

        except Exception as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")


def load_llm_config() -> dict:
    """Load LLM configuration from config file or defaults.

    Returns:
        dict: LLM configuration
    """
    # Try multiple config locations
    config_paths = [
        Path.home() / '.zotero-cli' / 'config.yaml',
        Path('config.yaml'),
        Path(__file__).parent.parent / 'config.yaml',
    ]

    for config_path in config_paths:
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if 'llm' in config:
                    return config['llm']

    # Default configuration
    return {
        'default_provider': 'claude',
        'providers': {
            'claude': {
                'api_key_env': 'ANTHROPIC_API_KEY',
                'model': 'claude-3-5-sonnet-20241022',
                'max_tokens': 4096
            },
            'openai': {
                'api_key_env': 'OPENAI_API_KEY',
                'model': 'gpt-4-turbo-preview',
                'max_tokens': 4096
            },
            'ollama': {
                'base_url': 'http://localhost:11434',
                'model': 'llama2'
            }
        }
    }


def get_llm_provider(provider_name: Optional[Literal['claude', 'openai', 'ollama']] = None,
                     config: Optional[dict] = None) -> LLMProvider:
    """Factory function to get LLM provider instance.

    Args:
        provider_name: Provider to use (claude, openai, ollama)
        config: Optional configuration override

    Returns:
        LLMProvider: Configured provider instance

    Raises:
        ValueError: If provider not configured or API key missing
    """
    if config is None:
        config = load_llm_config()

    # Use default provider if not specified
    if provider_name is None:
        provider_name = config.get('default_provider', 'claude')

    provider_config = config['providers'].get(provider_name)
    if not provider_config:
        raise ValueError(f"Provider '{provider_name}' not configured")

    # Get provider instance
    if provider_name == 'claude':
        api_key_env = provider_config.get('api_key_env', 'ANTHROPIC_API_KEY')
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise ValueError(f"API key not found in environment variable: {api_key_env}")

        return ClaudeProvider(
            api_key=api_key,
            model=provider_config.get('model', 'claude-3-5-sonnet-20241022'),
            max_tokens=provider_config.get('max_tokens', 4096)
        )

    elif provider_name == 'openai':
        api_key_env = provider_config.get('api_key_env', 'OPENAI_API_KEY')
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise ValueError(f"API key not found in environment variable: {api_key_env}")

        return OpenAIProvider(
            api_key=api_key,
            model=provider_config.get('model', 'gpt-4-turbo-preview'),
            max_tokens=provider_config.get('max_tokens', 4096)
        )

    elif provider_name == 'ollama':
        return OllamaProvider(
            base_url=provider_config.get('base_url', 'http://localhost:11434'),
            model=provider_config.get('model', 'llama2')
        )

    else:
        raise ValueError(f"Unknown provider: {provider_name}")


def build_analysis_prompt(topics: Optional[list[str]] = None,
                          context: Optional[str] = None,
                          mode: Literal['quick', 'deep'] = 'quick') -> str:
    """Build analysis prompt for LLM.

    Args:
        topics: List of topics to focus on
        context: Research context for deep mode
        mode: Analysis depth (quick or deep)

    Returns:
        str: Formatted prompt for LLM
    """
    if mode == 'quick':
        if not topics:
            topics = ['key points', 'important data', 'strategies']

        topic_list = ', '.join(topics)
        return f"""Analyze this document and highlight key passages about: {topic_list}.

For each highlight:
1. Extract the exact text excerpt (50-200 words)
2. Estimate the page number where it appears
3. Explain briefly why this passage is relevant

Focus on:
- Quantitative data and statistics
- Strategic initiatives and plans
- Key findings and conclusions
- Unique approaches or insights"""

    else:  # deep mode
        if not context:
            context = "Comprehensive research analysis"

        topic_section = ""
        if topics:
            topic_bullets = '\n'.join([f"- {topic}" for topic in topics])
            topic_section = f"""

Specific topics to address:
{topic_bullets}"""

        return f"""Research context: {context}

Analyze this document in depth and identify passages that address the research goals.{topic_section}

For each highlight:
1. Extract the exact text excerpt (50-200 words)
2. Estimate the page number where it appears
3. Explain how it relates to the research context

Look for:
- Comparable data that can be used for analysis
- Strategies and approaches that can be learned from
- Methodologies and frameworks
- Connections to other topics or documents
- Data that supports or contradicts assumptions"""


def extract_highlights_from_response(llm_response: dict) -> list[dict]:
    """Parse LLM response into structured highlights.

    Args:
        llm_response: Response from LLM provider

    Returns:
        list: List of highlight dictionaries with standardized fields
    """
    highlights = llm_response.get('highlights', [])

    # Normalize highlight structure
    normalized = []
    for h in highlights:
        normalized.append({
            'text': h.get('text', ''),
            'page': h.get('page', 1),
            'reason': h.get('reason', ''),
            'type': h.get('type', 'text')
        })

    return normalized
