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
    app.run(debug=True)
