from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime
import os
from pathlib import Path

# Import services
from services.pdf_processor import PDFProcessor
from services.llm_api import LLMAPIService
from config.config import DATA_DIR

router = APIRouter()

class PDFInput(BaseModel):
    enable_tts: bool = False
    chunk_size: Optional[int] = None


class SummaryChunk(BaseModel):
    id: str
    page: int
    original_text: str
    summary: str
    audio_url: Optional[str] = None


class PDFSummaryResponse(BaseModel):
    request_id: str
    timestamp: str
    filename: str
    chunks: List[SummaryChunk]
    metadata: Dict[str, Any]


@router.post("/process", response_model=PDFSummaryResponse)
async def process_pdf(
    file: UploadFile = File(...),
    enable_tts: bool = Form(False),
    chunk_size: Optional[int] = Form(None)
):
    """
    Process and summarize PDF document
    
    Args:
        file: PDF file to process
        enable_tts: Whether to enable text-to-speech
        chunk_size: Optional custom chunk size
        
    Returns:
        PDFSummaryResponse: Summarized chunks with metadata
    """
    try:
        # Check if file is PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Save the uploaded file temporarily
        temp_file_path = Path(DATA_DIR) / "temp" / f"{uuid.uuid4().hex}.pdf"
        os.makedirs(temp_file_path.parent, exist_ok=True)
        
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Initialize services
        pdf_processor = PDFProcessor()
        llm_service = LLMAPIService()
        
        # Extract text from PDF
        pdf_text_by_page = pdf_processor.extract_text(temp_file_path)
        
        # Process each page into chunks
        summary_chunks = []
        
        for page_num, page_text in pdf_text_by_page.items():
            # Process text into chunks
            chunks = pdf_processor.chunk_text(page_text, chunk_size=chunk_size)
            
            for i, chunk in enumerate(chunks):
                # Get summary from LLM
                summary = llm_service.summarize(chunk)
                
                # Create chunk ID
                chunk_id = f"page_{page_num}_chunk_{i+1}_{uuid.uuid4().hex[:8]}"
                
                # Initialize chunk without audio
                summary_chunk = SummaryChunk(
                    id=chunk_id,
                    page=page_num,
                    original_text=chunk,
                    summary=summary,
                    audio_url=None
                )
                
                # Generate TTS if requested
                if enable_tts:
                    # TTS would be handled by a separate endpoint
                    # This endpoint would just prepare the data for TTS
                    pass
                    
                summary_chunks.append(summary_chunk)
        
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        # Prepare response
        response = PDFSummaryResponse(
            request_id=uuid.uuid4().hex,
            timestamp=datetime.now().isoformat(),
            filename=file.filename,
            chunks=summary_chunks,
            metadata={
                "total_chunks": len(summary_chunks),
                "total_pages": len(pdf_text_by_page),
                "enable_tts": enable_tts
            }
        )
        
        return response
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
