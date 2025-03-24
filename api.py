from flask import Flask, request, jsonify
from utils import get_news_articles, compare_sentiments, generate_tts

app = Flask(__name__)

@app.route('/fetch_news', methods=['GET'])
def fetch_news():
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400
    
    articles = get_news_articles(company)
    sentiment_analysis = compare_sentiments(articles)
    summary_text = f"{company} के समाचारों का विश्लेषण किया गया।"
    
    audio_file = generate_tts(summary_text)
    
    response = {
        "company": company,
        "news": sentiment_analysis,
        "audio": audio_file
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
