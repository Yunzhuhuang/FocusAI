import os
import uuid
from pathlib import Path
from gtts import gTTS

class TTSService:
    def __init__(self):
        # Get the project root directory - fixed path resolution
        self.base_dir = Path(__file__).parent.parent  # This resolves to the backend directory
        self.output_dir = self.base_dir / "temp" / "audio"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_speech(self, text: str, language: str = 'en') -> str:
        """
        Generate speech from text and save it as an MP3 file using Google's TTS
        
        Args:
            text (str): The text to convert to speech
            language (str): Language code (e.g., 'en', 'fr', 'es')
            
        Returns:
            str: Path to the generated audio file
        """
        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        
        # Make sure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Construct the full file path
        filepath = str(self.output_dir / filename)

        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to file
            tts.save(filepath)
            
            # Verify the file was created
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Failed to generate audio file at {filepath}")
                
            print(f"Audio file successfully created at: {filepath}")
            return filepath
            
        except Exception as e:
            error_msg = f"Error generating speech with gTTS: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)

    def cleanup_file(self, filepath: str):
        """
        Remove the generated audio file after it's been sent to the client
        
        Args:
            filepath (str): Path to the file to remove
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Cleaned up file: {filepath}")
            else:
                print(f"File not found for cleanup: {filepath}")
        except Exception as e:
            print(f"Error cleaning up file {filepath}: {str(e)}")
