from flask import Blueprint, request, send_file, jsonify
from backend.services.tts_service import TTSService

tts_api = Blueprint('tts_api', __name__)
tts_service = TTSService()

@tts_api.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        language = data.get('language', 'en')  # Default to English if no language specified

        # Generate speech file
        audio_file_path = tts_service.generate_speech(text, language)

        # Send the file
        response = send_file(
            audio_file_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='speech.mp3'
        )

        # Clean up the file after sending
        @response.call_on_close
        def cleanup():
            tts_service.cleanup_file(audio_file_path)

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500
