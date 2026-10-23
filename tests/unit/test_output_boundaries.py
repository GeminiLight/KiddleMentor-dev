"""Response adapters accept real LangChain messages and serialized equivalents."""

import json

import pytest
from langchain_core.messages import AIMessage

from gen_mentor.utils.llm_output import convert_json_output, preprocess_response
from gen_mentor.utils.preprocess import clean_text, extract_json_from_text


@pytest.mark.parametrize("message", [AIMessage(content="Hello"), {"role": "assistant", "content": "Hello"}])
def test_serialized_and_native_messages_have_the_same_text(message):
    assert preprocess_response({"messages": [message]}) == "Hello"


def test_content_blocks_preserve_text_without_reasoning_or_image_data():
    message = AIMessage(
        content=[
            {"type": "text", "text": "First"},
            {"type": "image_url", "image_url": {"url": "https://example.org/image.png"}},
            {"type": "text", "text": "Second"},
        ]
    )
    assert preprocess_response({"messages": [message]}) == "FirstSecond"


@pytest.mark.parametrize("response", [{"messages": []}, {"choices": []}])
def test_empty_response_has_an_explicit_error(response):
    with pytest.raises(ValueError, match="empty"):
        preprocess_response(response)


def test_json_extraction_respects_string_braces_and_multiple_candidates():
    text = 'bad {not json} then {"nested": {"text": "brace }"}} trailing {noise}'
    assert extract_json_from_text(text) == {"nested": {"text": "brace }"}}
    assert convert_json_output(text) == {"nested": {"text": "brace }"}}


def test_json_array_output_remains_an_array():
    assert convert_json_output('```json\n[{"value": 1}]\n```') == [{"value": 1}]


def test_malformed_json_is_not_returned_as_a_successful_answer():
    assert extract_json_from_text('{"broken":') is None
    with pytest.raises(json.JSONDecodeError):
        convert_json_output('{"broken":')


@pytest.mark.parametrize("text, expected", [("", ""), (" \n\t ", ""), ("你好\t世界\n", "你好 世界")])
def test_clean_text_handles_empty_and_unicode_whitespace(text, expected):
    assert clean_text(text) == expected


@pytest.mark.parametrize(
    "response", [{"choices": [{"message": {"content": "Hello"}}]}, {"choices": [{"text": "Hello"}]}]
)
def test_openai_chat_and_completion_response_shapes(response):
    assert preprocess_response(response) == "Hello"


def test_raw_response_mode_preserves_the_original_object():
    response = {"messages": [AIMessage(content="Hello")]}
    assert preprocess_response(response, only_text=False) is response


@pytest.mark.parametrize("content", [None, 123, {"unexpected": "mapping"}])
def test_unsupported_message_content_is_rejected(content):
    with pytest.raises(TypeError, match="Response content"):
        preprocess_response({"messages": [{"content": content}]})
