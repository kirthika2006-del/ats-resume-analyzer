# ATS Resume & Career Fit Analyzer

An AI-powered chatbot that analyzes a resume (PDF) against a job description and gives an ATS-style match score, missing keywords, and improvement suggestions.

## Tech Stack
- Flask (backend)
- Groq API (LLM - llama-3.3-70b-versatile)
- ChromaDB (vector store for RAG)
- Firebase Firestore (save analysis history)
- PyPDF2 (resume text extraction)

## Setup

1. Create virtual environment
```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # Mac/Linux
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Configure `.env`
```
GROQ_API_KEY=your_groq_api_key_here
FIREBASE_CRED_PATH=firebase-credentials.json
```
- Get a free Groq API key from https://console.groq.com
- Download your Firebase service account JSON and place it in the project root as `firebase-credentials.json`

4. Run the app
```
python app.py
```

5. Open in browser
```
http://127.0.0.1:5000
```

## How it works
1. User uploads a resume PDF and pastes a job description.
2. Resume text is extracted using PyPDF2.
3. Both resume and JD text are chunked and stored in ChromaDB.
4. Relevant context is retrieved (RAG) and sent along with the resume + JD to Groq's LLM.
5. The LLM returns a match score, missing keywords, and improvement suggestions.
6. Result is saved to Firestore and displayed on the page.

## Notes
- `firebase-credentials.json` should NEVER be committed to Git — add it to `.gitignore`.
- Free tier Groq API has rate limits; if you hit errors, wait a few seconds and retry.
