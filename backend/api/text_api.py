
from pydantic import BaseModel
from typing import List
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, send_file, jsonify
from langchain.prompts import PromptTemplate
from backend.config.config import LLM_CONFIG

text_api = Blueprint('text_api', __name__)



@text_api.route('/summarize', methods=['POST'])
async def process_text():
    """
    Process and summarize text input
    
    Args:
        text_input: Text content to be processed and summarized
        request: Request object to access headers

    Returns:
        List of summaries in JSON format
    """
    try:
        text_input = request.get_json()
        # Read the API key from the header

        llm_service = chat_bot()
        text_processor = TextProcessor()

        prompt = LLM_CONFIG["prompt_template"]

        prompt_template = PromptTemplate(
            template=prompt,
            input_variables=["text"]
        )

        #chunk the text
        chunks = text_processor.chunk_text(text = text_input['content'])

        summaries = []
        for chunk in chunks:
        #     #summarize the text
            prompt = prompt_template.format(text=chunk)
            summaries.append(llm_service.chat(prompt))
            
        return jsonify(summaries)

        
    except Exception as e:
        return jsonify({'error': str(e)}), 500