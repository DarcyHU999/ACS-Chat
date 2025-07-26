import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

_embedding = None

def set_embedding():
    """
    Initialize OpenAI embeddings with API key from environment variables.
    """
    global _embedding
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable is not set")
    _embedding = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )

def get_embedding():
    """
    Get the initialized embedding instance.
    
    Returns:
        OpenAIEmbeddings instance
        
    Raises:
        Exception: If embedding is not ready
    """
    if not is_embedding_ready():
        raise Exception("Embedding is not ready")
    return _embedding

def is_embedding_ready():
    """
    Check if embedding is initialized and ready.
    
    Returns:
        bool: True if embedding is ready, False otherwise
    """
    return _embedding is not None

set_embedding()