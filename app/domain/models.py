"""
도메인 모델 정의
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    """Task 도메인 모델"""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "FastAPI 공부하기",
                "description": "FastAPI 문서를 읽고 예제 만들기",
                "completed": False,
                "created_at": "2025-12-05T10:00:00",
                "updated_at": "2025-12-05T10:00:00"
            }
        }


class TaskCreate(BaseModel):
    """Task 생성 요청 모델"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI 공부하기",
                "description": "FastAPI 문서를 읽고 예제 만들기"
            }
        }


class TaskUpdate(BaseModel):
    """Task 수정 요청 모델"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None
