# FastAPI Sample - Task Management API

ADR을 준수하는 계층화된 아키텍처로 구현된 Task 관리 API입니다.

## 아키텍처

### ADR-0001: Layered Architecture
- **API Layer** (`app/api/`): HTTP 요청/응답 처리
- **Domain Layer** (`app/domain/`): 비즈니스 로직 및 모델
- **Infrastructure Layer** (`app/infra/`): 데이터 저장소 (현재 InMemory)

### ADR-0002: Error Handling
모든 에러 응답은 다음 JSON 포맷을 사용합니다:
```json
{
  "errorCode": "TASK_NOT_FOUND",
  "message": "Task with id 1 not found",
  "details": {"task_id": 1}
}
```

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행
```bash
uvicorn app.main:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | 모든 Task 조회 |
| GET | `/tasks/{id}` | 특정 Task 조회 |
| POST | `/tasks` | Task 생성 |
| PUT | `/tasks/{id}` | Task 수정 |
| DELETE | `/tasks/{id}` | Task 삭제 |

## 사용 예제

### Task 생성
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "FastAPI 공부하기", "description": "FastAPI 문서 읽기"}'
```

### 모든 Task 조회
```bash
curl -X GET "http://localhost:8000/tasks"
```

### Task 수정
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 프로젝트 구조

```
FastAPI_Sample/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── api/                    # API Layer
│   │   ├── __init__.py
│   │   ├── tasks.py            # Task API 엔드포인트
│   │   └── error_responses.py  # 표준 에러 응답
│   ├── domain/                 # Domain Layer
│   │   ├── __init__.py
│   │   ├── models.py           # 도메인 모델
│   │   ├── services.py         # 비즈니스 로직
│   │   └── exceptions.py       # 도메인 예외
│   └── infra/                  # Infrastructure Layer
│       ├── __init__.py
│       └── repositories.py     # 데이터 저장소
├── requirements.txt
└── README.md
```
