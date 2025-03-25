from flask import Flask, request, jsonify, url_for
import requests
from textblob import TextBlob
from gtts import gTTS
import os
import time
from transformers import pipeline
from deep_translator import GoogleTranslator  # ✅ Fix: Import translator

app = Flask(__name__)

# ✅ NewsAPI Configuration
NEWS_API_KEY = "fb0bd4003cfb42a9b7a65d4b57656c5b"  # Replace with your actual API key
NEWS_API_URL = "https://newsapi.org/v2/everything"

# ✅ Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_news(company):
    """Fetch top 5 news articles for a given company"""
    params = {
        "q": company,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5  # Fetch only 5 articles
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def summarize_text(text):
    """Summarize text using Hugging Face transformer"""
    summary = summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)
    return summary[0]["summary_text"] if summary else ""

def analyze_sentiment(text):
    """Perform sentiment analysis using TextBlob"""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    label = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"
    return {"label": label, "score": round(polarity, 2)}

def generate_tts(text, lang="hi"):
    """Generate Hindi text-to-speech audio"""
    try:
        # ✅ Step 1: Translate the text
        translated_text = GoogleTranslator(source="auto", target=lang).translate(text)
        if not translated_text.strip():
            raise ValueError("Translation failed: Empty text returned.")

        print(f"✅ Translated Text: {translated_text}")

        # ✅ Step 2: Generate TTS audio
        tts = gTTS(text=translated_text, lang=lang, slow=False)

        # ✅ Step 3: Ensure the static directory exists
        static_dir = os.path.join(os.getcwd(), "static")
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # ✅ Step 4: Save the audio file
        filename = f"output_{int(time.time())}.mp3"
        file_path = os.path.join(static_dir, filename)
        tts.save(file_path)

        print(f"✅ Audio saved at: {file_path}")
        return filename  # ✅ Return the filename (not full path)

    except Exception as e:
        print(f"❌ Error generating TTS: {e}")
        return None

# ✅ Flask API Endpoints

@app.route("/fetch_news", methods=["POST"])
def get_news():
    """Fetch news articles for a given company"""
    data = request.json
    company = data.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = fetch_news(company)
    return jsonify({"articles": articles})

@app.route("/news", methods=["POST"])
def process_news():
    """Summarize the given news text"""
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    summary = summarize_text(text)
    return jsonify({"summary": summary})

@app.route("/sentiment", methods=["POST"])
def get_sentiment():
    """Analyze the sentiment of the text"""
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    sentiment = analyze_sentiment(text)
    return jsonify(sentiment)

@app.route("/tts", methods=["POST"])
def text_to_speech():
    """Generate Hindi speech from given text"""
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    tts_file = generate_tts(text)
    if tts_file:
        # ✅ Generate the URL for the saved audio file
        audio_url = url_for("static", filename=tts_file, _external=True)
        return jsonify({"audio_url": audio_url})
    else:
        return jsonify({"error": "Failed to generate speech"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
