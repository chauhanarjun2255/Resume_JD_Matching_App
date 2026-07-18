import streamlit as st
from modules.jd_parser import parse_jd
from modules.resume_parser import extract_resume
from modules.skill_extractor import extract_skills
from modules.similarity import calculate_similarity
from modules.scoring import (
    skill_match_score,
    experience_score,
    education_score,
    final_score,
    similarity_level
)
from modules.explanation import generate_explanation
from modules.dashboard import create_gauge
import plotly.express as px
import pandas as pd
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume JD Matcher",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("AI Resume Matcher")

st.sidebar.markdown("""
### Features

✅ Resume Upload

✅ Job Description

✅ AI Matching

✅ Skill Analysis

✅ Match Score

✅ Suggestions
""")

st.sidebar.info(
"""
Supported Files

✔ PDF

✔ DOCX

✔ TXT
"""
)

st.sidebar.success("AI Model Ready")

with st.expander("About This Tool"):

    st.write("""
This AI Resume Matcher uses

• NLP

• Sentence Transformers

• Gemini AI

• ATS-style Scoring

to compare resumes with job descriptions.
""")


# -----------------------------
# Main Title
# -----------------------------
st.title("🤖 AI Resume - JD Matching Tool")

st.write(
    "Upload your Resume and Job Description."
)

st.divider()

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns(2)

# -----------------------------
# Resume Upload
# -----------------------------
with left:

    st.subheader("📄 Upload Resume")

    uploaded_resume = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx", "txt"]
    )

# -----------------------------
# Job Description
# -----------------------------
with right:

    st.subheader("📝 Job Description")

    uploaded_jd = st.file_uploader(
        "Choose Job Description",
        type=["pdf", "docx", "txt"]
    )

st.divider()

# -----------------------------
# Analyze Button
# -----------------------------
analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# -----------------------------
# Result
# -----------------------------
if analyze:

    if uploaded_resume is None:
        st.error("Please upload a Resume.")

    elif uploaded_jd is None:
        st.error("Please upload a Job Description.")

    else:

        # -------------------------
        # Step 1: Parse Resume
        # -------------------------
        resume_text = extract_resume(uploaded_resume)

        # -------------------------
        # Step 2: Parse JD
        # -------------------------
        if uploaded_jd:
            jd_text = extract_resume(uploaded_jd)
            clean_jd = parse_jd(jd_text)

        # -------------------------
        # Step 3: Extract Skills
        # -------------------------
        col1, col2 = st.columns(2)
        
        with col1:
            resume_skills = extract_skills(resume_text)
        
        with col2:
            jd_skills = extract_skills(clean_jd)

        # -------------------------
        # Step 4: Compare Skills
        # -------------------------
        matched = sorted(list(set(resume_skills) & set(jd_skills)))
        missing = sorted(list(set(jd_skills) - set(resume_skills)))
        extra = sorted(list(set(resume_skills) - set(jd_skills)))

        # -------------------------
        # Step 5: Calculate Semantic Similarity
        #-------------------------
        with st.spinner("Loading AI model and comparing documents..."):
            semantic_score = calculate_similarity(
                resume_text,
                clean_jd
            )
        
        # -------------------------
        # Step 6: Display Results
        # -------------------------
        st.subheader("Resume Skills")
        st.write(resume_skills)

        st.subheader("JD Skills")
        st.write(jd_skills)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("✅ Matched Skills")
            st.write(matched)
            
            st.subheader("🧠 AI Semantic Similarity")

            st.metric(
                label="Semantic Similarity",
                value=f"{semantic_score}%"
            )
            st.progress(min(int(semantic_score), 100))
            

        with col2:
            st.warning("❌ Missing Skills")
            st.write(missing)
            
            skill_score = skill_match_score(
                resume_skills,
                jd_skills
            )

            exp_score = experience_score(
                resume_text,
                clean_jd
            )

            edu_score = education_score(
                resume_text,
                clean_jd
            )

            overall_score = final_score(
                skill_score,
                semantic_score,
                exp_score,
                edu_score
            )
            
        with col3:
            st.info("✅ Extra Skills")
            st.write(extra)
            
            st.divider()

            st.header("🎯 Final AI Match Score")

            st.metric(
                label="Overall Score",
                value=f"{overall_score}%"
            )

            st.progress(min(int(overall_score), 100))
                    
        st.subheader("🎯 AI Match Analysis")

        fig = create_gauge(overall_score)

        st.plotly_chart(fig, use_container_width=True)
        
        df = pd.DataFrame({

            "Category": [
                "Matched",
                "Missing",
                "Extra"
            ],

            "Count": [
                len(matched),
                len(missing),
                len(extra)
            ]
        })

        fig = px.bar(
            df,
            x="Category",
            y="Count",
            text="Count"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("✅ Matched Skills")

        for skill in matched:
            st.success(skill)
        
        st.subheader("❌ Missing Skills")

        for skill in missing:
            st.error(skill)
            
        st.subheader("📌 Additional Skills")

        for skill in extra:
            st.info(skill)
        
        st.subheader("📊 AI Match Analysis")
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Skill Match",
            f"{skill_score}%"
        )

        c2.metric(
            "Semantic",
            f"{semantic_score}%"
        )

        c3.metric(
            "Experience",
            f"{exp_score}%"
        )

        c4.metric(
            "Education",
            f"{edu_score}%"
        )
        
        st.subheader("🧠 AI Semantic Similarity")
        level = similarity_level(semantic_score)
        st.success(level)

        if overall_score >= 90:

            st.success("⭐⭐⭐⭐⭐ Highly Recommended")

        elif overall_score >= 80:

            st.success("⭐⭐⭐⭐ Recommended")

        elif overall_score >= 70:

            st.warning("⭐⭐⭐ Good Match")

        else:

            st.error("Needs Resume Improvement")
            
        strength = len(matched)

        if strength >= 10:
            st.success("Excellent Technical Profile")

        elif strength >= 6:
            st.info("Good Technical Profile")

        else:
            st.warning("Needs More Relevant Skills")


        # Generate AI explanation
        explanation = generate_explanation(
            resume_text,
            clean_jd,
            matched,
            missing,
            overall_score
        )

        st.subheader("🤖 Gemini AI Explanation")
        st.markdown(explanation)

                
