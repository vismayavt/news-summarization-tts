import os
from flask import Flask, jsonify, request
from gtts import gTTS  # Import gTTS for TTS

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Hugging Face!"  # Mapped to home route


@app.route("/news")
def get_news():
    company_name = request.args.get("company", "Tesla")

    # Generate dynamic TTS for the company
    text_to_speech(company_name)

    # Dummy data for articles, replace with actual logic to fetch news
    articles = [
        {"Title": f"News about {company_name}", "Summary": f"Some summary for {company_name}", "Sentiment": "Positive", "Topics": ["Technology", "Business"]},
    ]
    
    # Prepare response with audio file path and articles
    response = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {"positive": 70, "negative": 30},
        "TTS_Audio": f"/static/{company_name}_output.mp3"  # Path to the generated audio
    }

    return jsonify(response)

def text_to_speech(company_name):
    # Generate speech using gTTS (Google Text-to-Speech)
    text = f"Here is the latest news for {company_name}"
    tts = gTTS(text=text, lang='hi')  # Language set to Hindi (you can change it)
    
    # Define the path to save the TTS audio file
    audio_path = f"static/{company_name}_output.mp3"
    
    # Save the audio to a file
    tts.save(audio_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
