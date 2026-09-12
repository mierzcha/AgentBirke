from src.stt.whisper_client import WhisperClient


client = WhisperClient()

text = client.transcribe(
    "data/audio/test_piper_client2.wav" #temp
)

print("Erkannter Text:")
print(text)
