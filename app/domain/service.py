"""
도메인 서비스
ADR-0001: 비즈니스 로직 처리, Repository 인터페이스에 의존
"""
from typing import List
from datetime import datetime
import uuid
import logging

from app.domain.models import Task
from app.domain.repository import TaskRepository
from app.domain.exceptions import TaskNotFoundError, InvalidTaskDataError

logger = logging.getLogger(__name__)


class TaskService:
    """Task 비즈니스 로직 서비스"""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def create_task(self, task: Task) -> Task:
        """새로운 Task 생성"""
        logger.info(f"Creating task: {task.title}")
        
        # 비즈니스 규칙: title은 필수
        if not task.title or not task.title.strip():
            raise InvalidTaskDataError("Task title cannot be empty")
        
        # ID와 타임스탬프 설정
        task.id = str(uuid.uuid4())
        task.created_at = datetime.now()
        task.updated_at = datetime.now()
        
        return self.repository.create(task)
    
    def get_all_tasks(self) -> List[Task]:
        """모든 Task 조회"""
        logger.info("Fetching all tasks")
        return self.repository.find_all()
    
    def get_task_by_id(self, task_id: str) -> Task:
        """ID로 Task 조회"""
        task = self.repository.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
        return task
    
    def update_task(self, task_id: str, task_data: Task) -> Task:
        """Task 수정"""
        existing_task = self.get_task_by_id(task_id)
        
        if task_data.title:
            existing_task.title = task_data.title
        if task_data.description is not None:
            existing_task.description = task_data.description
        if task_data.completed is not None:
            existing_task.completed = task_data.completed
        
        existing_task.updated_at = datetime.now()
        
        return self.repository.update(task_id, existing_task)
    
    def delete_task(self, task_id: str) -> None:
        """Task 삭제"""
        self.get_task_by_id(task_id)  # 존재 여부 확인
        self.repository.delete(task_id)
