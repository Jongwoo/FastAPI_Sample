# 이 파일은 ARCH/adr/ADR-0001-layered-architecture.md, ARCH/adr/ADR-0002-error-handling.md를 따른다.
# - ADR-0001: api 레이어에서 domain 서비스에 의존하고 infra에는 직접 의존하지 않는다.
# - ADR-0002: 모든 에러 응답은 {"errorCode","message","details"} JSON 포맷을 사용해야 한다.

# TODO: 위 ADR을 준수하는 간단한 FastAPI 예제를 만들어줘.
# /tasks GET: 모든 Task 조회 (지금은 InMemory 저장소로 충분)
# /tasks POST: Task 생성
