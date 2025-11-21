# 01. Flask vs FastAPI 비교 가이드

Flask에 익숙한 개발자를 위한 FastAPI 학습 가이드입니다. 두 프레임워크의 주요 차이점을 이해하면 FastAPI 학습이 훨씬 쉬워집니다.

## 1. 핵심 차이점

### 1.1 성능 비교

| 항목 | Flask | FastAPI |
|------|-------|---------|
| **성능** | 중간 (동기 기반) | 높음 (비동기 기반) |
| **처리량** | ~초당 1000-2000 요청 | ~초당 10000+ 요청 |
| **ASGI 지원** | 별도 설정 필요 | 기본 지원 |
| **비동기** | 제한적 | 완전 지원 |

### 1.2 개발 경험

| 항목 | Flask | FastAPI |
|------|-------|---------|
| **학습곡선** | 낮음 (마이크로) | 중간 (풀 기능) |
| **자동 문서화** | 없음 (Swagger 추가 설정) | 자동 제공 |
| **타입 힌팅** | 선택사항 | 필수 |
| **데이터 검증** | 수동 또는 외부 라이브러리 | Pydantic 자동 지원 |

---

## 2. 코드 스타일 비교

### 2.1 기본 애플리케이션 생성

**Flask:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def read_root():
    return jsonify({"message": "Hello World"})

if __name__ == "__main__":
    app.run(debug=True)
```

**FastAPI:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

**주요 차이점:**
- FastAPI는 HTTP 메서드별로 명확한 데코레이터 사용 (`@app.get()`, `@app.post()`)
- Flask는 `@app.route()` 데코레이터에 `methods` 파라미터로 지정
- FastAPI는 자동으로 JSON 변환 (dict 반환 가능)
- Flask는 명시적으로 `jsonify()` 사용 필요

### 2.1.1 애플리케이션 실행 방식 (중요!)

#### Flask의 app.run() 사용

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # Flask의 내장 개발 서버 사용
    app.run(debug=True, host="127.0.0.1", port=5000)
```

**Flask app.run() 주요 파라미터:**

| 파라미터 | 설명 | 기본값 | 예시 |
|---------|------|--------|------|
| `debug` | 디버그 모드 (자동 리로드) | `False` | `debug=True` |
| `host` | 바인드할 호스트 | `127.0.0.1` | `host="0.0.0.0"` |
| `port` | 포트 번호 | `5000` | `port=8000` |
| `threaded` | 스레드 활성화 | `False` | `threaded=True` |
| `use_reloader` | 코드 변경 감지 리로드 | `True` | `use_reloader=True` |
| `ssl_context` | SSL/HTTPS 설정 | `None` | `ssl_context='adhoc'` |

```python
# Flask 실행 예제
if __name__ == "__main__":
    # 개발 환경
    app.run(debug=True, port=8000)

    # 프로덕션 환경
    app.run(debug=False, host="0.0.0.0", port=8000, threaded=True)

    # HTTPS
    app.run(ssl_context='adhoc', port=443)
```

#### FastAPI의 실행 방식

FastAPI는 WSGI/WSGI가 아닌 **ASGI** 기반이므로 직접 `app.run()` 메서드가 없습니다.
대신 **Uvicorn** (또는 다른 ASGI 서버)을 사용하여 실행합니다.

**방식 1: 명령줄에서 실행 (권장)**

```bash
# 기본 실행
uvicorn main:app --reload

# 호스트와 포트 지정
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# FastAPI CLI (v0.109 이상)
fastapi dev main.py
fastapi run main.py
```

**방식 2: Python 코드에서 실행**

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # Uvicorn으로 실행
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

**Uvicorn 주요 파라미터:**

