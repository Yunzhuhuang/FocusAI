from pydantic import BaseModel
from typing import List
import pdfplumber
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, jsonify

pdf_api = Blueprint('pdf_api', __name__)

def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file using pdfplumber.

    Args:
        pdf_file: A file-like object representing the PDF.

    Returns:
        A string containing the concatenated text from the PDF pages.
    """
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"
    return extracted_text

@pdf_api.route('/summarize', methods=['POST'])
def process_pdf_route():
    """
    Process and summarize PDF input.

    Expects:
        A file upload with key 'pdf'.

    Returns:
        JSON containing a list of summaries.
    """
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf']

        # Process the PDF: extract text using pdfplumber.
        raw_text = extract_text_from_pdf(pdf_file)
        
        # Initialize services.
        llm_service = chat_bot()
        text_processor = TextProcessor()

        # Chunk the text.
        chunks = text_processor.chunk_text(text=raw_text)

        summaries = []
        for chunk in chunks:
            print(chunk)  # Debug: print each chunk.
            # Summarize each text chunk.
            #summary = llm_service.chat(chunk)
            #summaries.append(summary)
            
        return jsonify({'summaries': summaries})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
