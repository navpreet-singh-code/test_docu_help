import json
import re
from app.services.grok_service import chat_with_grok

def clean_text(text):
    # Extract text if it's in a dictionary structure
    if isinstance(text, list) and text and isinstance(text[0], dict):
        text = text[0].get('text', '')
    
    # Clean special artifacts
    text = re.sub(r'\(cid:\d+\)', '', text)  # Remove CID markers
    text = text.replace(':etaD', 'Date:')     # Fix reversed text
    text = re.sub(r'\s+', ' ', text)         # Normalize whitespace 
    return text.strip()

def load_grok_field_rules():
    with open("server/app/grok_field_rules.json", "r") as f:
        return json.load(f)

async def extract_fields_with_grok(text: str, fields: list[str]) -> dict:
    """
    Uses Grok to extract specific fields from the text and returns them as a JSON object.
    """
    rules = load_grok_field_rules()
    
    rules_prompt = "\n".join(
        f"- {field}: Look for keywords like '{', '.join(rules[field]['keywords'])}'. The value should match the pattern: {rules[field]['pattern']}"
        for field in fields if field in rules
    )

    prompt = f"""
    Analyze the following text and extract the specified fields based on the rules provided.
    Return the result as a JSON object with the field names as keys.
    If a field is not found, its value should be null.

    Text:
    ---
    {text}
    ---

    Fields to extract and their rules:
    {rules_prompt}

    Respond ONLY with a JSON object.
    """
    try:
        response_content = chat_with_grok(prompt)
        if response_content:
            # The response should be a JSON string, so we can parse it directly
            return json.loads(response_content)
        else:
            return {"error": "Failed to get a response from Grok API."}
    except json.JSONDecodeError:
        # If JSON parsing fails, return all null values for requested fields
        return {field: None for field in fields}
    except Exception as e:
        # Handle potential API errors
        return {"error": f"An error occurred with the Grok API: {str(e)}"}

async def identify_document_type_with_grok(text: str) -> str:
    """
    Uses Grok to identify the document type from the text.
    :param text: The text extracted from the document.
    :return: The identified document type as a string.
    """
    cleaned_text = clean_text(text)
    prompt = f"""
    Analyze the following text and identify the type of document.
    The document is related to travel. Examples include "Passport", "Visa", "Flight Ticket", "Hotel Booking", "Aadhaar Card" , "DRIVING LICENSE", etc.
    Return ONLY the document type as a single string. For example: "Passport".
    Do not include any additional text, explanations, or JSON formatting.

    Text:
    ---
    {cleaned_text}
    ---

    Document Type:
    """

    try:
        response_content = chat_with_grok(prompt)
        print('habai',response_content)
        if response_content:
            # The response should be a single string, so we can return it directly after stripping whitespace
            return response_content.strip()
        else:
            return "Unknown"
    except Exception as e:
        # Handle potential API errors
        return "Error in identification"
