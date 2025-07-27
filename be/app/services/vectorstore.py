# vectorstore.py
import os
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config.embedding_config import get_embedding
from qdrant_client.models import VectorParams, Distance
from langchain_core.documents import Document

_vectorstore = None

def set_vectorstore():
    global _vectorstore
    try:
        # Use environment variable for Qdrant host, fallback to localhost for local development
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=qdrant_host, port=6333, check_compatibility=False)

        # Create QdrantVectorStore
        _vectorstore = QdrantVectorStore(
            client=client,
            collection_name="ACS-Chat",
            embedding=get_embedding(),
        )
    except Exception as e:
        print(f"Error setting up QdrantVectorStore: {e}")
        raise e

def is_vectorstore_ready():
    return _vectorstore is not None

def get_vectorstore():
    global _vectorstore
    if not is_vectorstore_ready():
        set_vectorstore()
    return _vectorstore

def search_vectorstore(query_vector: list[float], top_k: int, similarity_threshold: float = 0.3):
    """
    Search for similar documents using vector similarity.
    
    Args:
        query_vector: The query vector to search for
        top_k: Number of top results to return
        similarity_threshold: Minimum similarity score (0.0 to 1.0) for documents to be considered relevant
        
    Returns:
        List of Document objects with similar content
    """
    try:
        # Use Qdrant client directly for search
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=qdrant_host, port=6333, check_compatibility=False)
        search_results = client.search(
            collection_name="ACS-Chat",
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
            score_threshold=similarity_threshold
        )
        
        # Convert to LangChain Document format
        docs = []
        for result in search_results:
            doc = Document(
                page_content=result.payload.get("page_content", ""),
                metadata=result.payload.get("metadata", {})
            )
            docs.append(doc)
        
        return docs
    except Exception as e:
        print(f"Error searching vectorstore: {e}")
        return []

# Initialize vectorstore on first use
print("Vectorstore will be initialized on first use")
