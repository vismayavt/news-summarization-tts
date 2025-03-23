from flask import Flask, request, jsonify
from utils import extract_news, analyze_sentiment, generate_tts

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the News API!"})

@app.route("/news", methods=["GET"])
def get_news():
    company_name = request.args.get("company")  # Get company name from URL
    if not company_name:
        return jsonify({"error": "Please provide a company name"}), 400
    
    news = extract_news(company_name)
    return jsonify(news)

@app.route("/sentiment", methods=["POST"])
def sentiment_analysis():
    data = request.json
    text = data.get("text", "")
    sentiment = analyze_sentiment(text)  # Make sure analyze_sentiment() exists in utils.py
    return jsonify({"sentiment": sentiment})

@app.route("/tts", methods=["POST"])
def text_to_speech():
    data = request.json
    text = data.get("text", "")
    filename = generate_tts(text)  # Make sure generate_tts() exists in utils.py
    return jsonify({"audio_file": filename})
print(app.url_map)


if __name__ == "__main__":
    app.run(debug=True)
