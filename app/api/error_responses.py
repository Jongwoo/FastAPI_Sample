"""
ADR-0002: 표준 에러 응답 포맷 정의
모든 에러 응답은 {"errorCode", "message", "details"} JSON 포맷을 사용
"""
from typing import Optional, Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """표준 에러 응답 모델"""
    errorCode: str
    message: str
    details: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "errorCode": "TASK_NOT_FOUND",
                "message": "Task with id 1 not found",
                "details": {"task_id": 1}
            }
        }
