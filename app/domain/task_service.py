# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

from typing import List
from .task_repository import TaskRepository
from .task_models import Task

class TaskService:
    """Task 도메인 서비스 (ADR-0001: api 레이어에서 domain 서비스에 의존)"""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def get_all_tasks(self) -> List[Task]:
        """모든 Task를 조회한다."""
        return self.repository.get_all()
    
    def create_task(self, title: str, description: str) -> Task:
        """새로운 Task를 생성한다."""
        if not title or len(title.strip()) == 0:
            raise ValueError("Task title cannot be empty")
        return self.repository.create(title, description)
