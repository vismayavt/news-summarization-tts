import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS

def extract_news(company_name):
    """Scrapes news related to a company."""
    url = f"https://news.google.com/search?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = [a.text for a in soup.find_all("a", class_="DY5T1d", limit=5)]
    return headlines

def analyze_sentiment(text):
    """Performs sentiment analysis."""
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)
    return result[0]['label']

def generate_tts(text, filename="output.mp3"):
    """Converts text to speech and saves as an MP3 file."""
    tts = gTTS(text)
    tts.save(filename)
    return filename


