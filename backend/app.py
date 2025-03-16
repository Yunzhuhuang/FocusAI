from flask import Flask
from flask_cors import CORS

# Import API routes
# Comment out other routes for now until we implement them
from backend.api.tts_api import tts_api
from backend.api.text_api import text_api
from backend.api.pdf_api import pdf_api
from backend.api.web_api import web_api
from backend.api.gamify import gamify_api

# Create Flask app
app = Flask(__name__)

# Configure CORS
CORS(app)

# Register blueprints
# Only register tts_api for now
app.register_blueprint(tts_api, url_prefix='/api/tts')
app.register_blueprint(text_api, url_prefix='/api/text')
app.register_blueprint(pdf_api, url_prefix='/api/pdf')
app.register_blueprint(web_api, url_prefix='/api/web')
app.register_blueprint(gamify_api, url_prefix='/api/gamify')
@app.route("/")
def root():
    """
    Root endpoint that returns basic API information
    """
    return {
        "message": "Welcome to FocusAI API",
        "version": "1.0.0",
        "endpoints": [
            "/api/tts - Convert text to speech"
        ]
    }

if __name__ == "__main__":
    # Run the application
    app.run(host="0.0.0.0", port=8000, debug=True)
