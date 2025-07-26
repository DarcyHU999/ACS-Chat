from hmac import new
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  
from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.services.llm import llm_service
from app.chains.qa_chain import qa_chain
from app.services.vectorize_documents import embedding_service_file
import inspect

class HistoryMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class QARequest(BaseModel):
    history: list[HistoryMessage]
    message: str

class QAResponse(BaseModel):
    answer: str

router = APIRouter()

@router.post("/qa")
async def qa(req: QARequest):
    """
    Question-answering endpoint that processes user messages and returns streaming responses.
    
    Args:
        req: QARequest containing conversation history and new message
        
    Returns:
        StreamingResponse with generated answer chunks
    """
    try:
        # embedding_service_file("/Users/darcy/Desktop/target_cleaned")
        history = req.history
        new_message = req.message
        configed_history = []
        
        # Convert history to LangChain message format
        for hist in history:
            if hist.role == "system":
                configed_history.append(SystemMessage(content=hist.content))
            elif hist.role == "user":
                configed_history.append(HumanMessage(content=hist.content))
            elif hist.role == "assistant":
                configed_history.append(AIMessage(content=hist.content))
            else:
                raise HTTPException(status_code=400, detail="Invalid role") 

        configed_history.append(HumanMessage(content=new_message))
        
        async def generate_response():
            """
            Generate streaming response from QA chain.
            """
            try:
                # Get the generator from qa_chain
                gen = qa_chain(configed_history, new_message)
                
                # Check if it's an async generator or regular generator
                if inspect.isasyncgen(gen):
                    # Handle async generator (normal LLM response)
                    async for chunk in gen:
                        yield f"{chunk}"
                else:
                    # Handle regular generator (content irrelevant response)
                    for chunk in gen:
                        yield f"{chunk}"
                        
            except Exception as e:
                yield f"data: error: {str(e)}"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))