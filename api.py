from utils import fetch_news, summarize_text, analyze_sentiment, extract_topics, compare_sentiments, text_to_speech_hindi

def generate_output(company_name):
    articles = fetch_news(company_name)

    for article in articles:
        article["Summary"] = summarize_text(article["Content"])
        article["Sentiment"] = analyze_sentiment(article["Content"])
        article["Topics"] = extract_topics(article["Content"])

    sentiment_comparison = compare_sentiments(articles)

    final_report = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": sentiment_comparison,
        "Final Sentiment Analysis": f"{company_name}’s latest news coverage is mostly positive."
    }

    text_to_speech_hindi(final_report["Final Sentiment Analysis"])

    return final_report
