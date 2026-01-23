import re
import json
from typing import Dict


def extract_json_from_markdown(md: str) -> Dict:
    """
    Extract JSON from markdown code blocks.
    
    Args:
        md: Markdown string potentially containing JSON in code blocks.
        
    Returns:
        Parsed JSON as dictionary.
        
    Raises:
        ValueError: If JSON cannot be parsed.
    """
    pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(pattern, md, re.MULTILINE)
    json_text = match.group(1) if match else md.strip()
    
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {e}")
