# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

from fastapi import FastAPI
from .api.tasks import router as tasks_router

app = FastAPI(
    title="Task Service",
    description="Simple Task Management API following ADR guidelines",
    version="1.0.0"
)

# API 라우터 등록
app.include_router(tasks_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Task Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
