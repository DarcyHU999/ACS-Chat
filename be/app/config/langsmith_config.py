import os
from dotenv import load_dotenv
from langsmith import Client
from langchain.callbacks import LangChainTracer

# 加载环境变量
load_dotenv()

# 全局变量
_langsmith_client = None
_langsmith_tracer = None
_langsmith_enabled = False

def setup_langsmith():
    global _langsmith_client, _langsmith_tracer, _langsmith_enabled
    
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project_name = os.getenv("LANGCHAIN_PROJECT")
    endpoint = os.getenv("LANGCHAIN_ENDPOINT")
    
    if api_key:
        # 直接使用从 .env 加载的值，不需要重新设置
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
    """获取LangSmith客户端"""
    return _langsmith_client

def get_langsmith_tracer():
    """获取LangChain追踪器"""
    return _langsmith_tracer

def is_langsmith_enabled():
    """检查LangSmith是否启用"""
    return _langsmith_enabled

# 初始化
setup_langsmith() 