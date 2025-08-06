import json
import re
from pydantic import ValidationError
from typing import Tuple, Optional
from pydantic import BaseModel
from typing import Type, List, Optional
from typing import TypeVar

T = TypeVar("T", bound=BaseModel)


def clean_json_string(raw_text: str) -> str:
    """
    Removes markdown code block markers (e.g., ```json ... ```) and trims the text.
    """
    raw_text = raw_text.strip()
    if raw_text.startswith("```json") or raw_text.startswith("```"):
        raw_text = raw_text.strip("` \n")
        raw_text = re.sub(r"^json", "", raw_text, flags=re.IGNORECASE).strip()
    return raw_text


def parse_json_with_schema(raw_text: str, schema_class: Type[T]) -> Tuple[Optional[T], Optional[str]]:
    """
    Cleans and validates a raw JSON-like text using the provided Pydantic schema.

    Parameters:
        raw_text (str): The raw text from LLM.
        schema_class (type): A Pydantic BaseModel subclass (e.g., SyntheticTrend)

    Returns:
        (validated_object, error_message): Tuple where only one of the values is not None.
    """
    try:
        # Step 1: Remove Markdown formatting
        cleaned = clean_json_string(raw_text)

        # Step 2: Remove control characters
        cleaned = re.sub(r'[\x00-\x1F\x7F]', '', cleaned)

        # Step 3: Ensure it's valid JSON (optional, gives better error)
        json.loads(cleaned)

        # Step 4: Validate with the provided schema
        parsed = schema_class.model_validate_json(cleaned)
        return parsed, None

    except (json.JSONDecodeError, ValidationError) as e:
        return None, str(e)


def extract_key_value_pairs(raw_text: str) -> dict:
    """
    Parses outputs like:
    Goal: ...\nEmotion: ...\nText: ...
    Returns a dictionary
    """
    import re
    pattern = r'(\\w+):\s*(.*?)\s*(?=\\w+:|$)'
    matches = re.findall(pattern, raw_text, re.DOTALL)
    return {k.lower(): v.strip() for k, v in matches}


def normalize_output(data: dict, fields_to_listify: List[str]) -> dict:
    for key in fields_to_listify:
        if key in data and not isinstance(data[key], list):
            data[key] = [data[key]]
    return data
