import requests

API_URL = "http://127.0.0.1:5000/news"
response = requests.post(API_URL, json={"url": "https://example.com"})
print(response.status_code)
print(response.text)
