from flask import Flask, request, jsonify
from utils import fetch_news, summarize_text, analyze_sentiment, generate_tts
import traceback

app = Flask(__name__)

@app.route('/news', methods=['POST'])
def get_news():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Fetch news articles from NewsAPI
        news_content, error = fetch_news(query)
        if error:
            return jsonify({"error": error}), 500

        # Summarize the extracted news
        summary = summarize_text(news_content)

        # Perform sentiment analysis
        sentiment = analyze_sentiment(summary)

        # Convert summarized text to speech
        audio_path = generate_tts(summary)

        return jsonify({
            "summary": summary,
            "sentiment": sentiment,
            "audio": audio_path
        })

    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())  # 🔹 Log full traceback for debugging
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "News Summarization API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)


