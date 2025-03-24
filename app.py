import streamlit as st
import requests

st.set_page_config(page_title="News Summarization & Hindi TTS", layout="wide")

# Title of the App
st.title("📰 News Summarization & Hindi TTS")

# Input box for the company name
company = st.text_input("Enter Company Name", "")

if st.button("Fetch News"):
    if company:
        with st.spinner("Fetching news..."):
            # Call the API (ensure Flask backend is running)
            response = requests.get(f"http://127.0.0.1:8000/fetch_news?company={company}")

            
            if response.status_code == 200:
                data = response.json()
                
                # Display Sentiment Analysis
                st.subheader("Sentiment Analysis")
                for article in data["news"]["articles"]:
                    st.write(f"**Title:** {article['title']}")
                    st.write(f"**Summary:** {article['summary']}")
                    st.write(f"**Sentiment:** {article['sentiment']}")
                    st.write("---")
                
                # Display Audio
                st.subheader("🔊 Hindi Speech Output")
                st.audio(data["audio"], format="audio/mp3")
            else:
                st.error("Failed to fetch news. Try again later!")
    else:
        st.warning("Please enter a company name.")

