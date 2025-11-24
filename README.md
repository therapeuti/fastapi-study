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

#### 📌 방법 1: if __name__ == "__main__" 사용 (권장)
```python
# main.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# ✅ 이 부분이 중요!
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
```

실행:
```bash
python main.py
```

**파라미터 설명:**
- `"main:app"`: 모듈명:앱 객체
- `reload=True`: 파일 변경 시 자동 재시작 (개발 모드)
- `host="0.0.0.0"`: 모든 IP에서 접근 가능
- `port=8000`: 포트 번호

#### 📌 방법 2: 명령행에서 직접 실행
```bash
# 자동 리로드 모드
fastapi dev main.py

# 또는
uvicorn main:app --reload

# 포트 변경
uvicorn main:app --reload --port 8080

# 프로덕션 (리로드 없음)
uvicorn main:app
```

### 4. 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

---

## 📋 학습 진행 체계

### **1일차: 기초 (1-3장)**
- [x] Flask와 FastAPI 비교 읽기
- [x] 환경 설정 완료
- [x] 첫 API 작성 및 실행
- [x] Path/Query 파라미터 실습
- [x] 서버 실행 방법 (uvicorn, if __name__)

### **2일차: 데이터 처리 (4-5장)**
- [x] Pydantic 모델 학습
- [x] Request Body 처리
- [x] Response Model 구현
- [x] 간단한 CRUD API 작성
- [x] 모델 기본값 설정
- [x] 선택적/필수 필드 구분

### **3일차: 비즈니스 로직 (6-7장)**
- [x] 글로벌 변수와 global 키워드
- [x] 함수 내에서 변수 수정하기
- [ ] 에러 핸들링 이해
- [ ] 의존성 주입 활용
- [ ] 인증 로직 구현
- [ ] 복잡한 API 설계

### **4일차: 고급 주제 (8-9장)**
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

## 📝 예제 프로젝트 및 학습 코드

### 📂 프로젝트 구조

```
fastapi-study/
├── README.md                          # 이 파일
├── 01_Flask_vs_FastAPI.md            # Flask vs FastAPI 비교
├── 02_환경설정_및_첫API.md
├── 03_Path_Query_Parameters.md        # Path/Query 파라미터 (실전 테스트 결과 포함)
├── 04_Request_Body_Pydantic.md
├── 05_Response_Model_및_상태코드.md
├── 06_에러핸들링.md
├── 07_의존성주입.md
├── 08_미들웨어_CORS.md
├── 09_인증_보안.md
│
├── 1.helloworld.py                   # 첫 번째 예제
├── 2_path_query_param.py             # Path & Query 파라미터 예제
├── todolist.py                        # TODO API 프로젝트 (CRUD + 동적 ID)
│
├── static/
│   ├── todolist.html                 # TODO 프론트엔드
│   └── js/
│       └── todolist.js               # TODO JavaScript (async/await, fetch)
│
└── templates/                         # (필요시) Jinja2 템플릿
    ├── index.html
    ├── request_body.html
    ├── error_handling.html
    └── security.html
```

### 🎯 실습 프로젝트

#### **초급 - TODO List API**
현재 학습 중인 프로젝트입니다.

**구현 기능:**
- [x] GET `/api/todo/` - 모든 TODO 조회
- [x] POST `/api/todo/` - 새 TODO 추가 (자동 ID 생성)
- [ ] PUT `/api/todo/{id}` - TODO 상태 수정
- [ ] DELETE `/api/todo/{id}` - TODO 삭제
- [x] 프론트엔드 (HTML + JavaScript)

**핵심 학습 내용:**
- Pydantic 모델 (기본값, 선택적 필드)
- 전역 변수 관리 (`global` 키워드)
- 비동기 JavaScript (`async/await`, `fetch`)
- REST API 설계

```python
# todolist.py 예제
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class Todo(BaseModel):
    todo: str
    status: bool = False

todolist = [{'id': 1, 'todo': '투두리스트', 'status': False}]
todo_id = 2

@app.post('/api/todo/')
def add_todolist(todo: Todo):
    global todo_id  # 글로벌 변수 수정
    todo_dict = todo.dict()
    todo_dict['id'] = todo_id
    todo_id += 1
    todolist.append(todo_dict)
    return {'todolist': todolist}

if __name__ == "__main__":
    uvicorn.run("todolist:app", reload=True)
```

