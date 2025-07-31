from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.langsmith_middleware import LangSmithMiddleware
from app.api import qa
import os

app = FastAPI()

# Secure CORS configuration
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    f"http://{os.getenv('FRONTEND_HOST', 'localhost')}:3000",
]

# If a specific domain is specified, add it to the allowed list
frontend_domain = os.getenv('FRONTEND_DOMAIN')
if frontend_domain:
    allowed_origins.append(f"http://{frontend_domain}")
    allowed_origins.append(f"https://{frontend_domain}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Restrict to specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit HTTP methods
    allow_headers=["*"],
)

app.add_middleware(LangSmithMiddleware)

app.include_router(qa.router, prefix="/api/v1")

