# 02. 환경 설정 및 첫 API 만들기

이 장에서는 FastAPI 개발 환경을 설정하고 첫 번째 API를 만들어봅니다.

## 1. 환경 설정

### 1.1 Python 버전 확인

FastAPI는 Python 3.7 이상이 필요합니다.

```bash
python --version
# 또는
python3 --version
```

### 1.2 가상환경 생성

프로젝트 폴더를 생성하고 가상환경을 설정합니다.

```bash
# 프로젝트 디렉토리 생성
mkdir fastapi-project
cd fastapi-project

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 1.3 필수 패키지 설치

FastAPI를 설치합니다.

```bash
# 기본 설치
pip install fastapi

# FastAPI + Uvicorn (ASGI 서버)
pip install fastapi uvicorn[standard]

# 모든 기본 의존성 포함 (권장)
pip install "fastapi[standard]"
```

**설치된 주요 패키지:**
- **fastapi**: FastAPI 프레임워크
- **uvicorn**: ASGI 서버
- **pydantic**: 데이터 검증
- **starlette**: ASGI 애플리케이션 프레임워크

### 1.4 설치 확인

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

---

## 2. 첫 번째 FastAPI 애플리케이션

### 2.1 기본 구조

`main.py` 파일을 생성합니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**코드 설명:**
- `FastAPI()`: FastAPI 애플리케이션 인스턴스 생성
- `@app.get()`: GET 요청 처리를 위한 데코레이터
- `read_root()`: 경로 작업 함수 (endpoint)

### 2.2 서버 실행

```bash
# fastapi dev 명령어 (권장 - 자동 리로드)
fastapi dev main.py

# 또는 uvicorn 직접 사용
uvicorn main:app --reload
```

**실행 결과:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete [Lifespan.startup]
```

### 2.3 API 테스트

브라우저에서 다음 주소에 접속합니다:

```
http://127.0.0.1:8000/
```

**응답:**
```json
{"message": "Hello World"}
```

---

## 3. 자동 문서화

FastAPI는 OpenAPI 표준을 따르는 자동 문서화를 제공합니다.

### 3.1 Swagger UI 확인

다음 주소에 접속하면 대화형 API 문서를 볼 수 있습니다:

```
http://127.0.0.1:8000/docs
```

**Swagger UI의 기능:**
- 모든 엔드포인트 목록
- 각 엔드포인트의 파라미터 설명
- "Try it out" 버튼으로 API 직접 테스트
- 요청/응답 예시

### 3.2 ReDoc 확인

다른 형식의 API 문서:

```
http://127.0.0.1:8000/redoc
```

**ReDoc의 특징:**
- 깔끔한 문서 형식
- 검색 기능 제공
- 인쇄 친화적

### 3.3 OpenAPI Schema

OpenAPI 스키마 JSON 파일:

```
http://127.0.0.1:8000/openapi.json
```

---

## 4. 향상된 첫 번째 API

이제 더 실용적인 예제를 작성해봅시다.

### 4.1 여러 엔드포인트 추가

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="FastAPI 학습용 API",
    version="1.0.0"
)

@app.get("/", tags=["root"])
def read_root():
    """
    루트 경로입니다.
    """
    return {"message": "Hello World"}

@app.get("/api/hello", tags=["greeting"])
def read_hello():
    """
    인사말을 반환합니다.
    """
    return {"message": "Hello from FastAPI"}

@app.get("/api/status", tags=["status"])
def read_status():
    """
    서버 상태를 확인합니다.
    """
    return {"status": "running"}
```

**FastAPI 생성자 파라미터:**
- `title`: API 제목
- `description`: API 설명
- `version`: API 버전
- `tags`: 문서에서 그룹핑할 때 사용

### 4.2 엔드포인트 설명 추가

문서화를 더 상세하게 하기 위해 설명과 요약을 추가합니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get(
    "/api/users",
    summary="사용자 목록 조회",
    description="모든 사용자의 목록을 조회합니다.",
    tags=["users"]
)
def get_users():
    """
    사용자 목록을 반환합니다.

    **응답:**
    - `users`: 사용자 목록 배열
    - `total`: 전체 사용자 수
    """
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "total": 2
    }
```

---

## 5. 다양한 HTTP 메서드

FastAPI는 모든 HTTP 메서드를 지원합니다.

```python
from fastapi import FastAPI

app = FastAPI()

# GET: 데이터 조회
@app.get("/items")
def get_items():
    return {"items": []}

# POST: 데이터 생성
@app.post("/items")
def create_item():
    return {"message": "Item created"}

# PUT: 데이터 전체 수정
@app.put("/items/1")
def update_item():
    return {"message": "Item updated"}

# PATCH: 데이터 부분 수정
@app.patch("/items/1")
def partial_update_item():
    return {"message": "Item partially updated"}

# DELETE: 데이터 삭제
@app.delete("/items/1")
def delete_item():
    return {"message": "Item deleted"}

# HEAD: GET과 동일하지만 응답 본문 없음
@app.head("/items")
def check_items():
    return {}

# OPTIONS: 사용 가능한 HTTP 메서드 확인
@app.options("/items")
def options_items():
    return {}
```

