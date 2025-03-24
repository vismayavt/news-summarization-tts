import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from keybert import KeyBERT
from gtts import gTTS
import os
from collections import Counter

# News Scraper using BeautifulSoup
def fetch_news(company_name):
    search_url = f"https://www.bing.com/news/search?q={company_name}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("a", class_="title", limit=10):
        title = item.text
        url = item["href"]
        articles.append({"Title": title, "Content": url})
    
    return articles

# Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    if not text:
        return "No summary available."
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]["summary_text"]

# Sentiment Analysis Model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    if not text:
        return "Neutral"
    sentiment = sentiment_pipeline(text)[0]["label"]
    return "Positive" if sentiment == "POSITIVE" else "Negative"

# Topic Extraction using KeyBERT
kw_model = KeyBERT()

def extract_topics(text):
    if not text:
        return []
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words="english")
    return [kw[0] for kw in keywords[:5]]

# Comparative Sentiment Analysis
def compare_sentiments(articles):
    sentiments = [article["Sentiment"] for article in articles]
    sentiment_counts = Counter(sentiments)

    return {
        "Sentiment Distribution": dict(sentiment_counts),
        "Coverage Differences": [
            {
                "Comparison": f"Article {i+1} vs Article {i+2}",
                "Impact": "Different perspectives on company performance"
            }
            for i in range(len(articles)-1)
        ]
    }

# Hindi Text-to-Speech


def text_to_speech_hindi(text):
    from gtts import gTTS

    # Ensure the 'static/' directory exists
    output_dir = "static"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create 'static/' if missing

    # Generate and save speech
    tts = gTTS(text=text, lang="hi")
    output_path = os.path.join(output_dir, "output.mp3")
    tts.save(output_path)

    return output_path  # Return path for Flask to serve
