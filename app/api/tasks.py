# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

# API List:
# /tasks GET: 모든 Task 조회 (InMemory 저장소 사용)
# /tasks POST: Task 생성

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.domain.models import Task
from app.domain.service import TaskService
from app.domain.exceptions import TaskNotFoundError, InvalidTaskDataError
from app.api.error_responses import ErrorResponse
from app.infra.in_memory_repository import InMemoryTaskRepository

logger = logging.getLogger(__name__)

# Router 설정
router = APIRouter(prefix="/tasks", tags=["tasks"])

# ADR-0001: API 레벨에서 구체 구현(InMemoryTaskRepository)을 주입
_task_repository = InMemoryTaskRepository()
_task_service = TaskService(_task_repository)


def get_task_service() -> TaskService:
    """TaskService 의존성"""
    return _task_service


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid task data"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
def create_task(
    task: Task,
    service: TaskService = Depends(get_task_service)
) -> Task:
    """
    Task 생성
    
    ADR-0001: domain 서비스를 통해 비즈니스 로직 처리
    ADR-0002: 에러 발생 시 표준 포맷으로 응답
    """
    try:
        return service.create_task(task)
    except InvalidTaskDataError as e:
        # ADR-0002: {"errorCode", "message", "details"} 포맷
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "errorCode": e.error_code,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "errorCode": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {}
            }
        )


@router.get(
    "",
    response_model=List[Task],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
def get_all_tasks(
    service: TaskService = Depends(get_task_service)
) -> List[Task]:
    """
    모든 Task 조회
    
    ADR-0001: domain 서비스를 통해 데이터 조회
    """
    try:
        return service.get_all_tasks()
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "errorCode": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {}
            }
        )


@router.get(
    "/{task_id}",
    response_model=Task,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> Task:
    """
    특정 Task 조회
    
    ADR-0002: Task 없을 때 표준 에러 포맷으로 응답
    """
    try:
        return service.get_task_by_id(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "errorCode": e.error_code,
                "message": e.message,
                "details": {"taskId": task_id}
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "errorCode": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {}
            }
        )