| 파라미터 | 설명 | 기본값 | 예시 |
|---------|------|--------|------|
| `app` | ASGI 애플리케이션 | 필수 | `app` |
| `host` | 바인드할 호스트 | `127.0.0.1` | `host="0.0.0.0"` |
| `port` | 포트 번호 | `8000` | `port=8000` |
| `reload` | 자동 리로드 | `False` | `reload=True` |
| `workers` | 워커 프로세스 수 | `1` | `workers=4` |
| `log_level` | 로그 레벨 | `info` | `log_level="debug"` |
| `access_log` | 접근 로그 출력 | `True` | `access_log=True` |
| `ssl_keyfile` | SSL 키 파일 | `None` | `ssl_keyfile="key.pem"` |
| `ssl_certfile` | SSL 인증서 파일 | `None` | `ssl_certfile="cert.pem"` |

```python
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # 개발 환경
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

    # 프로덕션 환경 (여러 워커)
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)

    # HTTPS
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=443,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )
```

#### 비교 요약

| 측면 | Flask | FastAPI |
|------|-------|---------|
| **실행 방식** | `app.run()` 직접 호출 | Uvicorn 사용 |
| **명령줄** | Flask 없음 | `uvicorn main:app --reload` |
| **개발 서버** | 내장 (간단하지만 느림) | Uvicorn (빠르고 강력) |
| **자동 리로드** | `debug=True` | `--reload` 또는 `reload=True` |
| **멀티 워커** | 어려움 | `--workers 4` |
| **비동기** | 제한적 | 완전 지원 |

---

### 2.2 Path 파라미터 처리

**Flask:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/items/<int:item_id>")
def get_item(item_id):
    return {"item_id": item_id}
```

**FastAPI:**
```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., gt=0, lt=1000)):
    return {"item_id": item_id}
```

**주요 차이점:**
- FastAPI는 타입 힌팅으로 파라미터 타입 지정 (자동 변환 및 검증)
- Flask는 URL 패턴에 `<int:param>` 형식으로 지정
- FastAPI는 `Path()` 사용으로 추가 검증 규칙 적용 가능

---

### 2.3 Query 파라미터 처리

**Flask:**
```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/items/")
def list_items():
    skip = request.args.get("skip", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)
    return {"skip": skip, "limit": limit}
```

**FastAPI:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**주요 차이점:**
- FastAPI는 함수 파라미터로 쿼리 파라미터 자동 인식
- Flask는 `request.args.get()` 사용해서 수동 처리
- FastAPI는 기본값 설정 가능 (선택적 파라미터)

---

### 2.4 Request Body 처리

**Flask:**
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/items/", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")

    # 수동 검증
    if not name or not price:
        return jsonify({"error": "Invalid input"}), 400

    return {"name": name, "price": price}
```

**FastAPI:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**주요 차이점:**
- FastAPI는 Pydantic 모델로 자동 검증 (타입 체크, 필수/선택 필드)
- Flask는 수동으로 JSON 파싱 및 검증 필요
- FastAPI는 잘못된 요청에 자동으로 422 Unprocessable Entity 반환

---

### 2.5 응답 처리

**Flask:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/items/", methods=["POST"])
def create_item():
    item = {"name": "Item", "price": 100}
    return jsonify(item), 201

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    return "", 204
```

**FastAPI:**
```python
from fastapi import FastAPI, status

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None
```

**주요 차이점:**
- FastAPI는 `status_code` 파라미터로 명확하게 상태 코드 지정
- Flask는 tuple `(data, status_code)` 형태로 반환
- FastAPI의 `status` 모듈은 HTTP 상태 코드 상수 제공 (가독성 향상)

---

### 2.6 에러 처리

**Flask:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"detail": "Item not found"}), 404

@app.route("/items/<int:item_id>")
def get_item(item_id):
    if item_id < 1:
        return jsonify({"detail": "Invalid ID"}), 400

    item = database.get(item_id)
    if not item:
        return not_found(None)

    return item
```

**FastAPI:**
```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Invalid ID")

    item = database.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
```

**주요 차이점:**
- FastAPI는 `HTTPException` 예외 발생으로 에러 처리
- Flask는 에러 핸들러 데코레이터로 전역 처리
- FastAPI는 더 명시적이고 간결한 에러 처리

---

## 3. 비동기 처리

