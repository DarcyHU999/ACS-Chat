from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.langsmith_middleware import LangSmithMiddleware
from app.api import qa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LangSmithMiddleware)

app.include_router(qa.router, prefix="/api/v1")

