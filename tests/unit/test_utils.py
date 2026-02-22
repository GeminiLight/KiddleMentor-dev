"""Unit tests for utilities."""

import json
import pytest

from gen_mentor.utils.llm_output import preprocess_response
from gen_mentor.utils.preprocess import clean_text, extract_json_from_text


class TestLLMOutput:
    """Tests for LLM output preprocessing."""

    def test_preprocess_response_text_only(self):
        """Test preprocessing response for text only."""
        raw_output = {
            "messages": [
                {"role": "assistant", "content": "Hello, how can I help?"}
            ]
        }

        result = preprocess_response(
            raw_output,
            only_text=True,
            exclude_think=True,
            json_output=False,
        )

        assert isinstance(result, str)
        assert "Hello" in result

    def test_preprocess_response_json_output(self):
        """Test preprocessing response with JSON parsing."""
        raw_output = {
            "messages": [
                {"role": "assistant", "content": '{"name": "Test", "value": 123}'}
            ]
        }

        result = preprocess_response(
            raw_output,
            only_text=True,
            exclude_think=True,
            json_output=True,
        )

        assert isinstance(result, dict)
        assert result["name"] == "Test"
        assert result["value"] == 123

    def test_preprocess_response_with_think_tags(self):
        """Test preprocessing with <think> tags."""
        raw_output = {
            "messages": [
                {
                    "role": "assistant",
                    "content": "<think>Internal reasoning</think>Final answer",
                }
            ]
        }

        result = preprocess_response(
            raw_output,
            only_text=True,
            exclude_think=True,
            json_output=False,
        )

        assert "Internal reasoning" not in result
        assert "Final answer" in result

    def test_preprocess_response_keep_think(self):
        """Test preprocessing keeping <think> tags."""
        raw_output = {
            "messages": [
                {
                    "role": "assistant",
                    "content": "<think>Internal reasoning</think>Final answer",
                }
            ]
        }

        result = preprocess_response(
            raw_output,
            only_text=True,
            exclude_think=False,
            json_output=False,
        )

        assert "Internal reasoning" in result


class TestPreprocess:
    """Tests for text preprocessing utilities."""

    def test_clean_text(self):
        """Test text cleaning."""
        text = "  Hello   World  \n\n  Test  "
        cleaned = clean_text(text)

        assert cleaned == "Hello World Test"

    def test_extract_json_from_text(self):
        """Test extracting JSON from text."""
        text = 'Some text {"key": "value", "number": 42} more text'

        result = extract_json_from_text(text)

        assert result is not None
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_extract_json_with_code_blocks(self):
        """Test extracting JSON from markdown code blocks."""
        text = '''
        Here is the JSON:
        ```json
        {"name": "Test", "items": [1, 2, 3]}
        ```
        '''

        result = extract_json_from_text(text)

        assert result is not None
        assert result["name"] == "Test"
        assert len(result["items"]) == 3

    def test_extract_json_invalid_returns_none(self):
        """Test that invalid JSON returns None."""
        text = "This is not JSON at all"

        result = extract_json_from_text(text)

        assert result is None
