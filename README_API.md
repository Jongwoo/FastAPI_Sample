# FastAPI Task Service

ADR 가이드라인을 따르는 간단한 Task 관리 FastAPI 애플리케이션입니다.

## 아키텍처

이 프로젝트는 다음 ADR (Architecture Decision Record)을 따릅니다:

- **ADR-0001**: 레이어드 아키텍처와 의존성 주입
- **ADR-0002**: 표준 에러 응답 포맷

### 프로젝트 구조

```
app/
├── api/                    # HTTP 엔드포인트 (FastAPI router)
│   ├── __init__.py
│   └── tasks.py           # Task 관련 API 엔드포인트
├── domain/                # 도메인 모델, 도메인 서비스 (비즈니스 로직)
│   ├── __init__.py
│   ├── task_models.py     # Task 도메인 모델
│   ├── task_repository.py # Task Repository 인터페이스
│   └── task_service.py    # Task 도메인 서비스
├── infra/                 # 외부 의존성 (DB, 외부 API, in-memory repository 등)
│   ├── __init__.py
│   └── task_repository_impl.py # InMemory Task Repository 구현
├── __init__.py
└── main.py                # FastAPI 애플리케이션 진입점
```

### 의존성 방향

`api` → `domain` → `infra` (단방향 참조)

## API 엔드포인트

### Task 관리

- `GET /tasks/` - 모든 Task 조회
- `POST /tasks/` - Task 생성

### 요청/응답 예시

#### Task 생성
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "새로운 Task",
    "description": "Task 설명"
  }'
```

응답:
```json
{
  "id": 1,
  "title": "새로운 Task",
  "description": "Task 설명",
  "completed": false,
  "created_at": "2025-12-05T13:12:00.000000",
  "updated_at": "2025-12-05T13:12:00.000000"
}
```

#### 모든 Task 조회
```bash
curl -X GET "http://localhost:8000/tasks/"
```

응답:
```json
[
  {
    "id": 1,
    "title": "새로운 Task",
    "description": "Task 설명",
    "completed": false,
    "created_at": "2025-12-05T13:12:00.000000",
    "updated_at": "2025-12-05T13:12:00.000000"
  }
]
```

### 에러 응답 포맷 (ADR-0002)

모든 에러 응답은 다음 JSON 포맷을 따릅니다:

```json
{
  "errorCode": "INVALID_INPUT",
  "message": "Task title cannot be empty",
  "details": {
    "field": "title"
  }
}
```

## 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 테스트

프로젝트에 포함된 테스트 스크립트를 실행할 수 있습니다:

```bash
python test_app.py
```

## 특징

- **레이어드 아키텍처**: 비즈니스 로직과 인프라 코드가 분리되어 있음
- **의존성 주입**: 인터페이스 기반 DI로 테스트가 용이함
- **표준화된 에러 처리**: 일관된 에러 응답 포맷
- **InMemory 저장소**: 현재는 메모리에 데이터를 저장 (향후 DB로 확장 가능)
