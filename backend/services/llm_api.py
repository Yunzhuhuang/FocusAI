import requests
import yaml

from backend.config.config import LLM_CONFIG
 
 
class chat_bot:
    def __init__(self):
        
        self.config = LLM_CONFIG
 
        self.api_key = self.config["api_key"]
        self.chat_url = self.config["chat_uri"]
               
    def chat(self, message: str) -> str:
        """
        Send a chat request to the model server and return the response
       
        Inputs:
        - message: The message to send to the chatbot
        """
        print(message)
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
 
if __name__ == '__main__':
    chatbot = chat_bot()
    print(chatbot.chat("tell me about ai"))
 