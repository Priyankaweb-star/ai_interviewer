import requests

def evaluate_student(project_context, student_answer):
    prompt = f"""
Evaluate the student.

Project Context:
{project_context}

Student Answer:
{student_answer}

Give scores (0-10) for:
- Technical Depth
- Clarity
- Originality
- Implementation Understanding
Provide feedback.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
