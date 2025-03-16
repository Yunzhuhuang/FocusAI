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
        return chat(prompt)

if __name__ == '__main__':
    chatbot = chat_bot()
    print(chatbot.chat("tell me about ai"))