"""Flask web app: serves the chat page and the chatbot API."""
import uuid

from flask import Flask, jsonify, render_template, request

import database
from chatbot import ChatBot

app = Flask(__name__)
database.init_db()
bot = ChatBot("faqs.json")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id") or uuid.uuid4().hex

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    last_question = database.get_last_question(session_id)
    reply, intent, confidence = bot.get_reply(message, last_question)
    database.save_chat(session_id, message, reply, intent, confidence)

    return jsonify({"session_id": session_id, "reply": reply, "intent": intent,
                    "confidence": round(confidence, 2)})


@app.route("/history/<session_id>")
def history(session_id):
    return jsonify(database.get_history(session_id))


@app.route("/logs")
def logs():
    return render_template("logs.html", logs=database.get_all_logs())


if __name__ == "__main__":
    app.run(debug=True)
