import os
from dotenv import load_dotenv
from langsmith import Client
from langchain.callbacks import LangChainTracer

# Load environment variables
load_dotenv()

# Global variables
_langsmith_client = None
_langsmith_tracer = None
_langsmith_enabled = False

def setup_langsmith():
    global _langsmith_client, _langsmith_tracer, _langsmith_enabled
    
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project_name = os.getenv("LANGCHAIN_PROJECT")
    endpoint = os.getenv("LANGCHAIN_ENDPOINT")
    
    if api_key:
        # Directly use values loaded from .env, no need to reset
        _langsmith_client = Client(api_key=api_key, api_url=endpoint)
        _langsmith_tracer = LangChainTracer(project_name=project_name)
        _langsmith_enabled = True
        
        print("LangSmith tracing enabled")
        return True
    else:
        print("Warning: LANGCHAIN_API_KEY not found, LangSmith tracing disabled")
        _langsmith_enabled = False
        return False

def get_langsmith_client():
    """Get LangSmith client"""
    return _langsmith_client

def get_langsmith_tracer():
    """Get LangChain tracer"""
    return _langsmith_tracer

def is_langsmith_enabled():
    """Check if LangSmith is enabled"""
    return _langsmith_enabled

setup_langsmith() 