import streamlit as st
import requests

st.title("📢 News Summarization & TTS App")

company_name = st.text_input("Enter Company Name:", "Tesla")

if st.button("Analyze News"):
    response = requests.get(f"http://127.0.0.1:5000/news?company={company_name}")
    if response.status_code == 200:
        data = response.json()

        st.write(f"### Company: {data['Company']}")

        for article in data["Articles"]:
            st.subheader(article["Title"])
            st.write(f"📝 **Summary:** {article['Summary']}")
            st.write(f"📌 **Sentiment:** {article['Sentiment']}")
            st.write(f"🏷️ **Topics:** {', '.join(article['Topics'])}")

        st.subheader("📊 Comparative Sentiment Analysis")
        st.json(data["Comparative Sentiment Score"])

        st.subheader("🔊 Hindi Text-to-Speech")
        st.audio("static/output.mp3")
