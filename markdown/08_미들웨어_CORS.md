# 08. 미들웨어와 CORS

미들웨어는 모든 요청과 응답을 처리할 수 있는 함수입니다. 이 장에서는 미들웨어와 CORS(Cross-Origin Resource Sharing)를 배웁니다.

## 1. 미들웨어 개념

### 1.1 미들웨어란?

미들웨어는 요청이 엔드포인트에 도달하기 전에, 그리고 응답이 클라이언트로 반환되기 전에 실행되는 함수입니다.

```
요청 → [미들웨어] → 라우팅 → [엔드포인트] → [미들웨어] → 응답
```

### 1.2 기본 미들웨어

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

app = FastAPI()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        모든 요청과 응답을 로깅합니다.
        """
        # 요청 전
        start_time = time.time()
        print(f"[{request.method}] {request.url.path}")

        # 엔드포인트 실행
        response = await call_next(request)

        # 응답 후
        process_time = time.time() - start_time
        print(f"응답 시간: {process_time:.3f}초")

        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(LoggingMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

**출력:**
```
[GET] /items/
응답 시간: 0.001초
```

---

## 2. 미들웨어 활용

### 2.1 요청 헤더 추가

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        모든 응답에 커스텀 헤더를 추가합니다.
        """
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "Custom Value"
        return response

app.add_middleware(CustomHeaderMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

### 2.2 요청 검증

```python
from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        모든 요청에 인증을 확인합니다.
        """
        auth_header = request.headers.get("authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header required"
            )

        # 인증 검증 로직
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header"
            )

        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

### 2.3 응답 시간 추적

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        응답 시간을 추적합니다.
        """
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"Method={request.method} Path={request.url.path} "
            f"Status={response.status_code} Time={process_time:.3f}s"
        )

        return response

app.add_middleware(PerformanceMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

---

## 3. CORS (Cross-Origin Resource Sharing)

### 3.1 CORS 개념

CORS는 웹 애플리케이션이 다른 도메인의 리소스에 접근할 수 있게 해주는 메커니즘입니다.

**예시:**
- 프론트엔드: `http://frontend.example.com`
- 백엔드: `http://api.example.com`

프론트엔드에서 백엔드로 요청을 보낼 때 CORS 설정이 필요합니다.

### 3.2 기본 CORS 설정

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용 (개발 환경에서만 사용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

**주의:** `allow_origins=["*"]`는 개발 환경에서만 사용하고, 프로덕션 환경에서는 명시적으로 도메인을 지정합니다.

### 3.3 특정 도메인만 허용

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 특정 도메인만 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://example.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

### 3.4 환경별 CORS 설정

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 환경에 따라 다른 CORS 설정
if os.getenv("ENVIRONMENT") == "development":
    origins = ["*"]
else:
    origins = [
        "https://example.com",
        "https://www.example.com"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

### 3.5 CORS 파라미터 설명

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `allow_origins` | 허용할 오리진 | `["http://localhost:3000"]` |
| `allow_credentials` | 쿠키 전송 허용 | `True` / `False` |
| `allow_methods` | 허용할 HTTP 메서드 | `["GET", "POST"]` |
| `allow_headers` | 허용할 헤더 | `["*"]` 또는 특정 헤더 |
| `expose_headers` | 클라이언트에 노출할 헤더 | `["X-Custom-Header"]` |
| `max_age` | 프리플라이트 캐시 시간(초) | `600` |

---

## 4. 프리플라이트 요청

### 4.1 프리플라이트 요청이란?

특정 조건에서 브라우저는 실제 요청 전에 OPTIONS 메서드로 프리플라이트 요청을 보냅니다.

**프리플라이트 요청이 발생하는 경우:**
- Content-Type이 `application/json`
- 커스텀 헤더 사용
- PUT, DELETE 등의 메서드

### 4.2 프리플라이트 요청 처리

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600  # 프리플라이트 캐시 1시간
)

@app.post("/items/")
async def create_item(item: dict):
    return item

# 클라이언트 요청
# 1. OPTIONS 프리플라이트 요청 (자동 처리됨)
# 2. POST 실제 요청
```

---

## 5. 실전 예제

### 예제 1: 로깅 미들웨어

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

app = FastAPI()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        요청 로깅 미들웨어입니다.
        """
        # 요청 정보
        request_id = str(datetime.now().timestamp())
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"from {request.client.host}"
        )

        # 요청 본문 로깅 (POST/PUT)
        if request.method in ["POST", "PUT"]:
            body = await request.body()
            logger.info(f"[{request_id}] Body: {body.decode()}")

        response = await call_next(request)

        # 응답 정보
        logger.info(f"[{request_id}] Response Status: {response.status_code}")

        return response

app.add_middleware(RequestLoggingMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}

@app.post("/items/")
async def create_item(item: dict):
    return item
```

### 예제 2: API 버전 미들웨어

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import re

app = FastAPI()

class APIVersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        API 버전을 확인합니다.
        """
        # API 버전 헤더에서 추출
        api_version = request.headers.get("X-API-Version", "1.0")

        # 버전 검증
        if not re.match(r"^\d+\.\d+$", api_version):
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid API version format"}
            )

        # 지원 버전 확인
        supported_versions = ["1.0", "2.0"]
        if api_version not in supported_versions:
            return JSONResponse(
                status_code=400,
                content={"detail": f"API version {api_version} is not supported"}
            )

        response = await call_next(request)
        response.headers["X-API-Version"] = api_version
        return response

app.add_middleware(APIVersionMiddleware)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

### 예제 3: 인증 미들웨어와 CORS

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# 인증 미들웨어
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        모든 /api/ 경로에 대해 인증을 확인합니다.
        """
        if request.url.path.startswith("/api/"):
            token = request.headers.get("Authorization")

            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header required"
                )

            if not token.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header"
                )

            # 토큰 검증 (실제로는 JWT 검증)
            token_value = token.replace("Bearer ", "")
            if token_value != "valid_token":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)

