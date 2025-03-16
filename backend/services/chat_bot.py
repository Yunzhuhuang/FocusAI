import requests
import sys
import threading
import time
import yaml

from config.config import LLM_CONFIG


class chat_bot:
    def __init__(self):
        self.api_key = LLM_CONFIG["api_key"]
        self.base_url = LLM_CONFIG["model_server_base_url"]
        self.workspace_slug = LLM_CONFIG["workspace_slug"]

        self.chat_url = f"{self.base_url}/workspace/{self.workspace_slug}/chat"
                
    def chat(self, message: str) -> str:
        """
        Send a chat request to the model server and return the response
        
        Inputs:
        - message: The message to send to the chatbot
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        data = {
            "message": message,
            "mode": "chat",
            "sessionId": "example-session-id",
            "attachments": []
        }

        chat_response = requests.post(
            self.chat_url,
            headers=headers,
            json=data
        )

        try:
            text_response = chat_response.json()['textResponse']
            return text_response
        except ValueError:
            return "Response is not valid JSON"
        except Exception as e:
            return f"Chat request failed. Error: {e}"

    def summarize(self, text):
        prompt = LLM_CONFIG["prompt_template"].format(text=text)
        return self.chat(prompt)

if __name__ == '__main__':
    chatbot = chat_bot()
    story = """The Clockmaker’s Secret
    
    In the heart of Eldoria, where cobbled streets twisted like forgotten stories and lanterns flickered with whispers of magic, lived an old clockmaker named Tobias Grinn. His shop, Grinn & Gears, was a peculiar place, filled with ticking wonders—clocks that whispered secrets, watches that ran backward, and hourglasses that never emptied.
    
    But the most mysterious of all was the Eclipse Clock, a grand, golden timepiece hidden in the back of his workshop. No one knew why Tobias never sold it, nor why he often stared at it in silence.
    
    One rainy evening, a young girl named Liora wandered into the shop, drenched and shivering. "I need time," she pleaded. "Just a little more."
    
    Tobias studied her with knowing eyes. “Time is a precious thing,” he said, leading her to the Eclipse Clock. “What would you give for just a moment more?”
    
    “Anything,” Liora whispered.
    
    With a deep sigh, Tobias reached into his coat and pulled out a small, silver key. He turned it in the clock’s keyhole, and the gears groaned as the hands spun backward. A golden mist swirled around Liora, and suddenly—she was gone.
    
    The rain outside halted.
    
    Time rewound.
    
    A second chance had been granted.
    
    Tobias closed the Eclipse Clock with a heavy heart. Another debt to time had been made. He only hoped that, one day, someone would come to rewind time for him too.
    
    And so the clockmaker waited, listening to the ticking of fate.
    """
    print(chatbot.summarize(story))