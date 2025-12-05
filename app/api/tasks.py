# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

# API List:
# /tasks GET: 모든 Task 조회 (지금은 InMemory 저장소로 충분)
# /tasks POST: Task 생성

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional

from ..domain.task_service import TaskService
from ..domain.task_models import Task, TaskCreateRequest
from ..infra.task_repository_impl import InMemoryTaskRepository

router = APIRouter(prefix="/tasks", tags=["tasks"])

# 의존성 주입 (ADR-0001: API 레벨에서 구체 구현을 생성하여 서비스에 주입)
task_repository = InMemoryTaskRepository()
task_service = TaskService(task_repository)

# Error Handler (ADR-0002: 표준 에러 응답 포맷)
def create_error_response(error_code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = {
        "errorCode": error_code,
        "message": message
    }
    if details:
        response["details"] = details
    return response

@router.get("/", response_model=list[Task])
async def get_tasks():
    """
    모든 Task 조회
    """
    try:
        return task_service.get_all_tasks()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=create_error_response(
                "INTERNAL_SERVER_ERROR",
                "Failed to retrieve tasks",
                {"error": str(e)}
            )
        )

@router.post("/", response_model=Task)
async def create_task(task_data: TaskCreateRequest):
    """
    Task 생성
    """
    try:
        return task_service.create_task(task_data.title, task_data.description)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                "INVALID_INPUT",
                str(e),
                {"field": "title"}
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=create_error_response(
                "INTERNAL_SERVER_ERROR",
                "Failed to create task",
                {"error": str(e)}
            )
        )
