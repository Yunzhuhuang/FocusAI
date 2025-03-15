from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional

# Import API routes
from api.text_api import router as text_router
from api.pdf_api import router as pdf_router
from api.web_api import router as web_router
from api.tts_api import router as tts_router

# Create FastAPI app
app = FastAPI(
    title="FocusAI API",
    description="API for processing and summarizing documents for dyslexic readers",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(text_router, prefix="/api/text", tags=["Text Processing"])
app.include_router(pdf_router, prefix="/api/pdf", tags=["PDF Processing"])
app.include_router(web_router, prefix="/api/web", tags=["Web Scraping"])
app.include_router(tts_router, prefix="/api/tts", tags=["Text-to-Speech"])

@app.get("/")
async def root():
    """
    Root endpoint that returns basic API information
    """
    return {
        "message": "Welcome to FocusAI API",
        "version": "1.0.0",
        "endpoints": [
            "/api/text - Process text input",
            "/api/pdf - Process PDF documents",
            "/api/web - Process web URLs",
            "/api/tts - Convert text to speech"
        ]
    }

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
