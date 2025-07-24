from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.middleware.langsmith_middleware import LangSmithMiddleware
from app.api import qa
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加LangSmith中间件
app.add_middleware(LangSmithMiddleware)

app.include_router(qa.router, prefix="/api/v1")
