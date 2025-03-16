# FocusAI Document Simplification App - Frontend

This is the frontend application for the FocusAI document simplification service, designed to help people with dyslexia process and understand lengthy documents more easily.

## Features

- Upload documents in three formats:
  - PDF files
  - Plain text
  - Web page URLs
- View document chunks with an easy-to-navigate interface
- Dyslexia-friendly UI with appropriate fonts, colors, and spacing

## Prerequisites

- Python 3.8 or higher
- Backend API running at `http://localhost:8000` (see backend service documentation)

## Installation

1. Clone the repository (if you haven't already)
2. Navigate to the frontend directory:
   ```
   cd frontend
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Ensure the backend service is running
2. Start the Streamlit app:
   ```
   streamlit run app.py
   ```
3. Open your browser and go to `http://localhost:8501` to access the application

## Usage

1. Choose your preferred upload method (PDF, Text, or Web Page)
2. Upload your document or enter your text/URL
3. Click "Process" to send the document to the backend for processing
4. Navigate through the document chunks using the Previous and Next buttons
5. To start over, click the "Start Over" button

## Customization

You can modify the appearance of the app by editing the CSS in the `app.py` file.

## Troubleshooting

- If you encounter connection errors, ensure the backend service is running at the correct URL
- Check that all dependencies are installed correctly
- For PDF processing issues, ensure you have the necessary system dependencies for pdfplumber

## License

This project is licensed under the MIT License - see the LICENSE file for details. 