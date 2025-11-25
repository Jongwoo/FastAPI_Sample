"""
에러 응답 모델
ADR-0002: 표준화된 에러 응답 포맷
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    표준 에러 응답
    ADR-0002: {"errorCode", "message", "details"} 포맷
    """
    errorCode: str
    message: str
    details: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "errorCode": "TASK_NOT_FOUND",
                "message": "Task not found",
                "details": {"taskId": "123"}
            }
        }
