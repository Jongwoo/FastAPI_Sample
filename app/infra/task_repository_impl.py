# === ADR CONTEXT (DO NOT EDIT) ===
# 이 파일은 ARCH/ADR-0001-layered-architecture.md, ARCH/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.
# === END ADR CONTEXT ===

# 아래부터 실제 구현부. LLM은 이 영역만 수정한다.
# === IMPLEMENTATION START ===

from typing import List, Dict
from datetime import datetime
from ..domain.task_repository import TaskRepository
from ..domain.task_models import Task

class InMemoryTaskRepository(TaskRepository):
    """InMemory Task Repository 구현 (ADR-0001: 구체 구현은 infra에)"""
    
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
    
    def get_all(self) -> List[Task]:
        """모든 Task를 조회한다."""
        return list(self._tasks.values())
    
    def create(self, title: str, description: str) -> Task:
        """새로운 Task를 생성한다."""
        task_id = self._next_id
        now = datetime.now().isoformat()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )
        self._tasks[task_id] = task
        self._next_id += 1
        return task
