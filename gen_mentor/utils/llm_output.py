import re
import json
from typing import Any


def extract_json_from_text(text: str):
    """Return the first valid JSON object or array embedded in model output."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\[{]", text):
        try:
            value, _ = decoder.raw_decode(text, match.start())
        except json.JSONDecodeError:
            continue
        return value
    return None


def convert_json_output(output: str) -> Any:
    """
    Convert raw JSON output from the LLM into structured format.

    Args:
        output: The JSON output from the LLM

    Returns:
        Structured JSON output
    """
    output = output.strip()
    if output.startswith("```json"):
        output = output[7:].strip()
    if output.endswith("```"):
        output = output[:-3].strip()
    if output.endswith("```json"):
        output = output[:-7].strip()
    try:
        # Attempt to parse the output as JSON
        return json.loads(output)
    except json.JSONDecodeError:
        # If parsing fails, try to extract JSON from the output string
        extracted = extract_json_from_text(output)
        if extracted is not None:
            return extracted
        raise json.JSONDecodeError("No valid JSON found in response", output, 0)


def get_text_from_response(response):
    """Extract text from the response object."""
    if "messages" in response:
        messages = response["messages"]
        if not messages:
            raise ValueError("Response messages are empty")
        message = messages[-1]
        content = message["content"] if isinstance(message, dict) else message.content
    else:
        choices = response.get("choices", [])
        if not choices:
            raise ValueError("Response choices are empty")
        choice = choices[0]
        content = choice["message"]["content"] if "message" in choice else choice["text"]
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block if isinstance(block, str) else block.get("text", "")
            for block in content
            if isinstance(block, str) or isinstance(block, dict) and block.get("type") == "text"
        )
    raise TypeError("Response content must be text or a list of content blocks")


def extract_think_and_result(info):
    "Extract think and result content from the response info." ""
    think_match = re.search(r"<think>(.*?)</think>", info, re.DOTALL)
    think_content = think_match.group(1).strip() if think_match else ""
    result_content = re.sub(r"<think>.*?</think>", "", info, flags=re.DOTALL).strip()
    return think_content, result_content


def preprocess_response(response, only_text=True, exclude_think=False, json_output=False):
    if only_text or exclude_think or json_output:
        response = get_text_from_response(response)
    if exclude_think:
        think_content, result_content = extract_think_and_result(response)
        response = result_content
    if json_output:
        try:
            response = convert_json_output(response)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")
            response = {"error": "Invalid JSON output", "raw_content": response}
            raise e
    return response
