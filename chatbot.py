"""NLP part of the chatbot: NLTK text cleaning + TF-IDF similarity matching."""
import json
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.30  # minimum similarity needed to trust an answer

SMALL_TALK = [
    ("greeting", r"^(hi|hello|hey|good (morning|afternoon|evening))\b", "Hello! 👋 How can I help you today?"),
    ("thanks", r"\b(thanks|thank you|thx)\b", "You're welcome! Anything else I can help with?"),
    ("goodbye", r"\b(bye|goodbye|see you)\b", "Goodbye! Have a great day 😊"),
]


def load_stopwords():
    try:
        return set(stopwords.words("english"))
    except LookupError:
        try:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))
        except Exception:
            return {"a", "an", "the", "is", "are", "to", "of", "in", "i", "my", "me", "you", "do", "can", "it"}


class ChatBot:
    def __init__(self, faq_file="faqs.json"):
        self.tokenizer = RegexpTokenizer(r"[a-z0-9]+")
        self.stemmer = PorterStemmer()
        self.stop_words = load_stopwords()

        with open(faq_file, encoding="utf-8") as f:
            self.faqs = json.load(f)

        # Flatten: every example question points back to its FAQ
        self.examples, self.owner = [], []
        for i, faq in enumerate(self.faqs):
            for q in faq["questions"]:
                self.examples.append(self.clean(q))
                self.owner.append(i)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.examples)

    def clean(self, text):
        """lowercase -> tokenize -> remove stopwords -> stem"""
        words = self.tokenizer.tokenize(text.lower())
        words = [w for w in words if w not in self.stop_words] or words
        return " ".join(self.stemmer.stem(w) for w in words)

    def best_match(self, text):
        vec = self.vectorizer.transform([self.clean(text)])
        scores = cosine_similarity(vec, self.matrix)[0]
        best = int(scores.argmax())
        return self.faqs[self.owner[best]], float(scores[best])

    def get_reply(self, message, last_question=None):
        """Returns (reply, intent, confidence)."""
        # 1. small talk
        if len(message.split()) <= 6:
            for intent, pattern, reply in SMALL_TALK:
                if re.search(pattern, message.lower()):
                    return reply, intent, 1.0

        # 2. FAQ matching
        faq, score = self.best_match(message)

        # 3. context: short follow-up like "how long does it take?" -> add previous question
        if score < THRESHOLD and last_question and len(message.split()) <= 5:
            faq2, score2 = self.best_match(last_question + " " + message)
            if score2 > score:
                faq, score = faq2, score2

        if score >= THRESHOLD:
            return faq["answer"], faq["intent"], score

        # 4. fallback
        return ("Sorry, I didn't understand that. Could you rephrase? "
                "You can also email support@shopeasy.example."), "fallback", score
