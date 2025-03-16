from typing import Dict, Any, Optional
import requests
from config.config import LLM_CONFIG

class LLMAPIService:
    """
    Service for making API calls to LLM service
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the LLM API service with configuration
        
        Args:
            config: Custom configuration (defaults to global config)
        """
        self.config = config or LLM_CONFIG
        self.api_key = self.config.get("api_key")
        self.api_url = self.config.get("api_url")
        
        if not self.api_key:
            raise ValueError("API key is required for LLM API service")
        if not self.api_url:
            raise ValueError("API URL is required for LLM API service")
            
    def summarize(self, text: str) -> str:
        """
        Generate a summary of the input text using the LLM API
        
        Args:
            text: Text to summarize
            
        Returns:
            str: Generated summary
        """
        try:
            # Prepare the prompt using the template
            prompt = self.config["prompt_template"].format(text=text)
            
            # Prepare the API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "accept": "application/json"
            }

            payload = {
                "message": prompt,
                "mode": "chat",
                "sessionId": "example-session-id",
                "attachments": []
            }
            
            # Make the API call
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            # Extract and return the summary from the response
            result = response.json()
            summary = result["choices"][0]["message"]["summary"].strip()
            return summary
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error calling LLM API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Error parsing LLM API response: {str(e)}") 