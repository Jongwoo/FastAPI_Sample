"""
FastAPI 메인 애플리케이션
ADR-0001, ADR-0002 준수
"""
import logging
from fastapi import FastAPI
from app.api import tasks

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# FastAPI 애플리케이션
app = FastAPI(
    title="Task Service API",
    description="ADR 기반 레이어드 아키텍처 Task API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(tasks.router)


@app.get("/", tags=["health"])
def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "service": "task-service",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
