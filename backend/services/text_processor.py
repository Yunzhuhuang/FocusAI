from typing import List, Dict, Any, Optional
import re
from backend.config.config import TEXT_CONFIG
from backend.utils.chunking import split_text_into_chunks


class TextProcessor:
    """
    Service for processing and manipulating text content
    """
    
    def __init__(self):
        """
        Initialize the text processor with configuration
        
        Args:
            config: Custom configuration (defaults to global config)
        """
       
        self.chunk_size = 20
        self.chunk_overlap = 5
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into digestible chunks for processing
        
        Args:
            text: The text to split into chunks
            chunk_size: Optional custom chunk size
            
        Returns:
            List[str]: List of text chunks
        """
        
        # Use the chunking utility to split the text
        return split_text_into_chunks(
            text, 
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
