"""
도메인 서비스 계층
ADR-0001: 비즈니스 로직을 처리하며, infra 레이어의 리포지토리를 사용
"""
from typing import List, Optional
from datetime import datetime
from app.domain.models import Task, TaskCreate, TaskUpdate
from app.infra.repositories import TaskRepository
from app.domain.exceptions import TaskNotFoundException


class TaskService:
    """Task 관련 비즈니스 로직을 처리하는 서비스"""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def get_all_tasks(self) -> List[Task]:
        """모든 Task를 조회"""
        return self.repository.find_all()
    
    def get_task_by_id(self, task_id: int) -> Task:
        """ID로 Task 조회"""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        return task
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """새로운 Task 생성"""
        now = datetime.now()
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=now,
            updated_at=now
        )
        return self.repository.save(task)
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        """Task 수정"""
        task = self.get_task_by_id(task_id)
        
        # 업데이트할 필드만 변경
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.completed is not None:
            task.completed = task_data.completed
        
        task.updated_at = datetime.now()
        
        return self.repository.update(task)
    
    def delete_task(self, task_id: int) -> None:
        """Task 삭제"""
        task = self.get_task_by_id(task_id)
        self.repository.delete(task.id)
