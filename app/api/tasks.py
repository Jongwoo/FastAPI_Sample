# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

"""
Task API 엔드포인트
ADR-0001: domain 서비스에 의존하고 infra에는 직접 의존하지 않음
ADR-0002: 에러 응답은 표준 포맷 사용
"""
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.domain.models import Task, TaskCreate, TaskUpdate
from app.domain.services import TaskService
from app.domain.exceptions import TaskNotFoundException
from app.infra.repositories import TaskRepository
from app.api.error_responses import ErrorResponse

router = APIRouter()

# 의존성: 실제 프로덕션에서는 DI 컨테이너 사용 권장
_repository = TaskRepository()
_service = TaskService(_repository)


# API List:
# GET    /tasks       - 모든 Task 조회
# GET    /tasks/{id}  - 특정 Task 조회
# POST   /tasks       - Task 생성
# PUT    /tasks/{id}  - Task 수정
# DELETE /tasks/{id}  - Task 삭제


@router.get("", response_model=List[Task], summary="모든 Task 조회")
def get_all_tasks():
    """
    모든 Task를 조회합니다.
    InMemory 저장소에서 데이터를 가져옵니다.
    """
    return _service.get_all_tasks()


@router.get("/{task_id}", response_model=Task, summary="Task 조회")
def get_task(task_id: int):
    """
    ID로 특정 Task를 조회합니다.
    
    - **task_id**: 조회할 Task의 ID
    """
    try:
        return _service.get_task_by_id(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                errorCode="TASK_NOT_FOUND",
                message=str(e),
                details={"task_id": task_id}
            ).model_dump()
        )


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Task 생성")
def create_task(task_data: TaskCreate):
    """
    새로운 Task를 생성합니다.
    
    - **title**: Task 제목 (필수, 1-200자)
    - **description**: Task 설명 (선택)
    """
    return _service.create_task(task_data)


@router.put("/{task_id}", response_model=Task, summary="Task 수정")
def update_task(task_id: int, task_data: TaskUpdate):
    """
    기존 Task를 수정합니다.
    
    - **task_id**: 수정할 Task의 ID
    - **title**: 새로운 제목 (선택)
    - **description**: 새로운 설명 (선택)
    - **completed**: 완료 여부 (선택)
    """
    try:
        return _service.update_task(task_id, task_data)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                errorCode="TASK_NOT_FOUND",
                message=str(e),
                details={"task_id": task_id}
            ).model_dump()
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Task 삭제")
def delete_task(task_id: int):
    """
    Task를 삭제합니다.
    
    - **task_id**: 삭제할 Task의 ID
    """
    try:
        _service.delete_task(task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                errorCode="TASK_NOT_FOUND",
                message=str(e),
                details={"task_id": task_id}
            ).model_dump()
        )
