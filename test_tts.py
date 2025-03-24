from gtts import gTTS
import os

def text_to_speech(text, lang="hi", output_file="output.mp3"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"TTS successfully generated: {output_file}")
    except Exception as e:
        print(f"Error in TTS: {e}")

if __name__ == "__main__":
    sample_text = "यह एक परीक्षण संदेश है।"
    text_to_speech(sample_text)
