from flask import Flask, request, jsonify
import requests
from textblob import TextBlob
from gtts import gTTS
import os
import time
from transformers import pipeline
from deep_translator import GoogleTranslator

app = Flask(__name__)

# NewsAPI Configuration
NEWS_API_KEY = "fb0bd4003cfb42a9b7a65d4b57656c5b"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def fetch_news(company):
    params = {
        "q": company,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt"
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])[:5]  # Fetch only the first 5 articles
    return []


def summarize_text(text):
    summary = summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"] if summary else ""


def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    label = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"
    return {"label": label, "score": round(polarity, 2)}


def generate_tts(text, lang="hi"):
    translated_text = GoogleTranslator(source='auto', target='hi').translate(text)  # Translate to Hindi
    tts = gTTS(text=translated_text, lang=lang, slow=False)
    filename = f"static/output_{int(time.time())}.mp3"
    tts.save(filename)
    return filename


@app.route("/fetch_news", methods=["POST"])
def get_news():
    data = request.json
    company = data.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = fetch_news(company)
    return jsonify({"articles": articles})


@app.route("/news", methods=["POST"])
def process_news():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    summary = summarize_text(text)
    return jsonify({"summary": summary})


@app.route("/sentiment", methods=["POST"])
def get_sentiment():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    sentiment = analyze_sentiment(text)
    return jsonify(sentiment)


@app.route("/tts", methods=["POST"])
def text_to_speech():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    tts_file = generate_tts(text)
    return jsonify({"audio_url": tts_file})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)

