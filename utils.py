import requests
from bs4 import BeautifulSoup
import nltk
from newspaper import Article
from transformers import pipeline
import gtts
import os

nltk.download('punkt')

# Sentiment Analysis Model
sentiment_pipeline = pipeline("sentiment-analysis")

def extract_news(company):
    """Extracts news articles using Google News (Limited scraping workaround)."""
    query = company.replace(" ", "+")  # Encode spaces for search URL
    url = f"https://news.google.com/search?q={query}&hl=en&gl=US&ceid=US:en"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch news: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for link in soup.find_all('a', href=True)[:10]:  # Extract up to 10 articles
        href = link["href"]
        
        # Fix Google News URL format
        if href.startswith("./articles/"):
            article_url = "https://news.google.com" + href[1:]
        elif href.startswith("http"):
            article_url = href  # Sometimes Google links to external sites
        else:
            continue

        # Use newspaper3k to extract full text
        article = Article(article_url)
        try:
            article.download()
            article.parse()
            article.nlp()

            articles.append({
                "title": article.title,
                "summary": article.summary,
                "text": article.text,
                "url": article_url
            })
        except Exception as e:
            print(f"Skipping article due to error: {e}")
            continue

    return articles
def get_news_articles(company_name):
    """Fetches news articles, performs sentiment analysis, and structures the output."""
    news_articles = extract_news(company_name)
    
    for article in news_articles:
        article["sentiment"] = analyze_sentiment(article["text"])

    return news_articles


def compare_sentiments(articles):
    """Perform sentiment comparison across multiple articles."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment = article.get("sentiment", "Neutral")  # Default to Neutral if missing
        sentiment_counts[sentiment] += 1

    return sentiment_counts

    

def generate_tts(text, filename="output.mp3"):
    """Convert text to Hindi speech using Google TTS."""
    try:
        tts = gtts.gTTS(text=text, lang="hi")
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"TTS generation failed: {e}")
        return None