### 3.1 Flask의 비동기

Flask는 기본적으로 동기 프레임워크이며, 비동기 지원은 제한적입니다.

```python
from flask import Flask
import asyncio

app = Flask(__name__)

@app.route("/async-task")
async def async_task():
    await asyncio.sleep(1)
    return {"message": "Done"}
```

Flask는 위 코드를 지원하지만, 제대로 작동하려면 추가 설정이 필요합니다.

### 3.2 FastAPI의 비동기

FastAPI는 비동기를 완벽하게 지원합니다.

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/async-task")
async def async_task():
    await asyncio.sleep(1)
    return {"message": "Done"}
```

FastAPI는 ASGI 기반이므로 비동기가 네이티브입니다.

---

## 4. 의존성 관리

### 4.1 Flask의 의존성

Flask는 의존성 주입 기능이 없어서 수동으로 관리합니다.

```python
from flask import Flask

app = Flask(__name__)

def get_database():
    return Database()

@app.route("/items/")
def list_items():
    db = get_database()
    items = db.query(Item).all()
    return {"items": items}
```

### 4.2 FastAPI의 의존성

FastAPI는 내장된 의존성 주입 시스템이 있습니다.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_database():
    return Database()

@app.get("/items/")
async def list_items(db: Database = Depends(get_database)):
    items = db.query(Item).all()
    return {"items": items}
```

**장점:**
- 코드 재사용성 향상
- 테스트 용이 (Mock 주입 가능)
- 자동 문서화

---

## 5. 문서화

### 5.1 Flask의 문서화

Flask는 자동 API 문서화가 없습니다. Swagger 추가 설정 필요:

```python
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/items/<int:item_id>")
def get_item(item_id):
    """
    Get an item by ID
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Item data
    """
    return {"item_id": item_id}
```

### 5.2 FastAPI의 문서화

FastAPI는 자동으로 OpenAPI 문서를 생성합니다:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}", summary="Get item by ID")
async def get_item(item_id: int):
    """
    Get an item by its ID.

    - **item_id**: The ID of the item to retrieve
    """
    return {"item_id": item_id}
```

**자동 생성되는 문서:**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

추가 코드 필요 없음!

---

## 6. 성능 최적화

### 6.1 Flask의 병렬 처리

Flask는 동기 기반이므로 여러 워커 프로세스 필요:

```bash
# Gunicorn으로 4개 워커 실행
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 6.2 FastAPI의 병렬 처리

FastAPI는 비동기 이벤트 루프로 많은 동시 요청 처리 가능:

```bash
# Uvicorn으로 4개 워커 실행
uvicorn main:app --workers 4
```

**성능 차이:**
- Flask (4 워커): 초당 약 1000-2000 요청
- FastAPI (4 워커): 초당 약 10000+ 요청

---

## 7. 마이그레이션 체크리스트

Flask에서 FastAPI로 마이그레이션할 때 확인해야 할 사항:

### 기본 구조
- [ ] `@app.route()` → `@app.get()`, `@app.post()` 등으로 변경
- [ ] `request` 객체 사용 제거
- [ ] 함수 파라미터로 의존성 주입

### 데이터 처리
- [ ] Request body를 Pydantic 모델로 변환
- [ ] 수동 검증 제거 (Pydantic이 처리)
- [ ] `jsonify()` 제거 (자동 JSON 변환)

### 비동기
- [ ] 동기 함수 → `async def`로 변경
- [ ] I/O 작업은 `await` 사용

### 에러 처리
- [ ] 에러 핸들러 → `HTTPException` 사용
- [ ] 수동 상태 코드 → `status_code` 파라미터

---

## 8. Flask 개발자를 위한 팁

1. **타입 힌팅 사용하기**: FastAPI는 타입 힌팅을 활용하므로 습관 들이기
2. **Pydantic 배우기**: FastAPI의 강력한 검증 시스템 이해
3. **비동기 이해하기**: `async/await` 문법 숙달
4. **의존성 주입 활용하기**: 깔끔한 코드 작성
5. **자동 문서 활용하기**: 개발 중 `/docs` 확인

