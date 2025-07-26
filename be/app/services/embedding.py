from app.config.embedding_config import get_embedding, is_embedding_ready
import os

def embedding_service_text(text: str):
    """
    Generate embedding vector for a given text.
    
    Args:
        text: The text to embed
        
    Returns:
        List of floats representing the embedding vector, or None if error
    """
    try:
        vector = get_embedding().embed_query(text)
        return vector
    except Exception as e:
        print(f"Error embedding text: {e}")
        return None




