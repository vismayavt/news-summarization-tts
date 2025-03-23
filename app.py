import streamlit as st
import requests

st.title("📰 News Summarization & Sentiment Analysis")

# User input for company name
company = st.text_input("Enter a company name:", "")

if st.button("Fetch News"):
    if company:
        api_url = f"http://127.0.0.1:5000/news?company={company}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            st.write(f"### News for {data['company']}")
            
            for article in data["articles"]:
                st.subheader(article["title"])
                st.write(article["summary"])
                st.write(f"**Sentiment:** {article['sentiment']}")
                st.write(f"[Read More]({article['url']})")
                st.write("---")
        else:
            st.error("Error fetching news!")
    else:
        st.warning("Please enter a company name.")

if st.button("Generate Hindi Speech"):
    text = st.text_area("Enter text for Hindi speech conversion:")
    
    if text:
        api_url = "http://127.0.0.1:5000/tts"
        response = requests.post(api_url, json={"text": text})

        if response.status_code == 200:
            st.audio(response.content, format="audio/mp3")
        else:
            st.error("Error generating speech!")

