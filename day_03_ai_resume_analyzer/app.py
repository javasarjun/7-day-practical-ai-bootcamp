import streamlit as st

from llm_service import ask_ai
from resume_service import extract_resume_text
from resume_prompts import build_resume_analysis_prompt


st.set_page_config(
    page_title="Day 3 AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Day 3: AI Resume Analyzer")
st.write(
    "Upload a resume, optionally add a job description, and get AI-powered resume feedback."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("About This App")
st.sidebar.write(
    """
This app demonstrates a real AI application architecture:

User Interface → Resume Processing → Prompt Engineering → LLM → AI Report
"""
)

st.sidebar.markdown("---")
st.sidebar.subheader("Tips")
st.sidebar.write(
    """
For best results:
- Upload a clean PDF, TXT, or DOCX resume
- Add a job description for better matching
- Do not upload sensitive personal data in class demos
"""
)


# -----------------------------
# Resume Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt", "docx"],
)

manual_resume_text = st.text_area(
    "Or paste resume text manually",
    height=220,
    placeholder="Paste resume text here if you do not want to upload a file...",
)

job_description = st.text_area(
    "Optional: Paste a job description for matching",
    height=220,
    placeholder="Paste job description here...",
)


# -----------------------------
# Extract Resume Text
# -----------------------------

resume_text = ""

if uploaded_file is not None:
    try:
        resume_text = extract_resume_text(uploaded_file)
    except Exception as error:
        st.error(f"Could not extract resume text: {error}")

elif manual_resume_text.strip():
    resume_text = manual_resume_text.strip()


if resume_text:
    with st.expander("Preview Extracted Resume Text"):
        st.text(resume_text[:5000])

    st.caption(f"Extracted resume length: {len(resume_text)} characters")


# -----------------------------
# Analyze Resume
# -----------------------------

st.markdown("---")

analyze_button = st.button("Analyze Resume", type="primary")

if analyze_button:
    if not resume_text.strip():
        st.warning("Please upload a resume or paste resume text first.")
    else:
        # Limit text size for beginner lab stability.
        resume_text_for_ai = resume_text[:15000]
        job_description_for_ai = job_description[:8000]

        prompt = build_resume_analysis_prompt(
            resume_text=resume_text_for_ai,
            job_description=job_description_for_ai,
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful, honest, and practical career coach. "
                    "You help users improve resumes using only the information provided."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        with st.spinner("Analyzing resume..."):
            ai_response = ask_ai(messages)

        st.subheader("AI Resume Analysis")
        st.markdown(ai_response)

        st.download_button(
            label="Download Resume Analysis",
            data=ai_response,
            file_name="resume_analysis.md",
            mime="text/markdown",
        )


# -----------------------------
# Footer
# -----------------------------

st.markdown("---")
st.caption(
    "Day 3 Lab: This is an educational resume improvement tool, not an official hiring system."
)
