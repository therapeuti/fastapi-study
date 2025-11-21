# FastAPI 학습 가이드

Flask에 익숙한 개발자를 위한 **FastAPI 완벽 학습 자료**입니다.

## 📚 학습 목차

### 1️⃣ 기초 개념
- **[01_Flask_vs_FastAPI.md](./01_Flask_vs_FastAPI.md)**
  - Flask와 FastAPI의 차이점
  - 마이그레이션 가이드
  - 성능 비교 및 개발 경험

### 2️⃣ 환경 설정 및 첫 API
- **[02_환경설정_및_첫API.md](./02_환경설정_및_첫API.md)**
  - 환경 설정 (Python, 가상환경)
  - 첫 번째 FastAPI 애플리케이션
  - 자동 문서화 (Swagger UI, ReDoc)
  - HTTP 메서드 및 상태 코드

### 3️⃣ 파라미터 처리
- **[03_Path_Query_Parameters.md](./03_Path_Query_Parameters.md)**
  - Path 파라미터와 검증
  - Query 파라미터와 검증
  - 리스트 파라미터
  - 실전 예제

### 4️⃣ Request Body와 Pydantic
- **[04_Request_Body_Pydantic.md](./04_Request_Body_Pydantic.md)**
  - Pydantic 모델 기초
  - Field 검증
  - 커스텀 검증 (Validator)
  - 중첩된 모델
  - 실전 예제

### 5️⃣ Response Model과 상태 코드
- **[05_Response_Model_및_상태코드.md](./05_Response_Model_및_상태코드.md)**
  - Response Model 개념
  - 필드 필터링 (include/exclude)
  - HTTP 상태 코드
  - 응답 헤더
  - 모범 사례

### 6️⃣ 에러 핸들링
- **[06_에러핸들링.md](./06_에러핸들링.md)**
  - HTTPException 기초
  - 일반적인 에러 상황
  - 커스텀 예외 처리
  - Pydantic 검증 에러
  - 실전 예제

### 7️⃣ 의존성 주입
- **[07_의존성주입.md](./07_의존성주입.md)**
  - 의존성 주입(DI) 개념
  - 기본 의존성
  - 의존성 체인
  - 실전 예제 (인증, 데이터베이스)
  - 테스트

### 8️⃣ 미들웨어와 CORS
- **[08_미들웨어_CORS.md](./08_미들웨어_CORS.md)**
  - 미들웨어 개념과 구현
  - CORS 설정
  - 환경별 설정
  - 실전 예제

### 9️⃣ 인증과 보안
- **[09_인증_보안.md](./09_인증_보안.md)**
  - Basic Authentication
  - Bearer Token
  - OAuth 2.0 with JWT
  - 비밀번호 해싱
  - HTTPS 및 보안 헤더
  - Rate Limiting
  - 완전한 인증 시스템 구현

---

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# FastAPI 설치
pip install "fastapi[standard]"
```

### 2. 첫 번째 API 만들기
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

### 3. 서버 실행
```bash
# 자동 리로드 모드
fastapi dev main.py

# 또는
uvicorn main:app --reload
```

### 4. 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

---

## 📋 학습 진행 체계

### **1주차: 기초 (1-3장)**
- [ ] Flask와 FastAPI 비교 읽기
- [ ] 환경 설정 완료
- [ ] 첫 API 작성 및 실행
- [ ] Path/Query 파라미터 실습

### **2주차: 데이터 처리 (4-5장)**
- [ ] Pydantic 모델 학습
- [ ] Request Body 처리
- [ ] Response Model 구현
- [ ] 간단한 CRUD API 작성

### **3주차: 비즈니스 로직 (6-7장)**
- [ ] 에러 핸들링 이해
- [ ] 의존성 주입 활용
- [ ] 인증 로직 구현
- [ ] 복잡한 API 설계

### **4주차: 고급 주제 (8-9장)**
- [ ] 미들웨어 구현
- [ ] CORS 설정
- [ ] OAuth 2.0 JWT 인증
- [ ] 보안 관련 설정

---

## 💡 학습 팁

### 1. 각 장마다 코드 작성하기
문서를 읽기만 하지 말고 **직접 코드를 작성하고 실행**하세요.

```bash
# 각 장별로 테스트 파일 생성
touch chapter_02_test.py
python main.py
```

### 2. Swagger UI 활용하기
문서를 읽으면서 `http://localhost:8000/docs`에서 직접 API를 테스트하세요.

### 3. curl이나 Postman으로 테스트
```bash
# curl 예제
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 1500}'
```

