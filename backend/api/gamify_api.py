from pydantic import BaseModel
from typing import List
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, send_file, jsonify
from langchain.prompts import PromptTemplate
import json
import re
 
 
gamify_api = Blueprint('gamify_api', __name__)
 
 
 
@gamify_api.route('/games', methods=['POST'])
async def quiz_game():
    """
    given the entire summarization.  generate a simple quiz game with multiple choice questions
    """
    try:
        texts = request.get_json()['text']  
 
        # Define the prompt directly without f-string
        prompt_template = PromptTemplate(
            template="""
        given the entire summarized texts. generate a simple quiz game with multiple choice questions related to the texts.
        The return format should only contain text follow this structure. Your response should only contain JSON:
        {{
            "questions": [
                {{
                    "question": "question",
                    "options": ["option1", "option2", "option3", "option4"],
                    "answer": "answer"
                }},
                ...
            ]
        }}
 
        Here is one example response:
        {{
            "questions": [
                {{
                    "question": "Which of these follwing statements is true for the number PI?",
                    "options": ["A. It is a rational number", "B. It is a irrational number", "C. It is a prime number", "D. It is a composite number"],
                    "answer": "B"
                }},
                {{
                    "question": "how PI is related to the circle?",
                    "options": ["A. It is the circumference of the circle", "B. It is the area of the circle", "C. It is the diameter of the circle", "D. It is the radius of the circle"],
                    "answer": "A"
                }},
                ...
            ]
        }}
        
        Here are the texts to generate the quiz game, Generate questions and answers based on the texts with the given format:
        {texts}
 
        JSON Response:
        """,
            input_variables=["texts"]
        )
 
        # Format the prompt with the input text
        formatted_prompt = prompt_template.format(texts=texts)
    
        llm_service = chat_bot()
  
        response = llm_service.chat(formatted_prompt)

        response = json_extractor(response)
 
        # Return the LLM response
        return response
        
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def json_extractor(response):
    # Extract JSON using regex
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        response = json_match.group(0)  # Get the JSON part
    else:
        print("❌ No valid JSON found!")
        return jsonify({'error': 'Invalid JSON format from LLM'}), 500
    
    # Validate JSON format
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        print("❌ LLM returned invalid JSON:", str(e))
        return jsonify({'error': 'LLM response is not valid JSON'}), 500
    
    return jsonify(response_json)