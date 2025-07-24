from langchain_openai import OpenAIEmbeddings

_embedding = None

def set_embedding():
    global _embedding
    _embedding = OpenAIEmbeddings(model="text-embedding-3-small")

def get_embedding():
    if not is_embedding_ready():
        raise Exception("Embedding is not ready")
    return _embedding

def is_embedding_ready():
    return _embedding is not None