---

## 2.2 실전 실행 방식 비교

### 개발 환경에서의 실행

#### Flask
```bash
# 방법 1: Python에서 직접 실행
python app.py

# 방법 2: Flask CLI 사용
flask run --debug --port 8000

# 방법 3: Gunicorn 사용 (개발용)
gunicorn -w 1 -b 0.0.0.0:8000 --reload app:app
```

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"message": "Hello"}

if __name__ == "__main__":
    # 개발: 자동 리로드, 디버거 활성화
    app.run(debug=True, host="0.0.0.0", port=8000)
```

#### FastAPI
```bash
# 방법 1: FastAPI CLI (권장, v0.109+)
fastapi dev main.py

# 방법 2: Uvicorn 명령줄
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: Python에서 실행
python main.py
```

```python
# main.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello"}

if __name__ == "__main__":
    # 개발: 자동 리로드 활성화
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### 프로덕션 환경에서의 실행

#### Flask
```bash
# Gunicorn으로 여러 워커 실행
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Gunicorn + Nginx (권장)
# nginx.conf에서 uvicorn으로 프록시
upstream flask_app {
    server 127.0.0.1:8000;
}
```

```python
# app.py - 프로덕션
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
```

#### FastAPI
```bash
# Uvicorn으로 여러 워커 실행 (권장)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Gunicorn + Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

```python
# main.py - 프로덕션
if __name__ == "__main__":
    # 프로덕션: 여러 워커, 리로드 비활성화
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        reload=False,
        access_log=True
    )
```

### 환경 변수로 설정 관리

#### Flask
```python
import os
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False") == "True"
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))

    app.run(debug=debug, host=host, port=port)
```

```bash
# 실행
DEBUG=True HOST=0.0.0.0 PORT=8000 python app.py
```

#### FastAPI
```python
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    debug = os.getenv("DEBUG", "False") == "True"
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug,
        workers=workers if not debug else 1
    )
```

```bash
# 실행
DEBUG=True HOST=0.0.0.0 PORT=8000 WORKERS=4 python main.py
```

### Docker에서의 실행

#### Flask
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

#### FastAPI
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 요약 테이블

| 측면 | Flask | FastAPI |
|------|-------|---------|
| **개발 실행** | `app.run(debug=True)` | `uvicorn main:app --reload` |
| **프로덕션 서버** | Gunicorn | Uvicorn/Gunicorn |
| **멀티 워커** | Gunicorn의 `-w` 옵션 | Uvicorn의 `--workers` 옵션 |
| **자동 리로드** | `debug=True` | `--reload` 또는 `reload=True` |
| **HTTPS** | `ssl_context` | `ssl_keyfile/ssl_certfile` |
| **성능** | ~100-200 rps (1 worker) | ~1000+ rps (1 worker) |
| **비동기** | 제한적 | 완전 지원 |

**핵심 차이점:**
- Flask는 WSGI 기반으로 **Gunicorn** 필수
- FastAPI는 ASGI 기반으로 **Uvicorn** 사용
- FastAPI가 비동기 작업에 훨씬 효율적
- FastAPI는 적은 워커로 더 많은 동시 연결 처리 가능

---

## 요약

| 측면 | Flask | FastAPI |
|------|-------|---------|
| **적합한 경우** | 간단한 API, 프로토타입 | 고성능 프로덕션 API |
| **학습곡선** | 낮음 | 중간 |
| **성능** | 중간 | 높음 |
| **개발 속도** | 빠름 | 매우 빠름 |
| **자동 검증** | 없음 | 있음 (Pydantic) |
| **자동 문서화** | 없음 | 있음 |
| **비동기 지원** | 제한적 | 완전 지원 |

**결론**: FastAPI는 Flask의 개발 효율성과 Python의 모던한 기능(타입 힌팅, 비동기)을 결합하여 차세대 웹 프레임워크로 자리잡고 있습니다.
