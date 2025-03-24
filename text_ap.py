import requests

url = "http://127.0.0.1:5001/news"
data = {"query": "Apple"}

response = requests.post(url, json=data)
print(response.json())  # Print the API response
