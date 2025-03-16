from pydantic import BaseModel
from typing import List
from backend.services.llm_api import chat_bot
from backend.services.text_processor import TextProcessor
from flask import Blueprint, request, send_file, jsonify
from langchain.prompts import PromptTemplate


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
        given the entire summarized texts.  generate a simple quiz game with multiple choice questions related to the texts.
        The return format should follow this structure:
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

        Response:
        """,
            input_variables=["texts"]
        )

        # Format the prompt with the input text
        formatted_prompt = prompt_template.format(texts=texts)
        
        # For debugging
        print(formatted_prompt)


    

        #llm_service = chat_bot()
  

        #response = llm_service.chat(formatted_prompt)
        #getting the "questions" from the response
        response = json.loads(response)
        response = {
            "questions": [
                {
                    "question": "What landed in the Whispering Woods?",
                    "options": ["A. A shooting star", "B. A falling tree", "C. A flying bird", "D. A lost animal"],
                    "answer": "A"
                },
                {
                    "question": "Who discovered the fallen star?",
                    "options": ["A. A group of hunters", "B. Lyra", "C. The village elder", "D. A forest creature"],
                    "answer": "B"
                },
                {
                    "question": "What did Lyra dream of?",
                    "options": ["A. Riches", "B. Adventure beyond the skies", "C. Power", "D. Eternal youth"],
                    "answer": "B"
                },
                {
                    "question": "What color was the glow from the star?",
                    "options": ["A. Red", "B. Blue", "C. Green", "D. Silver"],
                    "answer": "D"
                },
                {
                    "question": "What did the villagers believe about the fallen star?",
                    "options": ["A. It was dangerous", "B. It brought good luck", "C. It was a message from the gods", "D. It would bring rain"],
                    "answer": "C"
                }
            ]
        }

        print(response)
        # Return the LLM response
        return jsonify(response)
        
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500