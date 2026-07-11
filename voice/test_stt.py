from voice.speech_to_text import SpeechToText

stt = SpeechToText()

text = stt.transcribe("recording.wav")

print("\n========================")
print("Recognized Text")
print("========================")
print(text)