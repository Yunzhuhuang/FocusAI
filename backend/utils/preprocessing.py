import re
from typing import List, Dict, Any
import string


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
        
    Returns:
        str: Cleaned text
    """
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Normalize quote characters
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Replace multiple periods with single ellipsis
    text = re.sub(r'\.{3,}', '...', text)
    
    # Clean up other characters
    text = text.replace('…', '...')
    
    return text


def remove_boilerplate(text: str) -> str:
    """
    Remove common boilerplate text like headers, footers, etc.
    
    Args:
        text: Text to process
        
    Returns:
        str: Text with boilerplate removed
    """
    # List of common boilerplate patterns to remove
    boilerplate_patterns = [
        r'Copyright © \d{4}.*?\n',
        r'All rights reserved\..*?\n',
        r'Terms and Conditions.*?\n',
        r'Privacy Policy.*?\n',
        r'Page \d+ of \d+',
        r'^\s*\d+\s*$',  # Page numbers on their own line
        r'https?://\S+',  # URLs
        r'www\.\S+',      # Web addresses
    ]
    
    # Apply all patterns
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text)
        
    return text


def extract_main_content(text: str) -> str:
    """
    Attempt to extract the main content from text by removing headers, footers, etc.
    
    Args:
        text: Text to process
        
    Returns:
        str: Main content
    """
    # Split into lines
    lines = text.split('\n')
    
    # Remove very short lines at the beginning (likely headers)
    while lines and len(lines[0].strip()) < 40:
        lines.pop(0)
        
    # Remove very short lines at the end (likely footers)
    while lines and len(lines[-1].strip()) < 40:
        lines.pop()
        
    # Join back into text
    return '\n'.join(lines)


def simplify_punctuation(text: str) -> str:
    """
    Simplify punctuation to make text more readable
    
    Args:
        text: Text to process
        
    Returns:
        str: Text with simplified punctuation
    """
    # Replace semicolons with periods
    text = text.replace(';', '.')
    
    # Replace multiple exclamation or question marks with a single one
    text = re.sub(r'!+', '!', text)
    text = re.sub(r'\?+', '?', text)
    
    # Add space after periods, exclamation marks, and question marks if missing
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
    
    return text


def format_lists(text: str) -> str:
    """
    Format lists with bullet points for better readability
    
    Args:
        text: Text to process
        
    Returns:
        str: Text with formatted lists
    """
    # Convert numbered lists (1. 2. 3. etc.) to bullet points
    text = re.sub(r'^\s*\d+\.\s+', '• ', text, flags=re.MULTILINE)
    
    # Convert asterisk lists to bullet points
    text = re.sub(r'^\s*\*\s+', '• ', text, flags=re.MULTILINE)
    
    # Convert dash lists to bullet points
    text = re.sub(r'^\s*-\s+', '• ', text, flags=re.MULTILINE)
    
    return text


def preprocess_text(text: str) -> str:
    """
    Apply all preprocessing steps to text
    
    Args:
        text: Text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Apply all preprocessing steps
    text = clean_text(text)
    text = remove_boilerplate(text)
    text = extract_main_content(text)
    text = simplify_punctuation(text)
    text = format_lists(text)
    
    return text
