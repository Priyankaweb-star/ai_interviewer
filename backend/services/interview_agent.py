import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_interview_questions(ocr_text: str, transcript: str) -> str:
    prompt = f"""
You are a technical interviewer.

Project Content:
{ocr_text}

Student Explanation:
{transcript}

Ask 2 technical questions and 1 follow-up question.
"""

    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    data = res.json()

    # 🔐 Safety check
    if "response" not in data:
        raise RuntimeError(f"Ollama returned unexpected response: {data}")

    return data["response"].strip()
