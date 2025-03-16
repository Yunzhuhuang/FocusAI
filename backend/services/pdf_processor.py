import os
from typing import Dict, List, Any, Optional
import PyPDF2
from pathlib import Path

from config.config import PDF_CONFIG
from utils.chunking import split_text_into_chunks
from services.text_processor import TextProcessor


class PDFProcessor:
    """
    Service for extracting and processing text from PDF files
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the PDF processor with configuration
        
        Args:
            config: Custom configuration (defaults to global config)
        """
        self.config = config or PDF_CONFIG
        self.chunk_size = self.config.get("chunk_size", 1000)
        self.chunk_overlap = self.config.get("chunk_overlap", 200)
        self.max_pages = self.config.get("max_pages", 100)
        
        # Initialize the text processor for further text processing
        self.text_processor = TextProcessor()
    
    def extract_text(self, pdf_path: str) -> Dict[int, str]:
        """
        Extract text content from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dict[int, str]: Dictionary mapping page numbers to text content
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        results = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Limit pages to maximum allowed
                num_pages = min(len(reader.pages), self.max_pages)
                
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    
                    if text:
                        # Preprocess the extracted text
                        processed_text = self.text_processor.preprocess_text(text)
                        results[page_num + 1] = processed_text  # 1-indexed page numbers
        
        except Exception as e:
            raise RuntimeError(f"Error extracting text from PDF: {str(e)}")
            
        return results
    
    def chunk_text(self, text: str, chunk_size: Optional[int] = None) -> List[str]:
        """
        Split text into digestible chunks for processing
        
        Args:
            text: The text to split into chunks
            chunk_size: Optional custom chunk size
            
        Returns:
            List[str]: List of text chunks
        """
        # Delegate to the text processor
        return self.text_processor.chunk_text(text, chunk_size or self.chunk_size)
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF file - extract text and split into chunks
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dict[str, Any]: Processed PDF data with page and chunk information
        """
        # Extract text by page
        pages_text = self.extract_text(pdf_path)
        
        # Process each page into chunks
        results = {
            "filename": Path(pdf_path).name,
            "total_pages": len(pages_text),
            "pages": []
        }
        
        for page_num, text in pages_text.items():
            chunks = self.chunk_text(text)
            
            page_data = {
                "page_number": page_num,
                "content_length": len(text),
                "total_chunks": len(chunks),
                "chunks": chunks
            }
            
            results["pages"].append(page_data)
            
        return results
