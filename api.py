import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:5002"

st.title("📰 News Analysis & Hindi TTS")

# ---- FETCH NEWS ARTICLES ---- #
st.header("🔎 Fetch News Articles")
company_name = st.text_input("Enter company name:")

if st.button("Fetch News"):
    if company_name.strip():
        with st.spinner(f"Fetching news about {company_name}..."):
            response = requests.post(f"{API_URL}/fetch_news", json={"company": company_name})

        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                st.success(f"Fetched {len(articles)} articles related to {company_name}.")
                for i, article in enumerate(articles):
                    st.subheader(f"📰 Article {i+1}")
                    st.write(f"**Title:** {article['title']}")
                    st.write(f"**Description:** {article.get('description', 'No description available.')}")
                    st.write(f"[Read More]({article['url']})")

                    # ---- SUMMARIZATION ---- #
                    summary_text = article.get("content", article.get("description", ""))
                    if summary_text:
                        with st.spinner("Summarizing article..."):
                            summary_response = requests.post(f"{API_URL}/news", json={"text": summary_text})

                        if summary_response.status_code == 200:
                            summary = summary_response.json().get("summary", "No summary available.")
                            st.success("**Summary:**")
                            st.write(summary)

                            # ---- SENTIMENT ANALYSIS ---- #
                            with st.spinner("Analyzing sentiment..."):
                                sentiment_response = requests.post(f"{API_URL}/sentiment", json={"text": summary})

                            if sentiment_response.status_code == 200:
                                sentiment_data = sentiment_response.json()
                                sentiment_label = sentiment_data["label"]
                                sentiment_score = sentiment_data["score"]

                                if sentiment_label == "POSITIVE":
                                    st.success(f"😊 **Sentiment:** {sentiment_label} ({sentiment_score:.2f})")
                                elif sentiment_label == "NEGATIVE":
                                    st.error(f"😞 **Sentiment:** {sentiment_label} ({sentiment_score:.2f})")
                                else:
                                    st.warning(f"😐 **Sentiment:** {sentiment_label} ({sentiment_score:.2f})")

                            # ---- TTS (Hindi) ---- #
                            with st.spinner("Generating Hindi speech..."):
                                tts_response = requests.post(f"{API_URL}/tts", json={"text": summary, "lang": "hi"})

                            if tts_response.status_code == 200:
                                audio_url = tts_response.json().get("audio_url", "")
                                if audio_url:
                                    st.audio(audio_url, format="audio/mp3")
                                else:
                                    st.error("Error generating Hindi speech.")
                            else:
                                st.error("Error generating Hindi speech.")
                        else:
                            st.error("Error in summarization.")
            else:
                st.warning("No news articles found.")
        else:
            st.error("Failed to fetch news articles.")
    else:
        st.warning("Please enter a company name.")
