from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime

# Import services
from services.text_processor import TextProcessor
from services.llm_api import LLMAPIService

router = APIRouter()

class TextInput(BaseModel):
    content: str
    enable_tts: bool = False
    chunk_size: Optional[int] = None
    

class SummaryChunk(BaseModel):
    id: str
    original_text: str
    summary: str
    audio_url: Optional[str] = None


class SummaryResponse(BaseModel):
    request_id: str
    timestamp: str
    chunks: List[SummaryChunk]
    metadata: Dict[str, Any]


@router.post("/process", response_model=SummaryResponse)
async def process_text(text_input: TextInput):
    """
    Process and summarize text input
    
    Args:
        text_input: Text content to be processed and summarized
        
    Returns:
        SummaryResponse: Summarized chunks with metadata
    """
    try:
        # Initialize services
        text_processor = TextProcessor()
        llm_service = LLMAPIService()
        
        # Process text into chunks
        chunks = text_processor.chunk_text(text_input.content, chunk_size=text_input.chunk_size)
        
        # Summarize each chunk
        summary_chunks = []
        for i, chunk in enumerate(chunks):
            # Get summary from LLM
            summary = llm_service.summarize(chunk)
            
            # Create chunk ID
            chunk_id = f"chunk_{i+1}_{uuid.uuid4().hex[:8]}"
            
            # Initialize chunk without audio
            summary_chunk = SummaryChunk(
                id=chunk_id,
                original_text=chunk,
                summary=summary,
                audio_url=None
            )
            
            # Generate TTS if requested
            if text_input.enable_tts:
                # TTS would be handled by a separate endpoint
                # This endpoint would just prepare the data for TTS
                pass
                
            summary_chunks.append(summary_chunk)
            
        # Prepare response
        response = SummaryResponse(
            request_id=uuid.uuid4().hex,
            timestamp=datetime.now().isoformat(),
            chunks=summary_chunks,
            metadata={
                "total_chunks": len(summary_chunks),
                "original_length": len(text_input.content),
                "enable_tts": text_input.enable_tts
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")
