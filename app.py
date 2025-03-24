from flask import Flask, request, jsonify
from utils import fetch_news, summarize_text, analyze_sentiment, generate_tts

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "News Summarization API is running!"})

@app.route("/news", methods=["POST"])
def get_news():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    news_text, error = fetch_news(query)
    if error:
        return jsonify({"error": error}), 500

    summary = summarize_text(news_text)
    sentiment = analyze_sentiment(summary)

    return jsonify({
        "summary": summary,
        "sentiment": sentiment
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)


