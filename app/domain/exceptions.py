"""
도메인 예외
ADR-0002: 구조화된 에러 처리를 위한 커스텀 예외
"""


class DomainException(Exception):
    """도메인 계층 기본 예외"""
    def __init__(self, message: str, error_code: str = "DOMAIN_ERROR", details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class TaskNotFoundError(DomainException):
    """Task를 찾을 수 없을 때 발생"""
    def __init__(self, message: str = "Task not found", details: dict = None):
        super().__init__(message=message, error_code="TASK_NOT_FOUND", details=details)


class InvalidTaskDataError(DomainException):
    """Task 데이터가 유효하지 않을 때 발생"""
    def __init__(self, message: str = "Invalid task data", details: dict = None):
        super().__init__(message=message, error_code="INVALID_TASK_DATA", details=details)
