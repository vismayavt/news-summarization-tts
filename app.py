import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Hugging Face!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))  # Get PORT from environment
    app.run(host='0.0.0.0', port=port)  # Run on 0.0.0.0 to be accessible externally
