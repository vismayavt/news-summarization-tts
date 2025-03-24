import streamlit as st
import requests

st.title("📢 News Summarization & TTS App")

company_name = st.text_input("Enter Company Name:", "Tesla")

if st.button("Analyze News"):
    url = f"http://127.0.0.1:5001/news?company={company_name}"  # Adjust Flask API URL

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        st.write(f"### Company: {data.get('Company', 'N/A')}")
        for article in data.get('Articles', []):
            st.subheader(article.get("Title", "No Title"))
            st.write(f"📝 **Summary:** {article.get('Summary', 'No Summary')}")
            st.write(f"📌 **Sentiment:** {article.get('Sentiment', 'N/A')}")
            st.write(f"🏷️ **Topics:** {', '.join(article.get('Topics', []))}")

        # Display Comparative Sentiment Score
        st.subheader("📊 Comparative Sentiment Analysis")
        st.json(data.get('Comparative Sentiment Score', {}))

        # Play the TTS audio for the company
        audio_file = data.get('TTS_Audio', None)
        if audio_file:
            st.subheader("🔊 Hindi Text-to-Speech")
            st.audio(audio_file)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching data: {e}")