#### **중급 프로젝트 아이디어**
- 👥 사용자 관리 API
- 📱 블로그 API (게시글, 댓글)
- 🛒 쇼핑몰 API (상품, 주문)

#### **고급 프로젝트 아이디어**
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

### 4. 글로벌 변수를 함수 내에서 수정할 때
```python
# ❌ 나쁜 예 (UnboundLocalError 발생)
counter = 0

@app.post("/increment")
def increment():
    counter += 1  # 에러!
    return counter

# ✅ 좋은 예
counter = 0

@app.post("/increment")
def increment():
    global counter  # 글로벌 선언 필수
    counter += 1
    return counter
```

### 5. Pydantic 모델에서 JSON 데이터를 딕셔너리로 변환하기
```python
# ❌ 나쁜 예
@app.post("/items")
def create_item(item: Item):
    todolist.append(item)  # Item 객체 직접 추가

# ✅ 좋은 예
@app.post("/items")
def create_item(item: Item):
    item_dict = item.dict()  # 딕셔너리로 변환
    todolist.append(item_dict)
    return {"list": todolist}
```

### 6. JavaScript에서 비동기 함수 제어 흐름
```javascript
// ❌ 나쁜 예 (순서 보장 안 됨)
document.addEventListener('click', async (e) => {
    updateStatus(id);  // 완료 대기 없음
    get_todolist()     // updateStatus가 끝나지 않았는데 바로 실행
})

// ✅ 좋은 예
document.addEventListener('click', async (e) => {
    await updateStatus(id);  // 완료 대기
    await get_todolist()     // updateStatus 완료 후 실행
})
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

**상세 가이드:**
```python
# ✅ 동기 함수 (메모리 연산만 할 때)
@app.get("/calculate")
def calculate(a: int, b: int):
    return {"result": a + b}  # CPU만 사용

@app.get("/items")
def get_items():
    return {"items": items_list}  # 메모리에서 바로 반환

# ✅ 비동기 함수 (I/O 작업이 있을 때)
@app.get("/users")
async def get_users():
    # 데이터베이스 조회 (대기 필요)
    users = await db.fetch("SELECT * FROM users")
    return users

@app.post("/create")
async def create_item(item: Item):
    # 외부 API 호출 (대기 필요)
    response = await httpx.get("https://api.example.com")
    return response
```

**성능 비교:**
| 상황 | 동기 | 비동기 |
|------|------|--------|
| I/O 없음 | ✅ 좋음 | 동일 |
| 데이터베이스 | ❌ 느림 (블로킹) | ✅ 빠름 |
| 외부 API | ❌ 느림 (대기) | ✅ 빠름 |
| 파일 읽기 | ❌ 느림 | ✅ 빠름 |

**초급 권장:** 지금은 동기로 충분합니다. 데이터베이스를 사용할 때 비동기로 전환하면 됩니다.

### Q: Pydantic 검증이 자동으로 되나요?
**A:** 네, BaseModel을 상속한 클래스에서 타입을 지정하면 자동으로 검증됩니다.

### Q: 프로덕션 환경에서는 어떻게 배포하나요?
**A:** gunicorn/uvicorn + Docker + Kubernetes 또는 클라우드 서비스를 사용합니다.

### Q: 모델에서 기본값을 지정하면 프론트에서 안 보내도 되나요?
**A:** 네! 기본값이 있는 필드는 선택적이므로 프론트에서 생략할 수 있습니다. 예: `status: bool = False`

### Q: 함수 내에서 글로벌 변수를 수정하려면 어떻게 하나요?
**A:** `global` 키워드를 함수 시작 부분에 추가해야 합니다.
```python
@app.post("/increment")
def increment():
    global counter  # 이 줄 필수!
    counter += 1
    return counter
```

### Q: JavaScript에서 서버 요청 완료를 기다려야 하나요?
**A:** 네, 비동기 함수를 사용할 때는 `await`를 붙여야 순서가 보장됩니다.
```javascript
await updateStatus(id);  // 완료 대기
await get_todolist()     // 그 다음 실행
```

### Q: fetch로 보낸 JSON 데이터를 서버에서 받으려면?
**A:** Pydantic 모델로 정의하면 자동 검증됩니다. 프론트에서 `{ "todo": "할일" }` 형식으로 보내야 합니다.

### Q: 모델 객체를 리스트에 추가할 때 어떻게 해야 하나요?
**A:** `.dict()` 메서드로 딕셔너리로 변환한 후 추가합니다.
```python
item_dict = item.dict()
todolist.append(item_dict)
```
