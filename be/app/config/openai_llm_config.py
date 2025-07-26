import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# 全局变量
_openai_llm = None

def setup_openai_llm():
    global _openai_llm
    _openai_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        max_tokens=1024,
        timeout=30,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
    )

def get_openai_llm():
    return _openai_llm

def is_openai_llm_ready():
    return _openai_llm is not None

setup_openai_llm()