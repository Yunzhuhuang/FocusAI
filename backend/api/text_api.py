from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List
from services.llm_api import LLMAPIService
from services.text_processor import TextProcessor

# Define the router
router = APIRouter()

# Define the input model
class TextInput(BaseModel):
    content: str

@router.post("/process")
async def process_text(text_input: TextInput, request: Request):
    """
    Process and summarize text input
    
    Args:
        text_input: Text content to be processed and summarized
        request: Request object to access headers

    Returns:
        List of summaries in JSON format
    """
    try:
        # Read the API key from the header
        api_key = request.headers.get('api_key')
        if not api_key:
            raise HTTPException(status_code=401, detail="API key is missing")

       #print the api key
        #print(api_key)

        llm_service = LLMAPIService()
        text_processor = TextProcessor()

        #print the content
        #print(text_input.content)

        #chunk the text
        chunks = text_processor.chunk_text(text_input.content)

        #print the chunks
        #print(chunks)

        #summarize the text
        summaries = llm_service.summarize(chunks)

        #print the summaries
        print(summaries)

        
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")