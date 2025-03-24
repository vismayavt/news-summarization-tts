import os
from flask import Flask, request, jsonify
from api import generate_output

app = Flask(__name__)

@app.route('/news', methods=['GET'])
def get_news():
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400
    
    output = generate_output(company)
    return jsonify(output)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))  # Get the PORT from the environment
    app.run(host='0.0.0.0', port=port)  # Run Flask without debug mode