---

## 6. 비동기 vs 동기

### 6.1 비동기 함수 (권장)

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/async-task")
async def async_task():
    """
    비동기 함수는 I/O 작업에 적합합니다.
    """
    # 데이터베이스 쿼리, API 호출 등
    await asyncio.sleep(1)  # I/O 시뮬레이션
    return {"message": "Async task completed"}
```

### 6.2 동기 함수

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/sync-task")
def sync_task():
    """
    동기 함수는 CPU 집약적 작업에 적합합니다.
    """
    # 계산, 데이터 처리 등
    result = sum(range(1000000))
    return {"result": result}
```

**선택 기준:**
- **비동기 (async)**: 데이터베이스, API 호출, 파일 I/O 등
- **동기**: CPU 집약적 계산, 메모리 처리 등

---

## 7. 응답 형식

### 7.1 JSON 응답

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/json")
def get_json():
    return {"key": "value", "number": 42, "array": [1, 2, 3]}
```

### 7.2 리스트 응답

```python
@app.get("/list")
def get_list():
    return [1, 2, 3, 4, 5]
```

### 7.3 문자열 응답

```python
@app.get("/string")
def get_string():
    return "Hello World"
```

### 7.4 숫자 응답

```python
@app.get("/number")
def get_number():
    return 42
```

**중요:** FastAPI는 Python 객체를 자동으로 JSON으로 변환합니다.

---

## 8. 상태 코드 지정

### 8.1 기본 상태 코드

```python
from fastapi import FastAPI, status

app = FastAPI()

# GET: 기본값 200
@app.get("/items")
def get_items():
    return {"items": []}

# POST: 기본값 200 (201로 변경 가능)
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"message": "Item created"}
```

### 8.2 자주 사용되는 상태 코드

```python
from fastapi import FastAPI, status

app = FastAPI()

# 200 OK - 성공
@app.get("/ok")
def get_ok():
    return {"status": "ok"}

# 201 Created - 생성됨
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"id": 1}

# 204 No Content - 응답 본문 없음
@app.delete("/items/1", status_code=status.HTTP_204_NO_CONTENT)
def delete_item():
    return None

# 400 Bad Request - 잘못된 요청
@app.get("/bad")
def get_bad():
    return {"error": "Invalid request"}

# 404 Not Found - 찾을 수 없음
@app.get("/notfound")
def get_notfound():
    return {"error": "Not found"}

# 500 Internal Server Error - 서버 오류
@app.get("/error")
def get_error():
    return {"error": "Internal server error"}
```

**상태 코드 상수:**
- `status.HTTP_200_OK`
- `status.HTTP_201_CREATED`
- `status.HTTP_204_NO_CONTENT`
- `status.HTTP_400_BAD_REQUEST`
- `status.HTTP_401_UNAUTHORIZED`
- `status.HTTP_403_FORBIDDEN`
- `status.HTTP_404_NOT_FOUND`
- `status.HTTP_500_INTERNAL_SERVER_ERROR`

---

## 9. 프로젝트 구조

좋은 프로젝트 구조는 유지보수를 쉽게 합니다.

### 9.1 기본 구조

```
fastapi-project/
├── main.py                 # 애플리케이션 진입점
├── requirements.txt        # 의존성 목록
├── .gitignore             # Git 무시 파일
└── venv/                  # 가상환경 (커밋하지 않음)
```

### 9.2 중급 구조

```
fastapi-project/
├── main.py
├── requirements.txt
├── .gitignore
├── .env
├── app/
│   ├── __init__.py
│   ├── main.py           # 메인 애플리케이션
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── items.py
│   │   │   └── users.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py
│   └── schemas/
│       ├── __init__.py
│       └── item.py
└── venv/
```

---

## 10. requirements.txt 작성

프로젝트 의존성을 관리합니다.

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
```

**설치 방법:**
```bash
pip install -r requirements.txt
```

**업데이트:**
```bash
pip freeze > requirements.txt
```

---

## 11. 실습 예제

### 예제 1: 간단한 계산 API

```python
from fastapi import FastAPI

app = FastAPI(title="계산 API")

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    """
    두 수를 더합니다.
    """
    return {"result": a + b}

@app.get("/subtract/{a}/{b}")
def subtract(a: int, b: int):
    """
    두 수를 뺍니다.
    """
    return {"result": a - b}

@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    """
    두 수를 곱합니다.
    """
    return {"result": a * b}

@app.get("/divide/{a}/{b}")
def divide(a: int, b: int):
    """
    두 수를 나눕니다.
    """
    if b == 0:
        return {"error": "Division by zero"}
    return {"result": a / b}
```

**테스트:**
```
GET http://localhost:8000/add/5/3
응답: {"result": 8}

GET http://localhost:8000/multiply/4/7
응답: {"result": 28}
```

### 예제 2: 사용자 정보 API

