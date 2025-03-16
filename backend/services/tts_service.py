import pyttsx3
import os
import uuid
from pathlib import Path

class TTSService:
    def __init__(self):
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent
        self.output_dir = str(project_root /"backend" / "temp" / "audio")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # Optional: Configure the engine
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Optional: List available voices and set a specific one
        voices = self.engine.getProperty('voices')
        if voices:
            # Usually index 0 is male voice, 1 is female voice
            self.engine.setProperty('voice', voices[0].id)

    def generate_speech(self, text: str, language: str = 'en') -> str:
        """
        Generate speech from text and save it as an MP3 file
        
        Args:
            text (str): The text to convert to speech
            language (str): Not used in pyttsx3, but kept for API compatibility
            
        Returns:
            str: Path to the generated audio file
        """
        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = str(Path(self.output_dir) / filename)  # Use absolute path

        # Generate speech
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()

        return filepath

    def cleanup_file(self, filepath: str):
        """
        Remove the generated audio file after it's been sent to the client
        
        Args:
            filepath (str): Path to the file to remove
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error cleaning up file {filepath}: {str(e)}")
