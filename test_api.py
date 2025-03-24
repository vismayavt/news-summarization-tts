import requests

NEWS_API_KEY = "fb0bd4003cfb42a9b7a65d4b57656c5b"  # Your API key
NEWS_API_URL = "https://newsapi.org/v2/everything"

query = "Apple"

params = {
    "q": query,
    "apiKey": NEWS_API_KEY,
    "language": "en",
    "pageSize": 5
}

print("🔹 Sending request to NewsAPI...")

response = requests.get(NEWS_API_URL, params=params)

print(f"🔹 Status Code: {response.status_code}")
print(f"🔹 Response JSON: {response.json()}")  # Print full response
