# FocusAI: Dyslexia Reading Assistance Tool

FocusAI is a web application designed to help dyslexic individuals read and comprehend documents more easily. The application processes text from various sources (PDFs, plain text, or web pages), summarizes it into digestible chunks, and provides text-to-speech functionality for easier consumption.

## Features

- Multiple input options: PDF documents, text input, and web URLs
- Text summarization for easier reading
- Text-to-speech functionality for audio playback of content
- Chunking of content for progressive reading
- User-friendly interface designed for accessibility

## Project Structure

```
FocusAI/
├── frontend/               # Frontend web application
│   ├── components/         # Reusable UI components
│   ├── pages/              # Page layouts
│   └── styles/             # CSS styles
├── backend/                # Python backend
│   ├── api/                # API endpoints
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions and helpers
│   └── config/             # Configuration files
└── data/                   # Data storage
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FocusAI.git
cd FocusAI
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
python -m backend.app
```

4. Open the frontend in a web browser:
```bash
streamlit run C:\Users\qc_de\OneDrive\Desktop\FocusAI\frontend\app.py
```

## API Endpoints

- `/api/text` - Process text input
- `/api/pdf` - Process PDF documents
- `/api/web` - Process web URLs
- `/api/tts` - Convert text to speech

## Technologies Used

- **Backend**: Python, FastAPI, LangChain, PyTorch, Llama.cpp
- **Frontend**: HTML, CSS, JavaScript
- **Text Processing**: Transformers, Beautiful Soup
- **Document Handling**: PyPDF2
- **Text-to-Speech**: pyttsx3
