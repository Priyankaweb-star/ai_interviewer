from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil

# Services
from backend.services.ocr_service import extract_text_from_image
from backend.services.interview_agent import generate_interview_questions
from backend.services.scoring_agent import evaluate_student
from backend.services.stt_service import transcribe_audio

app = FastAPI(title="AI-Driven Automated Interviewer")

# -------------------- Directories --------------------
UPLOAD_DIR = "data/uploads"
AUDIO_DIR = "data/audio"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# -------------------- Models --------------------
class InterviewInput(BaseModel):
    ocr_text: str
    transcript: str

class EvaluationInput(BaseModel):
    project_context: str
    student_answer: str

# -------------------- Routes --------------------
@app.get("/")
def root():
    return {"status": "AI Interviewer running 🚀"}

# ---------- OCR ----------
@app.post("/upload-slide/")
async def upload_slide(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_image(file_path)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text
    }

# ---------- STT ----------
@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    file_path = os.path.join(AUDIO_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(file_path)

    return {
        "filename": file.filename,
        "transcript": transcript
    }

# ---------- Interview Question Generator ----------
@app.post("/generate-questions/")
def generate_questions(data: InterviewInput):
    questions = generate_interview_questions(
        data.ocr_text,
        data.transcript
    )
    return {
        "questions": questions
    }

# ---------- Evaluation & Scoring ----------
@app.post("/evaluate/")
def evaluate(data: EvaluationInput):
    evaluation = evaluate_student(
        data.project_context,
        data.student_answer
    )
    return {
        "evaluation": evaluation
    }

class AnswerRequest(BaseModel):
    answer: str

@app.post("/evaluate-answer")
def evaluate_answer(data: AnswerRequest):
    feedback = generate_interview_questions(
        role="Student Project",
        level="Interview",
        skills=data.answer
    )
    return {
        "answer": data.answer,
        "feedback": feedback
    }