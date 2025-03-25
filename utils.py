import requests
from transformers import pipeline
from gtts import gTTS  # ✅ Proper TTS
import os

# ✅ Initialize Hugging Face models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")

# ✅ NewsAPI Key (Replace with your actual key)
NEWS_API_KEY = "fb0bd4003cfb42a9b7a65d4b57656c5b"  # Replace with a valid API key
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(query):
    """Fetch news articles from NewsAPI.org"""
    try:
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 5  # Fetch top 5 articles
        }
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()

        # ✅ Check if response is valid
        if response.status_code != 200 or "articles" not in data:
            return [], f"Error: {data.get('message', 'Unknown error')}"  # ✅ Return empty list instead of string

        articles = data.get("articles", [])
        if not articles:
            return [], "No articles found."  # ✅ Ensure it returns a list, not a string

        return articles, None  # ✅ Now it always returns a **list** and an error message if needed

    except Exception as e:
        return [], f"Exception occurred: {str(e)}"  # ✅ Return empty list on error


def chunk_text(text, chunk_size=1024):
    """✅ Split text into smaller chunks for summarization"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text):
    """Summarize the given text"""
    try:
        chunks = chunk_text(text)  # ✅ Handle long texts
        summaries = [summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]["summary_text"] for chunk in chunks]
        return " ".join(summaries)
    except Exception as e:
        return f"Summarization failed: {str(e)}"

def analyze_sentiment(text):
    """Perform sentiment analysis on summarized text"""
    try:
        return sentiment_analyzer(text[:512])[0]  # ✅ Truncate to avoid exceeding model limit
    except Exception as e:
        return f"Sentiment analysis failed: {str(e)}"

def generate_tts(text, lang="hi"):
    """✅ Generate text-to-speech and save as an audio file"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_path = "static/output.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        return f"TTS generation failed: {str(e)}"
