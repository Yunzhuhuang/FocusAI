from typing import List, Dict, Any, Optional
import re
from config.config import TEXT_CONFIG
from utils.chunking import split_text_into_chunks


class TextProcessor:
    """
    Service for processing and manipulating text content
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the text processor with configuration
        
        Args:
            config: Custom configuration (defaults to global config)
        """
        self.config = config or TEXT_CONFIG
        self.chunk_size = self.config.get("chunk_size", 1000)
        self.chunk_overlap = self.config.get("chunk_overlap", 200)
    
    def chunk_text(self, text: str, chunk_size: Optional[int] = None) -> List[str]:
        """
        Split text into digestible chunks for processing
        
        Args:
            text: The text to split into chunks
            chunk_size: Optional custom chunk size
            
        Returns:
            List[str]: List of text chunks
        """
        chunk_size = chunk_size or self.chunk_size
        
        # Use the chunking utility to split the text
        return split_text_into_chunks(
            text, 
            chunk_size=chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text to improve quality before chunking or summarization
        
        Args:
            text: The text to preprocess
            
        Returns:
            str: Preprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove URLs (simplified version)
        text = re.sub(r'https?://\S+', '[URL]', text)
        
        # Simple handling of common special characters
        text = text.replace('\t', ' ')
        text = text.replace('\n\n', '\n')
        
        return text
    
    def extract_key_sentences(self, text: str, num_sentences: int = 3) -> List[str]:
        """
        Extract key sentences from text
        
        Args:
            text: The text to extract sentences from
            num_sentences: Number of key sentences to extract
            
        Returns:
            List[str]: List of key sentences
        """
        # Very simple implementation - just get the first few sentences
        # In a real implementation, you'd use a more sophisticated approach
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return sentences[:min(num_sentences, len(sentences))]
    
    def format_output(self, chunks: List[str], summaries: List[str]) -> Dict[str, Any]:
        """
        Format processed text chunks and summaries into output format
        
        Args:
            chunks: Original text chunks
            summaries: Summarized versions of the chunks
            
        Returns:
            Dict[str, Any]: Formatted output with chunks and summaries
        """
        result = []
        
        for i, (chunk, summary) in enumerate(zip(chunks, summaries)):
            result.append({
                "chunk_id": i + 1,
                "original_text": chunk,
                "summary": summary
            })
            
        return {
            "total_chunks": len(result),
            "chunks": result
        }