### 4. 공식 문서 참고
각 장의 개념을 이해한 후 [FastAPI 공식 문서](https://fastapi.tiangolo.com/)를 참고하세요.

---

## 🎯 각 장의 핵심 개념

| 장 | 제목 | 핵심 개념 | 실습 |
|---|------|---------|------|
| 01 | Flask vs FastAPI | 차이점, 마이그레이션 | - |
| 02 | 환경설정 | 설치, 첫 API, 문서화 | 계산기 API |
| 03 | Path & Query | 파라미터 검증 | 검색 API |
| 04 | Request Body | Pydantic, 검증 | 상품 등록 API |
| 05 | Response Model | 필터링, 상태 코드 | 사용자 프로필 API |
| 06 | 에러 핸들링 | HTTPException | 에러 처리 API |
| 07 | 의존성 주입 | DI 패턴, 재사용성 | 인증 시스템 |
| 08 | 미들웨어 & CORS | 로깅, CORS 설정 | API 래퍼 |
| 09 | 인증 & 보안 | JWT, 해싱, HTTPS | 로그인 시스템 |

---

## 🔗 추가 학습 자료

### 공식 리소스
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Starlette 문서](https://www.starlette.io/)

### 추천 패키지
```bash
# 기본
pip install fastapi uvicorn[standard]

# 데이터 검증
pip install pydantic

# 인증
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# 데이터베이스
pip install sqlalchemy

# 테스트
pip install pytest httpx
```

### 추천 학습 경로
1. **기초**: 1-5장 완료
2. **중급**: 6-8장 완료
3. **고급**: 9장 + 데이터베이스 연동
4. **실전**: WebSocket, 파일 업로드, 배포

---

## 📝 예제 프로젝트 아이디어

### 초급
- 📝 TODO API (CRUD)
- 🧮 계산기 API
- 📚 도서 목록 API

### 중급
- 👥 사용자 관리 API
- 📱 블로그 API (게시글, 댓글)
- 🛒 쇼핑몰 API (상품, 주문)

### 고급
- 🔐 JWT 인증 기반 API
- 📊 실시간 알림 시스템 (WebSocket)
- 📁 파일 업로드/다운로드 API

---

## ⚠️ 일반적인 실수

### 1. 타입 힌팅 생략
```python
# ❌ 나쁜 예
@app.get("/items")
def read_items(skip, limit):
    return {"skip": skip}

# ✅ 좋은 예
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip}
```

### 2. Pydantic 모델 없이 처리
```python
# ❌ 나쁜 예
@app.post("/items")
def create_item(data: dict):
    return data

# ✅ 좋은 예
class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return item
```

### 3. 에러 처리 누락
```python
# ❌ 나쁜 예
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return items_db[item_id]  # KeyError 가능

# ✅ 좋은 예
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Not found")
    return items_db[item_id]
```

---

## 🎓 학습 완료 후 다음 단계

1. **데이터베이스 연동** → SQLAlchemy, Tortoise ORM
2. **비동기 데이터베이스** → async SQLAlchemy, databases
3. **캐싱** → Redis
4. **백그라운드 작업** → Celery, APScheduler
5. **WebSocket** → 실시간 통신
6. **테스트** → pytest, httpx
7. **배포** → Docker, Kubernetes, AWS
8. **모니터링** → Sentry, Prometheus

---

## 💬 FAQ

### Q: Flask에서 FastAPI로 전환하면 어렵나요?
**A:** 이 가이드의 1장을 읽으면 차이점을 명확하게 이해할 수 있습니다. 기본 개념만 잡으면 매우 쉽습니다.

### Q: 동기 함수와 비동기 함수 중 어떤 것을 써야 하나요?
**A:** I/O 작업(DB, API 호출)이 있으면 비동기, CPU 작업만 있으면 동기를 사용하세요.

### Q: Pydantic 검증이 자동으로 되나요?
**A:** 네, BaseModel을 상속한 클래스에서 타입을 지정하면 자동으로 검증됩니다.

### Q: 프로덕션 환경에서는 어떻게 배포하나요?
**A:** gunicorn/uvicorn + Docker + Kubernetes 또는 클라우드 서비스를 사용합니다.

---

## 📞 피드백

각 장을 학습하면서 피드백이 있으시면 [FastAPI GitHub Issues](https://github.com/tiangolo/fastapi/issues)에 정리된 내용을 참고하세요.

---

**Happy Learning! 🎉**

Flask 개발자라면 FastAPI를 배우는 것이 아주 자연스러울 것입니다. 차근차근 따라가세요!
