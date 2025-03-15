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
    
    # Find natural paragraph breaks
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    current_size = 0
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed chunk size, save the current chunk
        # unless the current chunk is empty (meaning the paragraph is longer than chunk_size)
        if current_size + len(paragraph) > chunk_size and current_size > 0:
            chunks.append(current_chunk)
            
            # Start a new chunk with overlap
            if chunk_overlap > 0 and current_chunk:
                # Get the last chunk_overlap characters as overlap
                words = current_chunk.split()
                overlap_words = []
                overlap_size = 0
                
                # Add words from the end until we reach the desired overlap
                for word in reversed(words):
                    if overlap_size + len(word) + 1 > chunk_overlap:
                        break
                    overlap_words.insert(0, word)
                    overlap_size += len(word) + 1  # +1 for the space
                
                # Start the new chunk with the overlap
                current_chunk = " ".join(overlap_words)
                current_size = overlap_size
            else:
                current_chunk = ""
                current_size = 0
        
        # Add the paragraph to the current chunk
        if current_size > 0:
            current_chunk += "\n\n" + paragraph
            current_size += 2 + len(paragraph)  # +2 for the newlines
        else:
            current_chunk = paragraph
            current_size = len(paragraph)
        
        # If the paragraph itself is longer than chunk_size, we need to split it
        while current_size > chunk_size:
            # Find a good breaking point - ideally at a sentence end
            break_point = find_break_point(current_chunk, chunk_size)
            
            # Add the chunk up to the break point
            chunks.append(current_chunk[:break_point].strip())
            
            # Calculate overlap
            if chunk_overlap > 0:
                # Get the last chunk_overlap characters as overlap
                overlap_start = max(0, break_point - chunk_overlap)
                overlap_text = current_chunk[overlap_start:break_point]
                
                # Start the new chunk with the overlap
                current_chunk = overlap_text + current_chunk[break_point:]
                current_size = len(current_chunk)
            else:
                # No overlap, just continue with the rest
                current_chunk = current_chunk[break_point:].strip()
                current_size = len(current_chunk)
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
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
