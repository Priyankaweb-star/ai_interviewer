import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="AI Interviewer", layout="wide")

st.title("🎤 AI-Driven Automated Interviewer")

# -------------------- Upload Slide --------------------
st.header("📽️ Upload Project Slide / Screenshot")
slide = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

ocr_text = ""
if slide:
    with st.spinner("Extracting content..."):
        res = requests.post(
            f"{API_BASE}/upload-slide/",
            files={"file": slide}
        )
        ocr_text = res.json()["extracted_text"]

    st.subheader("🧠 Extracted Content")
    st.text_area("OCR Output", ocr_text, height=150)

# -------------------- Upload Audio --------------------
st.header("🎙️ Upload Presentation Audio")
audio = st.file_uploader("Upload audio", type=["wav", "mp3"])

transcript = ""
if audio:
    with st.spinner("Transcribing speech..."):
        res = requests.post(
            f"{API_BASE}/upload-audio/",
            files={"file": audio}
        )
        transcript = res.json()["transcript"]

    st.subheader("📝 Transcript")
    st.text_area("Speech Text", transcript, height=150)

# -------------------- Generate Questions --------------------
if ocr_text and transcript:
    if st.button("🤖 Generate Interview Questions"):
        res = requests.post(
            f"{API_BASE}/generate-questions/",
            json={
                "ocr_text": ocr_text,
                "transcript": transcript
            }
        )

        questions = res.json()["questions"]
        st.subheader("❓ AI Interview Questions")
        st.write(questions)

# -------------------- Evaluation --------------------
st.header("📊 Evaluation")

student_answer = st.text_area("Student Answer")

if st.button("📈 Evaluate Performance"):
    res = requests.post(
        f"{API_BASE}/evaluate/",
        json={
            "project_context": ocr_text,
            "student_answer": student_answer
        }
    )

    st.subheader("🏆 Score & Feedback")
    st.write(res.json()["evaluation"])
