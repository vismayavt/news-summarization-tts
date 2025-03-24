import requests
from transformers import pipeline
import os

# Initialize Hugging Face models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")

# NewsAPI Key (Replace with your actual key)
NEWS_API_KEY = "fb0bd4003cfb42a9b7a65d4b57656c5b"  # 🔹 Replace with a valid API key
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

        if response.status_code != 200 or data.get("status") != "ok":
            return None, f"Error: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return None, "No articles found."

        # Extract content from the first 5 articles
        news_text = " ".join(
            [article.get("description", "") or article.get("content", "") for article in articles if article.get("description")]
        ).strip()

        if not news_text:
            return None, "No relevant content found in articles."

        return news_text, None  # 🔹 Return news text and no error

    except Exception as e:
        return None, f"Exception occurred: {str(e)}"

def summarize_text(text):
    """Summarize the given text"""
    try:
        return summarizer(text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
    except Exception as e:
        return f"Summarization failed: {str(e)}"

def analyze_sentiment(text):
    """Perform sentiment analysis on summarized text"""
    try:
        return sentiment_analyzer(text)[0]
    except Exception as e:
        return f"Sentiment analysis failed: {str(e)}"

def generate_tts(text):
    """Generate text-to-speech and save as an audio file"""
    try:
        audio_path = "output.mp3"
        os.system(f'echo "{text}" | festival --tts')  # Dummy command, replace with TTS model
        return audio_path
    except Exception as e:
        return f"TTS generation failed: {str(e)}"
