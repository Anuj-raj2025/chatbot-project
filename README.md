# 🤖 AI-Powered Customer Support Chatbot

A simple NLP chatbot for customer support FAQs.

**Tech stack:** Python, NLTK, scikit-learn (TF-IDF), Flask, SQLite, HTML/CSS/JS

## Features
- Understands questions written in different ways (NLTK cleaning + TF-IDF cosine similarity)
- Remembers the previous question for follow-ups (e.g. "how long does it take?")
- Small talk (hello / thanks / bye) and a fallback reply
- Saves every conversation (message, reply, intent, confidence) in SQLite
- Chat history restored on page refresh
- `/logs` page to view all interaction logs

## Project structure
```
chatbot-project/
├── app.py            # Flask server + routes
├── chatbot.py        # NLP logic
├── database.py       # SQLite functions
├── faqs.json         # Questions and answers (edit this!)
├── requirements.txt
├── templates/        # index.html (chat), logs.html (logs)
└── static/           # style.css, script.js
```

## How to run
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## API
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/chat` | Send `{"session_id": null, "message": "..."}` and get the reply |
| GET | `/history/<session_id>` | Past messages of a session |
| GET | `/logs` | Logs table page |

## Customize
Add or edit entries in `faqs.json`, then restart the app.
