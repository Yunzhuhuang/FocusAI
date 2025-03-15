import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

# Try to import llama_cpp, but provide fallback behavior if not installed
try:
    from llama_cpp import Llama
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

# Try to import transformers for alternative models
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from config.config import LLM_CONFIG
from utils.prompts import get_prompt_template


class LocalLLMService:
    """
    Service for interacting with local LLM models for text summarization
    and other NLP tasks.
    """
    
    def __init__(self, model_path: Optional[str] = None, model_type: Optional[str] = None):
        """
        Initialize the LLM service with the specified model
        
        Args:
            model_path: Path to the model file (defaults to config)
            model_type: Type of model to use (defaults to config)
        """
        self.model_path = model_path or LLM_CONFIG.get("model_path")
        self.model_type = model_type or LLM_CONFIG.get("model_type", "llama")
        self.context_window = LLM_CONFIG.get("context_window", 4096)
        self.max_tokens = LLM_CONFIG.get("max_tokens", 512)
        self.temperature = LLM_CONFIG.get("temperature", 0.7)
        self.top_p = LLM_CONFIG.get("top_p", 0.9)
        self.prompt_template = LLM_CONFIG.get("prompt_template", "")
        
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model based on configuration"""
        
        # For demo/development purposes, we'll provide a mock implementation
        # that doesn't require actual models to be installed
        if not os.path.exists(self.model_path):
            print(f"Warning: Model path {self.model_path} does not exist. Using mock implementation.")
            return
            
        if self.model_type == "llama" and LLAMA_AVAILABLE:
            try:
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=self.context_window,
                    n_batch=512
                )
            except Exception as e:
                print(f"Error loading Llama model: {e}")
                
        elif TRANSFORMERS_AVAILABLE:
            try:
                self.model = pipeline(
                    "summarization", 
                    model="facebook/bart-large-cnn"
                )
            except Exception as e:
                print(f"Error loading transformers model: {e}")
                
        else:
            print("No suitable LLM backend available. Using mock implementation.")
    
    def summarize(self, text: str) -> str:
        """
        Summarize the given text using the LLM
        
        Args:
            text: Text to summarize
            
        Returns:
            str: Summarized text
        """
        # If we don't have a real model, use a simplified mock implementation
        if self.model is None:
            # Simple mock implementation
            return f"Summary of text ({len(text)} chars): {text[:100]}..." if len(text) > 100 else text
        
        # Get the prompt from the template
        prompt = self.prompt_template.format(text=text)
        
        # Use the appropriate model type
        if self.model_type == "llama" and isinstance(self.model, Llama):
            response = self.model(
                prompt, 
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            return response["choices"][0]["text"].strip()
            
        elif TRANSFORMERS_AVAILABLE and "summarization" in str(type(self.model)):
            # For transformers pipeline
            result = self.model(text, max_length=self.max_tokens // 4, min_length=30, do_sample=False)
            return result[0]["summary_text"]
            
        else:
            # Fallback to mock implementation
            return f"Summary of text ({len(text)} chars): {text[:100]}..." if len(text) > 100 else text
    
    def process_text(self, text: str, prompt_type: str, **kwargs) -> str:
        """
        Process text with a specific prompt type
        
        Args:
            text: Text to process
            prompt_type: Type of prompt to use (summarize, simplify, etc.)
            **kwargs: Additional arguments for the prompt
            
        Returns:
            str: Processed text
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt_template(prompt_type)
        
        # Format the prompt with the text and any additional args
        prompt_args = {"text": text, **kwargs}
        prompt = prompt_template.format(**prompt_args)
        
        # Use the model to process the prompt
        if self.model is None:
            return f"Processed text with {prompt_type}: {text[:100]}..." if len(text) > 100 else text
            
        if self.model_type == "llama" and isinstance(self.model, Llama):
            response = self.model(
                prompt, 
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            return response["choices"][0]["text"].strip()
            
        elif TRANSFORMERS_AVAILABLE:
            # This is a simplified approach - in a real implementation,
            # you'd need different pipelines for different tasks
            result = self.model(text, max_length=self.max_tokens // 4, min_length=30, do_sample=False)
            return result[0]["summary_text"]
            
        else:
            return f"Processed text with {prompt_type}: {text[:100]}..." if len(text) > 100 else text