```python
from fastapi import FastAPI

app = FastAPI(title="사용자 정보 API")

# 샘플 데이터
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}

@app.get("/users")
def list_users():
    """
    모든 사용자를 조회합니다.
    """
    return list(users_db.values())

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    특정 사용자를 조회합니다.
    """
    if user_id in users_db:
        return users_db[user_id]
    return {"error": "User not found"}

@app.get("/users/email/{email}")
def get_user_by_email(email: str):
    """
    이메일로 사용자를 조회합니다.
    """
    for user in users_db.values():
        if user["email"] == email:
            return user
    return {"error": "User not found"}
```

**테스트:**
```
GET http://localhost:8000/users
응답: [{"id": 1, "name": "Alice", ...}, ...]

GET http://localhost:8000/users/1
응답: {"id": 1, "name": "Alice", "email": "alice@example.com"}
```

---

## 12. 실행 및 테스트

### 12.1 서버 실행

#### 방식 1: FastAPI CLI (권장)

```bash
# 가장 간단한 방식 (v0.109+)
fastapi dev main.py
```

#### 방식 2: Uvicorn 명령줄

```bash
# 기본 실행
uvicorn main:app --reload

# 호스트와 포트 지정
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 방식 3: Python 스크립트에서 실행

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    # ⭐ 중요: 파라미터가 reload=True나 workers>1이면 앱을 문자열로 지정!
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
```

실행:
```bash
python main.py
```

### 12.1.1 Reload 경고 메시지 해결

**문제 상황:**
```
WARNING:  You must pass the application as an import string to enable 'reload' or 'workers'.
```

이 경고가 나타나는 이유와 해결법:

**❌ 잘못된 코드 (경고 발생)**
```python
if __name__ == "__main__":
    import uvicorn
    # 앱 객체를 직접 전달하고 reload=True를 사용하면 경고 발생!
    uvicorn.run(app, reload=True)
```

**✅ 올바른 코드 (경고 없음)**
```python
if __name__ == "__main__":
    import uvicorn
    # 앱을 문자열로 지정 (모듈명:앱객체명)
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
```

**원인 설명:**

`reload=True` 또는 `workers > 1`을 사용하면 Uvicorn이 **여러 프로세스를 생성**합니다.
이때 Python 객체는 프로세스 간 전달할 수 없으므로 **문자열 형식의 임포트 경로**를 사용해야 합니다.

**해결책 정리:**

| 상황 | 파라미터 | 올바른 사용법 |
|------|---------|------------|
| 개발 (자동 리로드) | `reload=True` | `uvicorn.run("main:app", reload=True)` |
| 프로덕션 (다중 워커) | `workers=4` | `uvicorn.run("main:app", workers=4)` |
| 개발 (리로드 없음) | `reload=False` | `uvicorn.run(app, reload=False)` 또는 문자열 가능 |
| 프로덕션 (단일 워커) | `workers=1` | `uvicorn.run(app, workers=1)` 또는 문자열 가능 |

**권장 패턴:**

```python
# main.py - 개발 및 프로덕션 모두 작동
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    # 이 방식은 모든 경우에 경고가 없습니다
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
```

**패키지 구조에서의 사용:**

만약 다음과 같은 구조라면:
```
project/
├── app/
│   ├── __init__.py
│   └── main.py
└── run.py
```

`run.py`에서:
```python
# run.py
import uvicorn

if __name__ == "__main__":
    # 패키지.모듈:앱 형식으로 지정
    uvicorn.run("app.main:app", reload=True, port=8000)
```

실행:
```bash
python run.py
```

### 12.2 curl로 테스트

```bash
# GET 요청
curl http://localhost:8000/

# POST 요청
curl -X POST http://localhost:8000/items

# JSON 데이터 포함
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Item 1"}'
```

### 12.3 Python requests로 테스트

```python
import requests

# GET 요청
response = requests.get("http://localhost:8000/")
print(response.json())

# POST 요청
response = requests.post("http://localhost:8000/items")
print(response.json())
```

---

## 13. 문제 해결

### 13.1 "ModuleNotFoundError: No module named 'fastapi'"

```bash
# 가상환경이 활성화되었는지 확인
which python  # macOS/Linux
where python  # Windows

# FastAPI 설치 재확인
pip install fastapi uvicorn[standard]
```

### 13.2 포트 이미 사용 중

```bash
# 다른 포트 사용
uvicorn main:app --port 8001

# 기존 프로세스 종료
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### 13.3 "Address already in use"

```bash
# 서버를 완전히 종료할 때까지 기다리기
# 또는 다른 포트 사용
uvicorn main:app --port 8001
```

---

## 요약

- FastAPI 설치 및 가상환경 설정
- 첫 번째 API 만들기 및 실행
- 자동 문서화 활용 (Swagger UI, ReDoc)
- HTTP 메서드 및 상태 코드
- 비동기 vs 동기 함수 선택
- 프로젝트 구조 및 의존성 관리

**다음 장**: Path 파라미터와 Query 파라미터에 대해 배웁니다.
