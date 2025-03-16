
from pydantic import BaseModel
from typing import List
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, send_file, jsonify


gamify_api = Blueprint('gamify_api', __name__)



@gamify_api.route('/games', methods=['POST'])
async def quiz_game():
    """
    given the entire summarization.  generate a simple quiz game with multiple choice questions
    """
    try:
        texts = request.get_json()['text']
        # Read the API key from the header

        prompt = f"""
        given the entire summarized texts.  generate a simple quiz game with multiple choice questions related to the texts.
        The return format should follow this structure:
        {
            "questions": [
                {
                    "question": "question",
                    "options": ["option1", "option2", "option3", "option4"],
                    "answer": "answer"
                },
                ...
            ]
        }

        Here is one example response:
        {
            "questions": [
                {
                    "question": "Which of these follwing statements is true for the number PI?",
                    "options": ["A. It is a rational number", "B. It is a irrational number", "C. It is a prime number", "D. It is a composite number"],
                    "answer": "B"
                },
                {
                    "question": "how PI is related to the circle?",
                    "options": ["A. It is the circumference of the circle", "B. It is the area of the circle", "C. It is the diameter of the circle", "D. It is the radius of the circle"],
                    "answer": "A"
                },
                ...
            ]
        }
        
        Here are the texts to generate the quiz game, Generate questions and answers based on the texts with the given format:
        {texts}

        Response:

        """

        prompt_template = PromptTemplate(
            template=prompt,
            input_variables=["texts"]
        )

        prompt = prompt_template.format(texts=texts)

        test = {"questions": [
                {
                    "question": "Which of these follwing statements is true for the number PI?",
                    "options": ["A. It is a rational number", "B. It is a irrational number", "C. It is a prime number", "D. It is a composite number"],
                    "answer": "B"
                },
                {
                    "question": "how PI is related to the circle?",
                    "options": ["A. It is the circumference of the circle", "B. It is the area of the circle", "C. It is the diameter of the circle", "D. It is the radius of the circle"],
                    "answer": "A"
                }
            
            ]
        }

        ## this needs to be converted back to lllm response

        
        #llm_service = chat_bot()
        #response = llm_service.chat(prompt)

        return jsonify(test)

        
    except Exception as e:
        return jsonify({'error': str(e)}), 500