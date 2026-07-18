import streamlit as st


@st.cache_resource(show_spinner=False)
def get_similarity_model():
    """Load the embedding model once per Streamlit server process."""
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Semantic similarity dependencies are missing. Install the project requirements "
            "and ensure torchvision is available."
        ) from exc

    return SentenceTransformer("all-MiniLM-L6-v2", device="cpu")


def calculate_similarity(resume_text, jd_text):
    """
    Returns semantic similarity score (0–100)
    """

    model = get_similarity_model()

    # One batched inference call is faster than encoding each document separately.
    embeddings = model.encode(
        [resume_text, jd_text],
        normalize_embeddings=True,
        show_progress_bar=False,
        batch_size=32,
    )
    similarity = float(embeddings[0] @ embeddings[1])

    return round(similarity * 100, 2)
