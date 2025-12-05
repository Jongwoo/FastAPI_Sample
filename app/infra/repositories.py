"""
인프라 계층 - 데이터 저장소 구현
현재는 InMemory 저장소로 구현
"""
from typing import List, Optional, Dict
from app.domain.models import Task


class TaskRepository:
    """Task 저장소 인터페이스 및 InMemory 구현"""
    
    def __init__(self):
        self._storage: Dict[int, Task] = {}
        self._next_id = 1
    
    def find_all(self) -> List[Task]:
        """모든 Task 조회"""
        return list(self._storage.values())
    
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """ID로 Task 조회"""
        return self._storage.get(task_id)
    
    def save(self, task: Task) -> Task:
        """Task 저장"""
        if task.id is None:
            task.id = self._next_id
            self._next_id += 1
        self._storage[task.id] = task
        return task
    
    def update(self, task: Task) -> Task:
        """Task 업데이트"""
        if task.id in self._storage:
            self._storage[task.id] = task
        return task
    
    def delete(self, task_id: int) -> None:
        """Task 삭제"""
        if task_id in self._storage:
            del self._storage[task_id]
