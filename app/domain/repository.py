"""
Repository 인터페이스
ADR-0001: domain에서 인터페이스만 정의, 구현은 infra에 위치
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import Task


class TaskRepository(ABC):
    """Task 저장소 인터페이스"""
    
    @abstractmethod
    def create(self, task: Task) -> Task:
        """Task 생성"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """모든 Task 조회"""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """ID로 Task 조회"""
        pass
    
    @abstractmethod
    def update(self, task_id: str, task: Task) -> Optional[Task]:
        """Task 수정"""
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Task 삭제"""
        pass
