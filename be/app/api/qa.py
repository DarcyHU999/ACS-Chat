from hmac import new
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel  
from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.services.llm import llm_service


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
    try:
        history = req.history
        new_message = req.message
        configed_history = []
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
            try:
                for chunk in llm_service(configed_history, new_message):
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