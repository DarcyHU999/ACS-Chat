# vectorstore.py
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.config.embedding_config import get_embedding
from qdrant_client.models import VectorParams, Distance
from langchain_core.documents import Document

_vectorstore = None

def init_qdrant_collection():
    """
    Ensure that the 'acs-chat' collection exists before QdrantVectorStore connects to it.
    """
    client = QdrantClient(host="localhost", port=6333, check_compatibility=False)
    collections = client.get_collections().collections
    if "acs-chat" not in [c.name for c in collections]:
        print("Creating collection: acs-chat")
        client.create_collection(
            collection_name="acs-chat",
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )
        print("Collection created successfully.")

def set_vectorstore():
    global _vectorstore
    try:
        init_qdrant_collection()  # Collection must exist first

        client = QdrantClient(host="localhost", port=6333, timeout=60, check_compatibility=False)

        _vectorstore = QdrantVectorStore(
            client=client,
            collection_name="acs-chat",
            embedding=get_embedding(),
        )

        print("Vectorstore is ready.")
    except Exception as e:
        print(f"Error setting up QdrantVectorStore: {e}")
        raise e

def is_vectorstore_ready():
    return _vectorstore is not None

def get_vectorstore():
    global _vectorstore
    if not is_vectorstore_ready():
        print("Vectorstore not ready, initializing...")
        set_vectorstore()
    return _vectorstore

def search_vectorstore(query_vector: list[float], top_k: int, similarity_threshold: float = 0.4):
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
        print(f"Searching with query vector length: {len(query_vector)}")
        print(f"Query vector first 5 values: {query_vector[:5]}")
        print(f"Similarity threshold: {similarity_threshold}")
        
        # Use Qdrant client directly for search
        client = QdrantClient(host="localhost", port=6333, check_compatibility=False)
        search_results = client.search(
            collection_name="acs-chat",
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
            score_threshold=similarity_threshold
        )
        
        # Convert to LangChain Document format and show scores
        docs = []
        for result in search_results:
            doc = Document(
                page_content=result.payload.get("page_content", ""),
                metadata=result.payload.get("metadata", {})
            )
            docs.append(doc)
            print(f"Document score: {result.score:.4f}")
        
        print(f"Found {len(docs)} documents with similarity >= {similarity_threshold}")
        return docs
    except Exception as e:
        print(f"Error searching vectorstore: {e}")
        return []

# Ensure vectorstore is initialized at import time
set_vectorstore()
