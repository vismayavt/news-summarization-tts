from gtts import gTTS
import os

# Input text
text = "Hello, this is a test of the TTS functionality!"

# Initialize gTTS engine
tts = gTTS(text=text, lang='en')

# Save audio to a file
tts.save("output.mp3")

# Play the audio file
os.system("start output.mp3")
