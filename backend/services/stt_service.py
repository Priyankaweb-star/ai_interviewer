from faster_whisper import WhisperModel
import os

# Load model once (important for speed)
model = WhisperModel(
    "base",
    device="cpu",        # or "cuda" if you have GPU
    compute_type="int8"  # good for CPU + Windows
)

def transcribe_audio(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found")

    segments, info = model.transcribe(audio_path)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()
