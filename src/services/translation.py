import os
from pathlib import Path

import requests


OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
OPENROUTER_MODEL = 'deepseek/deepseek-v4-flash-0731'
REQUEST_TIMEOUT_SECONDS = 30
SUPPORTED_LANGUAGES = {
    'Chinese',
    'Japanese',
    'Spanish',
    'French',
    'German',
    'Korean',
}
PROMPT_PATH = Path(__file__).resolve().parents[2] / 'prompt' / 'translation.txt'


class TranslationConfigurationError(Exception):
    """Raised when local translation configuration is incomplete."""


class TranslationProviderError(Exception):
    """Raised when the translation provider cannot return a translation."""


def _load_translation_prompt():
    try:
        prompt = PROMPT_PATH.read_text(encoding='utf-8').strip()
    except OSError as error:
        raise TranslationConfigurationError from error

    if not prompt:
        raise TranslationConfigurationError
    return prompt


def translate_text(note_content, target_language):
    api_key = os.getenv('OPENROUTER_API_KEY', '').strip()
    if not api_key:
        raise TranslationConfigurationError

    prompt = _load_translation_prompt()
    payload = {
        'model': OPENROUTER_MODEL,
        'messages': [
            {'role': 'system', 'content': prompt},
            {
                'role': 'user',
                'content': (
                    f'Translate the following note into {target_language}. '
                    f'\n\n{note_content}'
                ),
            },
        ],
        'temperature': 0.2,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        response_data = response.json()
        translation = response_data['choices'][0]['message']['content'].strip()
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as error:
        raise TranslationProviderError from error

    if not translation:
        raise TranslationProviderError
    return translation