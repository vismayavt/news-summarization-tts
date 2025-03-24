import requests
from bs4 import BeautifulSoup
from newspaper import Article
from transformers import pipeline
from gtts import gTTS
import os
import nltk

nltk.download("punkt")  # Required for article parsing

# Initialize Sentiment Analysis Pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

def scrape_news(company):
    search_url = f"https://news.google.com/search?q={company}&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for link in soup.select("article a[href]")[:10]:
        url = "https://news.google.com" + link["href"][1:]
        article = Article(url)

        try:
            article.download()
            article.parse()
            article.nlp()
            articles.append({
                "Title": article.title,
                "Summary": article.summary,
                "Text": article.text
            })
        except:
            continue

    return articles

def analyze_sentiment(articles):
    for article in articles:
        result = sentiment_pipeline(article["Summary"])[0]
        article["Sentiment"] = result["label"]
    return articles

def comparative_analysis(articles):
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    topic_keywords = {}

    for article in articles:
        sentiment_counts[article["Sentiment"]] += 1
        for word in article["Summary"].split():
            topic_keywords[word] = topic_keywords.get(word, 0) + 1

    sorted_topics = sorted(topic_keywords.items(), key=lambda x: x[1], reverse=True)
    common_topics = [word for word, _ in sorted_topics[:5]]

    return {
        "Sentiment Distribution": sentiment_counts,
        "Common Topics": common_topics
    }

def generate_hindi_tts(text):
    tts = gTTS(text, lang="hi")
    filename = "output.mp3"
    tts.save(filename)
    return filename

# ✅ Run the script with a test company
company_name = "Tesla"
articles = scrape_news(company_name)
articles = analyze_sentiment(articles)
insights = comparative_analysis(articles)

print("Sentiment Analysis:", articles)
print("Comparative Insights:", insights)

# ✅ Test Hindi TTS
audio_file = generate_hindi_tts("यह समाचार बहुत रोचक है।")
print(f"Generated Audio: {audio_file}")
