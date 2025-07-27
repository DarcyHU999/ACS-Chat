# vectorstore.py
import os
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
    # Use environment variable for Qdrant host, fallback to localhost for local development
    import os
    qdrant_host = os.getenv("QDRANT_HOST", "localhost")
    client = QdrantClient(host=qdrant_host, port=6333, check_compatibility=False)
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

        # Use environment variable for Qdrant host, fallback to localhost for local development
        import os
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=qdrant_host, port=6333, timeout=60, check_compatibility=False)

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
        import os
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=qdrant_host, port=6333, check_compatibility=False)
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

# Initialize vectorstore with retry logic for Docker environment
def initialize_with_retry(max_retries=5, delay=2):
    """Initialize vectorstore with retry logic for Docker environment"""
    import time
    import os
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to initialize vectorstore (attempt {attempt + 1}/{max_retries})")
            set_vectorstore()
            print("Vectorstore initialized successfully!")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Vectorstore initialization failed.")
                raise e

# Initialize with retry for Docker environment
if os.getenv("QDRANT_HOST") == "qdrant":
    # In Docker environment, use retry logic
    initialize_with_retry()
else:
    # In local development, initialize immediately
    set_vectorstore()
