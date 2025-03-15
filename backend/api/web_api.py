from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
import json
import uuid
from datetime import datetime

# Import services
from services.web_scraper import WebScraper
from services.text_processor import TextProcessor
from services.local_llm import LocalLLMService

router = APIRouter()

class WebInput(BaseModel):
    url: HttpUrl
    enable_tts: bool = False
    chunk_size: Optional[int] = None


class SummaryChunk(BaseModel):
    id: str
    original_text: str
    summary: str
    audio_url: Optional[str] = None


class WebSummaryResponse(BaseModel):
    request_id: str
    timestamp: str
    url: str
    title: Optional[str]
    chunks: List[SummaryChunk]
    metadata: Dict[str, Any]


@router.post("/process", response_model=WebSummaryResponse)
async def process_web_url(web_input: WebInput):
    """
    Process and summarize content from a web URL
    
    Args:
        web_input: URL and processing options
        
    Returns:
        WebSummaryResponse: Summarized chunks with metadata
    """
    try:
        # Initialize services
        web_scraper = WebScraper()
        text_processor = TextProcessor()
        llm_service = LocalLLMService()
        
        # Scrape the web content
        web_content, page_title = web_scraper.scrape_url(str(web_input.url))
        
        if not web_content:
            raise HTTPException(status_code=400, detail="Could not extract content from the provided URL")
        
        # Process text into chunks
        chunks = text_processor.chunk_text(web_content, chunk_size=web_input.chunk_size)
        
        # Summarize each chunk
        summary_chunks = []
        for i, chunk in enumerate(chunks):
            # Get summary from LLM
            summary = llm_service.summarize(chunk)
            
            # Create chunk ID
            chunk_id = f"web_chunk_{i+1}_{uuid.uuid4().hex[:8]}"
            
            # Initialize chunk without audio
            summary_chunk = SummaryChunk(
                id=chunk_id,
                original_text=chunk,
                summary=summary,
                audio_url=None
            )
            
            # Generate TTS if requested
            if web_input.enable_tts:
                # TTS would be handled by a separate endpoint
                # This endpoint would just prepare the data for TTS
                pass
                
            summary_chunks.append(summary_chunk)
            
        # Prepare response
        response = WebSummaryResponse(
            request_id=uuid.uuid4().hex,
            timestamp=datetime.now().isoformat(),
            url=str(web_input.url),
            title=page_title,
            chunks=summary_chunks,
            metadata={
                "total_chunks": len(summary_chunks),
                "original_length": len(web_content),
                "enable_tts": web_input.enable_tts
            }
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing web URL: {str(e)}")
