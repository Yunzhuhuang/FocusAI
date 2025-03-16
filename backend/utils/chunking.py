from typing import List, Optional
import re


def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into chunks of specified size with overlap
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Overlap between consecutive chunks in characters
        
    Returns:
        List[str]: List of text chunks
    """
    # Ensure chunk_size is greater than chunk_overlap
    if chunk_size <= chunk_overlap:
        chunk_size = chunk_overlap + 100
        
    # Handle empty or very short text
    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    current_chunk = text
    
    while len(current_chunk) > chunk_size:
        # Find a good breaking point
        break_point = find_break_point(current_chunk, chunk_size)
        
        # If we couldn't find a good break point, force a break at chunk_size
        if break_point == 0:
            break_point = chunk_size

        # Add the chunk up to the break point
        chunks.append(current_chunk[:break_point].strip())
        
        # Move to next chunk, starting from break_point
        current_chunk = current_chunk[break_point:].strip()
        
        # Safety check - if we're not making progress, break
        if not current_chunk:
            break
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Now add overlap to the chunks after they're all created
    if chunk_overlap > 0 and len(chunks) > 1:
        final_chunks = []
        for i in range(len(chunks)):
            if i < len(chunks) - 1:
                # Get start of next chunk as overlap
                next_chunk = chunks[i + 1]
                overlap = next_chunk[:chunk_overlap] if len(next_chunk) > chunk_overlap else next_chunk
                final_chunks.append(chunks[i] + " " + overlap)
            else:
                final_chunks.append(chunks[i])
        return final_chunks
    
    return chunks


def find_break_point(text: str, max_length: int) -> int:
    """
    Find a good point to break text, preferably at a sentence end
    
    Args:
        text: Text to break
        max_length: Maximum length to consider
        
    Returns:
        int: Index where the text should be broken
    """
    # Don't try to break beyond the text length
    if len(text) <= max_length:
        return len(text)
    
    # Try to find sentence endings within the allowed length
    sentence_endings = [match.end() for match in re.finditer(r'[.!?]\s+', text[:max_length])]
    
    if sentence_endings:
        # Return the last sentence ending found
        return sentence_endings[-1]
    
    # If no sentence endings, try breaking at a paragraph
    paragraphs = [match.end() for match in re.finditer(r'\n\s*\n', text[:max_length])]
    
    if paragraphs:
        return paragraphs[-1]
    
    # If no paragraphs, try breaking at a line break
    line_breaks = [match.end() for match in re.finditer(r'\n', text[:max_length])]
    
    if line_breaks:
        return line_breaks[-1]
    
    # If no good breaking points, try breaking at a word boundary
    word_breaks = [match.end() for match in re.finditer(r'\s+', text[:max_length])]
    
    if word_breaks:
        return word_breaks[-1]
    
    # If all else fails, break at the maximum length
    return max_length