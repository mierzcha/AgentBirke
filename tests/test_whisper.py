from src.stt.whisper_client import WhisperClient

client = WhisperClient()
text = client.transcribe("data/audio/test_audio_for_whisper.wav")
print("Erkannter Text von test_audio_for_whisper.wav:")
print(text)
print("----------------------------------------------")

text = client.transcribe("data/audio/test_audio_for_whisper2.wav")
print("Erkannter Text von test_audio_for_whisper2.wav:")
print(text)
