from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-mpnet-base-v2")

def embed(text: str):
    """Turn text into a 768-dimensional vector."""
    return _model.encode(text).tolist()
