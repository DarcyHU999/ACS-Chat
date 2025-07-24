from fastapi.middleware.cors import CORSMiddleware

def cors_allow_all():
    return CORSMiddleware(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 