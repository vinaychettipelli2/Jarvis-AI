from voice.microphone import MicrophoneManager

mic = MicrophoneManager()

print("Devices:")

mic.list_devices()

print("\nRecording for 5 seconds...")

audio = mic.record(seconds=5)

mic.save(audio)

print("\nFinished.")
print("File saved as recording.wav")