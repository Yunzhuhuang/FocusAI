from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from pathlib import Path

# Import services
from services.tts_service import TTSService
from config.config import DATA_DIR, TTS_CONFIG

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    rate: Optional[int] = None
    volume: Optional[float] = None


class TTSResponse(BaseModel):
    audio_url: str
    audio_file: str
    text: str
    metadata: dict


@router.post("/generate", response_model=TTSResponse)
async def generate_speech(tts_request: TTSRequest):
    """
    Generate speech from text
    
    Args:
        tts_request: Text to convert to speech with optional voice parameters
        
    Returns:
        TTSResponse: Response with audio URL and metadata
    """
    try:
        # Initialize TTS service
        tts_service = TTSService()
        
        # Generate unique filename
        audio_filename = f"{uuid.uuid4().hex}.{TTS_CONFIG['output_format']}"
        audio_path = Path(TTS_CONFIG['output_dir']) / audio_filename
        
        # Generate speech
        voice = tts_request.voice or TTS_CONFIG['voice']
        rate = tts_request.rate or TTS_CONFIG['rate']
        volume = tts_request.volume or TTS_CONFIG['volume']
        
        tts_service.generate_speech(
            text=tts_request.text,
            output_file=str(audio_path),
            voice=voice,
            rate=rate,
            volume=volume
        )
        
        # Generate URL for the audio file
        # In a real application, this would be a proper URL
        audio_url = f"/api/tts/audio/{audio_filename}"
        
        return TTSResponse(
            audio_url=audio_url,
            audio_file=audio_filename,
            text=tts_request.text,
            metadata={
                "voice": voice,
                "rate": rate,
                "volume": volume,
                "format": TTS_CONFIG['output_format'],
                "duration": tts_service.get_audio_duration(str(audio_path))
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Serve audio file
    
    Args:
        filename: Name of the audio file to serve
        
    Returns:
        FileResponse: Audio file
    """
    audio_path = Path(TTS_CONFIG['output_dir']) / filename
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        str(audio_path),
        media_type=f"audio/{TTS_CONFIG['output_format']}",
        filename=filename
    )


@router.post("/process_chunks")
async def process_chunks(chunk_ids: list):
    """
    Generate speech for multiple text chunks
    
    Args:
        chunk_ids: List of chunk IDs to generate speech for
        
    Returns:
        dict: Mapping of chunk IDs to audio URLs
    """
    # This is a placeholder for a more complex implementation
    # In a real application, you would need to store and retrieve chunks
    # based on their IDs, then generate speech for each one
    
    return {"message": "This endpoint would generate speech for multiple chunks"}
