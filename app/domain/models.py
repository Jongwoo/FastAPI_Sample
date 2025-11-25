"""
도메인 모델
ADR-0001: domain 레이어에 비즈니스 엔티티 정의
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    """Task 도메인 모델"""
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "title": "FastAPI 학습하기",
                "description": "FastAPI 공식 문서 읽기",
                "completed": False
            }
        }
