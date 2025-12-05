"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from app.api import tasks

app = FastAPI(title="Task Management API", version="1.0.0")

# API 라우터 등록
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/")
def root():
    return {"message": "Task Management API"}
