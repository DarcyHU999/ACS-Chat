from app.config.embedding_config import get_embedding, is_embedding_ready

def embedding_service():
    if not is_embedding_ready():
        raise Exception("Embedding is not ready")
    vector = get_embedding().embed_query('how are you? I am fine, thank you!')
    print(f"Embedding: {vector}")
    return vector

# Only run if this module is executed directly
if __name__ == "__main__":
    embedding_service()