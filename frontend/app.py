import streamlit as st
import requests
import json
import os
import tempfile
from pathlib import Path
import base64

# Set page configuration
st.set_page_config(
    page_title="FocusAI - Document Simplification",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force white background at the beginning
st.markdown(
    """
    <style>
    #root > div:first-child {
        background-color: white !important;
    }
    body {
        background-color: white !important;
    }
    .stApp {
        background-color: white !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Custom CSS for a more dyslexia-friendly UI
st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff;
        padding: 2rem;
    }
    .stApp {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #2C3E50;
    }
    p, li {
        font-family: 'Arial', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #000000;
    }
    .stButton button {
        background-color: #3498DB;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #2980B9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .upload-option {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .upload-option:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .navigation-button {
        display: inline-block;
        background-color: #2ecc71;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-size: 1.2rem;
    }
    .document-viewer {
        background-color: white;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-top: 20px;
        min-height: 300px;
    }
    /* Ensure text is always visible */
    .document-viewer p {
        color: #000000 !important;
        background-color: white;
        padding: 10px;
        border-radius: 5px;
    }
    /* Make sure all text in the app is properly visible */
    .stMarkdown, .stText {
        color: #000000 !important;
    }
    /* Increase contrast for better readability */
    .stTextInput input, .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff;
        border: 1px solid #cccccc;
    }
    /* Make sure Streamlit container backgrounds are white */
    .stContainer, div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"] {
        background-color: #ffffff !important;
    }
    /* Remove any background colors from page sections */
    section[data-testid="stSidebar"], header[data-testid="stHeader"], footer[data-testid="stFooter"] {
        background-color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Backend API URL
API_URL = "http://localhost:8000/api"

# Initialize session state variables if they don't exist
if 'upload_option' not in st.session_state:
    st.session_state.upload_option = None
    
if 'document_chunks' not in st.session_state:
    st.session_state.document_chunks = []
    
if 'current_chunk_index' not in st.session_state:
    st.session_state.current_chunk_index = 0
    
if 'audio_html' not in st.session_state:
    st.session_state.audio_html = None
    
if 'current_audio_chunk' not in st.session_state:
    st.session_state.current_audio_chunk = -1

# Functions to handle different upload options
def handle_pdf_upload(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        
        try:
            files = {'pdf': open(temp_file_path, 'rb')}
            response = requests.post(f"{API_URL}/pdf/summarize", files=files)
            os.unlink(temp_file_path)  # Clean up the temp file
            
            if response.status_code == 200:
                data = response.json()
                summaries = data.get('summaries', [])
                
                # Ensure we have valid, non-empty summaries
                if not summaries:
                    # If backend returned empty summaries array, add placeholder text
                    st.warning("The backend returned empty content. Using placeholder text instead.")
                    summaries = ["This is placeholder text because the backend returned empty content. "
                                 "If you're seeing this, there might be an issue with the backend processing."]
                
                st.session_state.document_chunks = summaries
                st.session_state.current_chunk_index = 0
                return True
            else:
                st.error(f"Error processing PDF: {response.text}")
                return False
        except Exception as e:
            st.error(f"An error occurred: {e}")
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)  # Clean up in case of errors
            return False
    return False

def handle_text_upload(text_content):
    if text_content:
        try:
            payload = {"content": text_content}
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{API_URL}/text/summarize", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()

                # Check if data is array or object
                if isinstance(data, list):
                    summaries = data
                else:
                    summaries = data.get('summaries', [])
                
                # Ensure we have valid, non-empty summaries
                if not summaries:
                    # If backend returned empty content, use chunks of the original text
                    st.warning("The backend returned empty content. Using original text instead.")
                    # Split original text into paragraphs or chunks for display
                    summaries = [p for p in text_content.split('\n\n') if p.strip()]
                    if not summaries:
                        summaries = [text_content]
                
                st.session_state.document_chunks = summaries
                st.session_state.current_chunk_index = 0
                return True
            else:
                st.error(f"Error processing text: {response.text}")
                return False
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return False
    return False

def handle_web_upload(url):
    if url:
        try:
            payload = {"web_uri": url}
            headers = {"Content-Type": "application/json"}
            response = requests.post(f"{API_URL}/web/summarize", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                summaries = data.get('summaries', [])
                
                # Ensure we have valid, non-empty summaries
                if not summaries:
                    # If backend returned empty summaries array, add placeholder text
                    st.warning("The backend returned empty content. Using placeholder text instead.")
                    summaries = ["This is placeholder text because the backend returned empty content for the web page. "
                                 "If you're seeing this, there might be an issue with the backend processing."]
                
                st.session_state.document_chunks = summaries
                st.session_state.current_chunk_index = 0
                return True
            else:
                st.error(f"Error processing web page: {response.text}")
                return False
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return False
    return False

# Navigation functions
def next_chunk():
    if st.session_state.current_chunk_index < len(st.session_state.document_chunks) - 1:
        st.session_state.current_chunk_index += 1

def prev_chunk():
    if st.session_state.current_chunk_index > 0:
        st.session_state.current_chunk_index -= 1

# Add a function to handle text-to-speech conversion
def text_to_speech(text, language='en'):
    """Convert text to speech using the TTS API."""
    try:
        payload = {"text": text, "language": language}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{API_URL}/tts/tts", json=payload, headers=headers)
        
        if response.status_code == 200:
            # Get the audio content
            audio_content = response.content
            
            # Create a base64 encoded string for the audio
            b64_audio = base64.b64encode(audio_content).decode()
            
            # Create an HTML audio element
            audio_html = f"""
            <audio controls autoplay style="width: 100%;">
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """
            # Store in session state
            st.session_state.audio_html = audio_html
            st.session_state.current_audio_chunk = st.session_state.current_chunk_index
            return audio_html
        else:
            st.error(f"Error generating speech: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Main app layout
def main():
    st.title("FocusAI - Document Simplification")
    st.markdown("### A tool for simplifying and summarizing documents for people with dyslexia")
    
    # View mode: either uploading or viewing chunks
    if not st.session_state.document_chunks:
        display_upload_options()
    else:
        display_document_viewer()

def display_upload_options():
    st.markdown("## Upload your document")
    st.markdown("Choose one of the following options to upload your document:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### PDF Document")
            st.image("https://cdn-icons-png.flaticon.com/512/337/337946.png", width=100)
            if st.button("Choose PDF", key="pdf_button"):
                st.session_state.upload_option = "pdf"
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### Text Input")
            st.image("https://cdn-icons-png.flaticon.com/512/2911/2911226.png", width=100)
            if st.button("Enter Text", key="text_button"):
                st.session_state.upload_option = "text"
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### Web Page")
            st.image("https://cdn-icons-png.flaticon.com/512/726/726056.png", width=100)
            if st.button("Enter URL", key="web_button"):
                st.session_state.upload_option = "web"
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Display the appropriate upload form based on selection
    if st.session_state.upload_option == "pdf":
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 15px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### Upload PDF Document")
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file is not None:
                st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                if st.button("Process Document"):
                    with st.spinner("Processing PDF..."):
                        if handle_pdf_upload(uploaded_file):
                            st.success("PDF processed successfully!")
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.upload_option == "text":
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 15px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### Enter Text")
            text_content = st.text_area("Paste or type your text here:", height=300)
            if st.button("Process Text"):
                with st.spinner("Processing text..."):
                    if handle_text_upload(text_content):
                        st.success("Text processed successfully!")
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.upload_option == "web":
        with st.container(border=True):
            st.markdown("<div style='background-color: #ffffff; padding: 15px; border-radius: 5px;'>", unsafe_allow_html=True)
            st.markdown("### Enter Web Page URL")
            url = st.text_input("Enter the URL of the web page:")
            if st.button("Process Web Page"):
                with st.spinner("Processing web page..."):
                    if handle_web_upload(url):
                        st.success("Web page processed successfully!")
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

def display_document_viewer():
    st.markdown("## Document Viewer")
    
    # Navigation and chunk counter
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=(st.session_state.current_chunk_index == 0)):
            prev_chunk()
    
    with col2:
        st.markdown(f"<div style='text-align: center;'>Chunk {st.session_state.current_chunk_index + 1} of {len(st.session_state.document_chunks)}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ➡️", disabled=(st.session_state.current_chunk_index == len(st.session_state.document_chunks) - 1)):
            next_chunk()
    
    # Document content with improved styling for visibility and white background
    # Combine the container and content in a single markdown call to ensure proper nesting
    if st.session_state.document_chunks:
        current_chunk = st.session_state.document_chunks[st.session_state.current_chunk_index]
        
        # Combine div and p in one markdown call to ensure proper containment
        st.markdown(
            f"""
            <div class='document-viewer' style='background-color: #ffffff; border: 1px solid #e0e0e0; padding: 25px; border-radius: 10px; min-height: 300px;'>
                <p style='font-size: 1.2rem; line-height: 1.8; color: #000000; font-weight: 500; background-color: #ffffff;'>{current_chunk}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Add a text-to-speech button with better styling
        col_space1, col_tts, col_space2 = st.columns([3, 3, 3])
        
        with col_tts:
            # Use Streamlit's container for better styling
            with st.container(border=True):
                # Check if we already have audio for this chunk
                has_current_audio = (st.session_state.current_audio_chunk == st.session_state.current_chunk_index and 
                                     st.session_state.audio_html is not None)
                
                # Display the button text based on whether we have audio or not
                button_text = "🔊 Play Audio Again" if has_current_audio else "🔊 Listen to this text"
                
                # Listen button with improved styling and clear call to action
                if st.button(button_text, key="tts_button", use_container_width=True):
                    with st.spinner("Generating audio..."):
                        # Call the TTS API only if we don't already have audio for this chunk
                        if not has_current_audio:
                            audio_html = text_to_speech(current_chunk)
                        else:
                            audio_html = st.session_state.audio_html
                            
                        if audio_html:
                            # Show the audio player
                            st.markdown(audio_html, unsafe_allow_html=True)
                            st.success("Audio ready!")
        
        # Always display the audio player if we have it for the current chunk
        if (st.session_state.current_audio_chunk == st.session_state.current_chunk_index and 
            st.session_state.audio_html is not None):
            st.markdown(st.session_state.audio_html, unsafe_allow_html=True)
        
        # Debug information to check content
        st.caption(f"Debug - Content length: {len(current_chunk) if current_chunk else 0} characters")
    else:
        st.markdown(
            """
            <div class='document-viewer' style='background-color: #ffffff; border: 1px solid #e0e0e0; padding: 25px; border-radius: 10px; min-height: 300px;'>
                <p style='color: #000000; background-color: #ffffff;'>No document content to display.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Option to start over
    if st.button("Start Over"):
        st.session_state.document_chunks = []
        st.session_state.current_chunk_index = 0
        st.session_state.upload_option = None
        st.session_state.audio_html = None
        st.session_state.current_audio_chunk = -1
        st.rerun()

if __name__ == "__main__":
    main() 