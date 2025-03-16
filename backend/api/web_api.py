from pydantic import BaseModel
from typing import List
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, jsonify
from langchain.prompts import PromptTemplate
from backend.config.config import LLM_CONFIG

import requests
from readability import Document
from bs4 import BeautifulSoup

def extract_text_from_web_uri(web_uri):
    """
    Extract meaningful text from a web URI using readability-lxml.

    Args:
        web_uri: A string representing the URI of the web page.

    Returns:
        A string containing the main content text from the web page.
    """
    try:
        response = requests.get(web_uri)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

    # Use readability to get the main content as HTML
    doc = Document(response.text)
    summary_html = doc.summary()

    # Parse the HTML to extract clean text
    soup = BeautifulSoup(summary_html, "html.parser")
    # Remove unwanted elements like scripts and styles
    for element in soup(["script", "style"]):
        element.decompose()
    
    # Get text and strip leading/trailing whitespace
    text = soup.get_text(separator="\n", strip=True)
    return text



web_api = Blueprint('web_api', __name__)


@web_api.route('/summarize', methods=['POST'])
def process_web_page_route():
    """
    Process and summarize web page input.

    Expects:
       A JSON payload or form data with a key 'web_uri'.

    Returns:
        JSON containing a list of summaries.
    """
    try:
        # Get the web_uri from JSON or form-data.
        data = request.get_json() or request.form
        web_uri = data.get('web_uri')
        if not web_uri:
            return jsonify({'error': 'No web_uri provided'}), 400

        # Extract text from the provided web URI.
        raw_text = extract_text_from_web_uri(web_uri)

        prompt = LLM_CONFIG["prompt_template"]

        prompt_template = PromptTemplate(
            template=prompt,
            input_variables=["text"]
        )
        
        # Initialize services.
        llm_service = chat_bot()
        text_processor = TextProcessor()

        # Chunk the extracted text.
        chunks = text_processor.chunk_text(text=raw_text)

        summaries = []
        for chunk in chunks:
           
            prompt = prompt_template.format(text=chunk)
            summaries.append(llm_service.chat(prompt))
        print(summaries)
            
        return jsonify({'summaries': summaries})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
