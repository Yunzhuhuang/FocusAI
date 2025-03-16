import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Application configuration
APP_CONFIG = {
    "name": "FocusAI",
    "version": "1.0.0",
    "debug": True,
}

# LLM Configuration
LLM_CONFIG = {
    "api_key": "4MBHZ92-B7VMCQ6-HC07GZ1-0ZC8WDR",  # Your API key here
    "chat_uri": "http://localhost:3001/api/v1/workspace/focusai/chat",  # API endpoint
    "prompt_template": """
You are an assistant that summarizes text for people with dyslexia.
Make your summaries clear, concise, and easy to understand.
Use simple language and short sentences.
Break complex ideas into digestible chunks.

Here is the text to summarize:
{text}

Summary:
    """
}

# PDF Processing configuration
PDF_CONFIG = {
    "chunk_size": 1000,     # Characters per chunk
    "chunk_overlap": 200,   # Overlap between chunks
    "max_pages": 100,       # Maximum pages to process
}

# Text Processing configuration
TEXT_CONFIG = {
    "chunk_size": 1000,     # Characters per chunk
    "chunk_overlap": 200,   # Overlap between chunks
}

# Web Scraping configuration
WEB_CONFIG = {
    "timeout": 10,          # Request timeout in seconds
    "user_agent": "FocusAI Accessibility Reader/1.0",
    "extract_images": False,
    "max_content_length": 1000000,  # Maximum content length in bytes
}

# Text-to-Speech configuration
TTS_CONFIG = {
    "engine": "pyttsx3",    # TTS engine to use
    "voice": "com.apple.speech.synthesis.voice.alex",  # Default voice
    "rate": 150,            # Speech rate
    "volume": 1.0,          # Volume (0.0 to 1.0)
    "output_format": "mp3", # Output audio format
    "output_dir": str(DATA_DIR / "audio"),  # Directory for audio files
}

# Ensure audio output directory exists
os.makedirs(TTS_CONFIG["output_dir"], exist_ok=True)
