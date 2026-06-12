import streamlit as st
import os
import warnings
import logging
import pandas as pd

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

from src.pdf_reader import extract_text
from src.summarizer import generate_summary
from src.health_score import generate_health_score
from src.chatbot import ask_question
from src.report_compare import compare_reports
from src.pdf_generator import create_pdf
from src.rag_engine import create_rag_index

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="MedIntel AI+",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "report_text" not in st.session_state:
    st.session_state.report_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "health_score" not in st.session_state:
    st.session_state.health_score = ""

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = ""
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🏥 MedIntel AI+")

    st.markdown("---")

    st.subheader("📌 Features")

    st.success("Medical Report Analysis")
    st.success("AI Summary")
    st.success("Health Score Prediction")
    st.success("RAG Medical Assistant")
    st.success("PDF Report Download")
    st.success("Report Comparison")

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏥 MedIntel AI+")
st.subheader("RAG Based Medical Report Analyzer")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs("data/reports", exist_ok=True)

    save_path = os.path.join(
        "data/reports",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully")

    if st.button("Analyze Report"):

     with st.spinner("Analyzing Report..."):

        report_text = extract_text(save_path)

        chunks = create_rag_index(
            report_text
        )

        st.success(
            f"RAG Index Created with {chunks} chunks"
        )

        summary = generate_summary(
            report_text
        )

        health_score = generate_health_score(
            report_text
        )

        st.session_state.report_text = report_text
        st.session_state.summary = summary
        st.session_state.health_score = health_score
        st.session_state.analysis_done = True

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if st.session_state.analysis_done:

    st.markdown("---")

    # SUMMARY

    st.subheader("📋 Summary")

    st.write(
        st.session_state.summary
    )

    st.markdown("---")

    # HEALTH SCORE

    st.subheader("📊 Health Score")

    st.write(
        st.session_state.health_score
    )

    score = 75

    try:

        import re

        numbers = re.findall(
            r"\d+",
            str(st.session_state.health_score)
        )

        if numbers:
            score = int(numbers[0])

    except:
        pass

    st.progress(score / 100)

    chart_df = pd.DataFrame(
        {
            "Health Score": [score]
        }
    )

    st.bar_chart(chart_df)

    st.markdown("---")

    # PDF DOWNLOAD

    st.subheader("📥 Download Summary")

    try:

        pdf_path = create_pdf(
            st.session_state.summary
        )

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="📄 Download Summary PDF",
                data=pdf_file,
                file_name="summary.pdf",
                mime="application/pdf"
            )

    except Exception as e:

        st.error(
            f"PDF Generation Error: {e}"
        )

    st.markdown("---")

    # RAG ASSISTANT

    st.subheader("💬 RAG Medical Assistant")

    question = st.text_input(
        "Ask about your report",
        key="rag_question"
    )

if st.button("Ask Question"):

    if question.strip():

        try:

            st.session_state.rag_answer = ask_question(
                st.session_state.report_text,
                question
            )

        except Exception as e:

            st.session_state.rag_answer = f"Error: {e}"

if st.session_state.rag_answer:

    st.success(
        st.session_state.rag_answer
    )

    st.markdown("---")

    # REPORT COMPARISON

    st.subheader("📈 Report Comparison")

    col1, col2 = st.columns(2)

    with col1:

        previous_score = st.number_input(
            "Previous Score",
            min_value=0,
            max_value=100,
            value=65
        )

    with col2:

        current_score = st.number_input(
            "Current Score",
            min_value=0,
            max_value=100,
            value=75
        )

    if st.button("Compare Reports"):

        result = compare_reports(
            previous_score,
            current_score
        )

        st.success(result)

        comparison_df = pd.DataFrame(
            {
                "Score": [
                    previous_score,
                    current_score
                ]
            },
            index=[
                "Previous",
                "Current"
            ]
        )

        st.bar_chart(comparison_df)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <center>
        <h3>🏥 MedIntel AI+</h3>
        <p>AI Powered Medical Report Analyzer</p>
        <p>Built with Gemini AI + ChromaDB + RAG</p>
        <b>Developed by Gokul Prasad M.S</b>
    </center>
    """,
    unsafe_allow_html=True
)