# 공개 엔드포인트
@app.get("/")
async def read_root():
    return {"message": "Public endpoint"}

# 보호된 엔드포인트
@app.get("/api/items/")
async def read_items():
    return {"items": []}

@app.post("/api/items/")
async def create_item(item: dict):
    return item
```

**테스트:**
```bash
# 공개 엔드포인트
curl http://localhost:8000/

# 보호된 엔드포인트 (토큰 필요)
curl -H "Authorization: Bearer valid_token" http://localhost:8000/api/items/

# CORS 프리플라이트 요청
curl -X OPTIONS http://localhost:8000/api/items/ \
  -H "Origin: http://localhost:3000"
```

---

## 6. 미들웨어 순서

### 6.1 미들웨어 실행 순서

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class MiddlewareA(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("A - Request in")
        response = await call_next(request)
        print("A - Response out")
        return response

class MiddlewareB(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("B - Request in")
        response = await call_next(request)
        print("B - Response out")
        return response

# 마지막에 추가된 미들웨어가 먼저 실행됨
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)

# 실행 순서:
# B - Request in
# A - Request in
# [엔드포인트]
# A - Response out
# B - Response out
```

---

## 7. CORS 문제 해결

### 7.1 CORS 에러 디버깅

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

app = FastAPI()

class CORSDebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Origin: {request.headers.get('origin')}")
        print(f"Method: {request.method}")
        print(f"Headers: {dict(request.headers)}")

        response = await call_next(request)
        return response

app.add_middleware(CORSDebugMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/")
async def read_items():
    return {"items": []}
```

---

## 요약

### 미들웨어의 역할
- 모든 요청과 응답 처리
- 로깅, 인증, 검증 등
- 요청/응답 헤더 조작
- 성능 모니터링

### CORS 설정
- `allow_origins`: 허용할 도메인
- `allow_methods`: 허용할 HTTP 메서드
- `allow_headers`: 허용할 헤더
- 환경별로 다른 설정 사용

### 실전 팁
- 프로덕션에서는 specific domains 사용
- 미들웨어 순서에 주의
- CORS와 인증 미들웨어 함께 사용
- 성능 영향 고려

**다음 장**: 인증과 보안에 대해 배웁니다.
