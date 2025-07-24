from app.config.openai_llm_config import get_openai_llm, is_openai_llm_ready
from langchain_core.messages import HumanMessage


def llm_service(history: list, new_message: str):
    try:
        if not is_openai_llm_ready():
            raise Exception("OpenAI LLM is not ready")
        llm = get_openai_llm()
        for chunk in llm.stream(history + [HumanMessage(content=new_message)]):
            yield chunk.content

    except Exception as e:
        raise Exception(f"Error in llm_service: {str(e)}")