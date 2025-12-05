"""
도메인 예외 정의
"""


class DomainException(Exception):
    """도메인 계층의 기본 예외"""
    pass


class TaskNotFoundException(DomainException):
    """Task를 찾을 수 없을 때 발생하는 예외"""
    
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")
