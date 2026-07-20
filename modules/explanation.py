import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_explanation_model():
    """Create a Gemini client lazily so app startup stays fast.
    """
    """
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        # api_key = os.getenv("GEMINI_API_KEY")
    """
    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )
    st.write("API key loaded:", bool(api_key))
    
    # api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    try:
        from google import genai
    except ImportError as exc:
        raise ImportError(
            "Could not import the Gemini SDK. Install the supported "
            "'google-genai' package with: pip install -U google-genai"
        ) from exc

    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def generate_explanation(
    resume_text,
    jd_text,
    matched_skills,
    missing_skills,
    overall_score
):

    prompt = f"""
You are an expert ATS recruiter.

Analyze the following Resume and Job Description.

Resume:
{resume_text}

Job Description:
{jd_text}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Overall Match Score:
{overall_score}

Return the response in Markdown with these sections:

## Overall Assessment

## Strengths

## Matched Skills

## Missing Skills

## Suggestions for Improvement

## ATS Recommendation

## Suggest improvements to maximize ATS score.

## Rewrite the Professional Summary.

## Suggest missing projects.

## Suggest certifications.

Keep the response concise and professional.
"""

    client = get_explanation_model()
    # gemini-1.5-flash has been retired. This stable model supports text
    # generation through the Gemini API's generateContent endpoint.
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        text = response.text
    except Exception as exc:
        return (
            "### Gemini explanation unavailable\n\n"
            f"The request to `{model_name}` failed: `{exc}`\n\n"
            "Check that the API key is active and that its project has Gemini API quota."
        )
    finally:
        if hasattr(client, "close"):
            client.close()

    return getattr(response, "text", None) or "Gemini did not return an explanation."
