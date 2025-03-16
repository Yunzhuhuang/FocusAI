# import requests
# from typing import Tuple, Optional, Dict, Any
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urlparse

# from config.config import WEB_CONFIG
# from services.text_processor import TextProcessor


# class WebScraper:
#     """
#     Service for scraping and processing text from web pages
#     """
    
#     def __init__(self, config: Optional[Dict[str, Any]] = None):
#         """
#         Initialize the web scraper with configuration
        
#         Args:
#             config: Custom configuration (defaults to global config)
#         """
#         self.config = config or WEB_CONFIG
#         self.timeout = self.config.get("timeout", 10)
#         self.user_agent = self.config.get("user_agent", "FocusAI Accessibility Reader/1.0")
#         self.extract_images = self.config.get("extract_images", False)
#         self.max_content_length = self.config.get("max_content_length", 1000000)
        
#         # Initialize the text processor for further text processing
#         self.text_processor = TextProcessor()
        
#     def scrape_url(self, url: str) -> Tuple[str, Optional[str]]:
#         """
#         Scrape and extract main content from a web page
        
#         Args:
#             url: URL of the web page to scrape
            
#         Returns:
#             Tuple[str, Optional[str]]: Extracted text content and page title
#         """
#         headers = {
#             "User-Agent": self.user_agent,
#             "Accept": "text/html,application/xhtml+xml,application/xml",
#             "Accept-Language": "en-US,en;q=0.9"
#         }
        
#         try:
#             # Make the request
#             response = requests.get(
#                 url, 
#                 headers=headers, 
#                 timeout=self.timeout,
#                 stream=True
#             )
            
#             # Check response
#             response.raise_for_status()
            
#             # Check content length
#             content_length = int(response.headers.get("Content-Length", 0))
#             if content_length > self.max_content_length:
#                 raise ValueError(f"Content too large: {content_length} bytes")
                
#             # Parse HTML
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Remove script and style elements that would clutter the text
#             for element in soup(["script", "style", "meta", "noscript"]):
#                 element.extract()
                
#             # Extract title
#             title = None
#             title_tag = soup.find("title")
#             if title_tag and title_tag.string:
#                 title = title_tag.string.strip()
                
#             # Extract main content - this is a simplified approach
#             # A more sophisticated implementation would detect the main content area
#             main_content = self._extract_main_content(soup)
            
#             # Process the text
#             processed_text = self.text_processor.preprocess_text(main_content)
            
#             return processed_text, title
            
#         except Exception as e:
#             raise RuntimeError(f"Error scraping URL {url}: {str(e)}")
    
#     def _extract_main_content(self, soup: BeautifulSoup) -> str:
#         """
#         Extract the main content from a BeautifulSoup object
        
#         Args:
#             soup: BeautifulSoup object representing the HTML
            
#         Returns:
#             str: Extracted main content
#         """
#         # Try to find main content container
#         # These are common IDs and classes for main content
#         main_selectors = [
#             "main", "article", "#content", "#main", ".content", ".main",
#             "#main-content", ".main-content", "[role=main]"
#         ]
        
#         for selector in main_selectors:
#             main_elem = soup.select_one(selector)
#             if main_elem:
#                 return main_elem.get_text(separator=' ', strip=True)
        
#         # If we can't find a specific content container, use the body
#         body = soup.find("body")
#         if body:
#             # Remove navigation, footer, header, and sidebar elements
#             for elem in body.select("nav, header, footer, .sidebar, #sidebar, .nav, .menu"):
#                 elem.extract()
                
#             # Get the remaining text
#             return body.get_text(separator=' ', strip=True)
            
#         # Fallback to just getting all text
#         return soup.get_text(separator=' ', strip=True)
        
#     def clean_html_content(self, html_content: str) -> str:
#         """
#         Clean HTML content to extract plain text
        
#         Args:
#             html_content: Raw HTML content
            
#         Returns:
#             str: Cleaned text content
#         """
#         # Parse HTML
#         soup = BeautifulSoup(html_content, "html.parser")
        
#         # Remove script and style elements
#         for element in soup(["script", "style", "meta", "noscript"]):
#             element.extract()
            
#         # Get text with spacing between elements
#         text = soup.get_text(separator=' ', strip=True)
        
#         # Clean up whitespace
#         text = re.sub(r'\s+', ' ', text).strip()
        
#         return text
        
#     def get_domain(self, url: str) -> str:
#         """
#         Extract the domain from a URL
        
#         Args:
#             url: URL to extract domain from
            
#         Returns:
#             str: Domain name
#         """
#         parsed_url = urlparse(url)
#         return parsed_url.netloc
