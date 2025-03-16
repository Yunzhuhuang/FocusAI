# from typing import Dict, Optional

# # Dictionary of prompt templates for different tasks
# PROMPT_TEMPLATES = {
#     "summarize": """
# You are an assistant that summarizes text for people with dyslexia.
# Make your summaries clear, concise, and easy to understand.
# Use simple language and short sentences.
# Break complex ideas into digestible chunks.
# Avoid rare words, idioms, or complex grammar when possible.

# Here is the text to summarize:
# {text}

# Summary:
# """,

#     "simplify": """
# You are an assistant that simplifies text to make it more accessible for people with dyslexia.
# Your task is to rewrite the text to:
# 1. Use simpler vocabulary
# 2. Use shorter sentences
# 3. Use active voice instead of passive voice
# 4. Make the structure clearer with bullet points for lists
# 5. Explain difficult concepts in plain language

# Here is the text to simplify:
# {text}

# Simplified text:
# """,

#     "explain": """
# You are an assistant that explains complex topics to people with dyslexia.
# Your explanations should:
# 1. Be clear and methodical
# 2. Break down complex ideas step by step
# 3. Use simple language and short sentences
# 4. Use familiar examples and analogies
# 5. Avoid jargon unless you explain it immediately

# Here is the topic to explain:
# {text}

# Explanation:
# """,

#     "key_points": """
# You are an assistant that extracts key points from text for people with dyslexia.
# Extract the most important information as a bulleted list.
# Each point should be concise (1-2 sentences).
# Focus on the main ideas and essential details only.
# Use clear and simple language.

# Here is the text to extract key points from:
# {text}

# Key points:
# """
# }


# def get_prompt_template(prompt_type: str) -> str:
#     """
#     Get a prompt template by type
    
#     Args:
#         prompt_type: Type of prompt to get (summarize, simplify, explain, key_points)
        
#     Returns:
#         str: Prompt template string
#     """
#     if prompt_type in PROMPT_TEMPLATES:
#         return PROMPT_TEMPLATES[prompt_type]
#     else:
#         # Return the summarize template as default
#         return PROMPT_TEMPLATES["summarize"]


# def customize_prompt(prompt_type: str, **kwargs) -> str:
#     """
#     Get a customized prompt template with additional parameters
    
#     Args:
#         prompt_type: Type of prompt to customize
#         **kwargs: Additional parameters to include in the prompt
        
#     Returns:
#         str: Customized prompt template
#     """
#     # Get the base template
#     template = get_prompt_template(prompt_type)
    
#     # Add custom instructions if provided
#     if "custom_instructions" in kwargs:
#         # Insert the custom instructions before the final line
#         lines = template.splitlines()
#         custom_line = f"Additional instructions: {kwargs['custom_instructions']}"
        
#         # Insert before the last line (which is usually empty or contains just the template variable)
#         if len(lines) > 2:
#             result = "\n".join(lines[:-2] + [custom_line] + lines[-2:])
#         else:
#             result = template + "\n" + custom_line
            
#         return result
    
#     return template


# def generate_prompt(prompt_type: str, text: str, **kwargs) -> str:
#     """
#     Generate a complete prompt with the text inserted
    
#     Args:
#         prompt_type: Type of prompt to use
#         text: Text to insert into the prompt
#         **kwargs: Additional parameters for customization
        
#     Returns:
#         str: Complete prompt with text inserted
#     """
#     template = customize_prompt(prompt_type, **kwargs)
#     prompt_args = {"text": text, **kwargs}
    
#     return template.format(**prompt_args)
