# 🤖 AI-Powered Customer Support Chatbot

An intelligent chatbot that answers customer-support FAQs using **Natural Language Processing (NLP)**.
It understands questions written in different ways, remembers the previous question for follow-ups,
and stores every conversation in a database for analysis.

## 🚀 Features
- **NLP-based understanding**: text is cleaned with NLTK (tokenization, stop-word removal, stemming) and matched using **TF-IDF + cosine similarity**
- **Contextual replies**: follow-up questions like *"how long does it take?"* use the previous question as context
- **Small talk & fallback**: handles greetings, thanks, goodbye, and gives a helpful reply when it does not understand
- **Interaction logs**: every message, reply, detected intent and confidence score is saved in **SQLite**
- **Chat history**: conversation is restored when the page is refreshed
- **Logs dashboard**: view all interactions in a table at `/logs`
- **Easy to customize**: add new questions and answers in `faqs.json`, no retraining needed

## 🛠️ Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python |
| NLP | NLTK, scikit-learn (TF-IDF, cosine similarity) |
| Backend | Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

## 📁 Project Structure
```
chatbot-project/
├── app.py            # Flask server and routes
├── chatbot.py        # NLP logic (preprocessing, matching, context)
├── database.py       # SQLite functions for logs and history
├── faqs.json         # Knowledge base (questions and answers)
├── requirements.txt  # Python dependencies
├── templates/        # index.html (chat UI), logs.html (logs page)
└── static/           # style.css, script.js
```

## ⚙️ Installation & Setup
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/chatbot-project.git
cd chatbot-project

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

## 🔌 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send `{"session_id": null, "message": "How do I get a refund?"}` and receive the bot reply, intent and confidence |
| `GET` | `/history/<session_id>` | Get past messages of a session |
| `GET` | `/logs` | View all interaction logs |

**Example response**
```json
{
  "session_id": "a1b2c3...",
  "reply": "You can return items within 30 days of delivery for a full refund...",
  "intent": "refund_policy",
  "confidence": 0.74
}
```

## 🧠 How It Works
1. The user's message is cleaned: lowercase, tokenize, remove stop-words, stem (NLTK).
2. The message is converted into a TF-IDF vector and compared with all example questions using cosine similarity.
3. If the best match is above the confidence threshold, the answer of that FAQ is returned.
4. For short follow-up questions, the previous question is added to the message to keep context.
5. If nothing matches, a polite fallback reply is sent.
6. Every interaction is saved in SQLite (`chat_logs` table).

## ✏️ Customize the Chatbot
Open `faqs.json` and add a new entry:
```json
{
  "intent": "store_location",
  "questions": ["Where is your store?", "Do you have a physical shop?"],
  "answer": "Our store is located at ..."
}
```
Restart the app and the bot will answer the new questions.

## 🔮 Future Improvements
- Use Transformer-based sentence embeddings for better understanding
- Add user feedback (👍 / 👎) to improve answers
- Multi-language support
- Deploy on Render / Railway

## 👤 Author
**Your Name**
GitHub: [@your-username](https://github.com/your-username)
