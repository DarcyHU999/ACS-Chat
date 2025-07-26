from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.langsmith_config import get_langsmith_client, is_langsmith_enabled, _langsmith_tracer
import time
import json

class LangSmithMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 只对聊天API进行追踪
        if request.url.path == "/api/v1/qa" and request.method == "POST":
            if is_langsmith_enabled():
                try:
                    body = await request.body()
                    request_data = json.loads(body)
                    
                    client = get_langsmith_client()
                    if client:
                        run = client.create_run(
                            project_name=_langsmith_tracer.project_name,
                            name="qa_request",
                            inputs={
                                "history": request_data.get("history", []),
                                "new_message": request_data.get("new_message", "")
                            },
                            start_time=start_time
                        )
                        request.state.langsmith_run_id = run.id
                        
                except Exception as e:
                    print(f"Error logging to LangSmith: {e}")
        
        response = await call_next(request)
        
        # 更新运行记录
        if hasattr(request.state, 'langsmith_run_id'):
            if is_langsmith_enabled():
                try:
                    client = get_langsmith_client()
                    if client:
                        client.update_run(
                            run_id=request.state.langsmith_run_id,
                            end_time=time.time(),
                            outputs={"duration": time.time() - start_time}
                        )
                except Exception as e:
                    print(f"Error updating LangSmith run: {e}")
        
        return response 