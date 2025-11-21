# FastAPI 학습 계획

## 1. FastAPI 소개

### 주요 특징
- **고성능**: Starlette과 Pydantic 기반의 빠른 프레임워크
- **개발 속도 향상**: 200-300% 빠른 개발 속도
- **버그 감소**: 개발자 오류 약 40% 감소
- **직관적**: 뛰어난 편집기 지원과 자동완성
- **표준 기반**: OpenAPI, JSON Schema 완벽 호환

---

## 2. 학습 로드맵

### Phase 1: 기본 개념 (1-2주)
1. 환경 설정 및 첫 API 만들기
2. Path Parameters
3. Query Parameters
4. Request Body
5. Response Model

### Phase 2: 중급 개념 (2-3주)
6. 데이터 검증 (Validation)
7. Pydantic 모델 심화
8. 에러 핸들링
9. 의존성 주입 (Dependency Injection)
10. 미들웨어

### Phase 3: 고급 개념 (3-4주)
11. 인증 및 보안
12. 데이터베이스 연동
13. 백그라운드 태스크
14. WebSocket
15. 배포 및 최적화

---

## 3. 필수 모듈 및 함수

### 3.1 핵심 모듈

#### FastAPI
```python
from fastapi import FastAPI

app = FastAPI()
```
- **FastAPI**: 메인 애플리케이션 클래스
- 모든 API의 시작점

#### Pydantic
```python
from pydantic import BaseModel, Field, validator
```
- **BaseModel**: 데이터 모델 정의
- **Field**: 필드 검증 및 메타데이터
- **validator**: 커스텀 검증 로직

#### 라우팅 데코레이터
```python
@app.get()      # GET 요청
@app.post()     # POST 요청
@app.put()      # PUT 요청
@app.delete()   # DELETE 요청
@app.patch()    # PATCH 요청
```

### 3.2 요청 처리 모듈

```python
from fastapi import (
    Path,          # Path 파라미터 검증
    Query,         # Query 파라미터 검증
    Body,          # Request Body 검증
    Header,        # HTTP 헤더
    Cookie,        # 쿠키
    Form,          # Form 데이터
    File,          # 파일 업로드
    UploadFile,    # 파일 업로드 (향상된 버전)
)
```

### 3.3 응답 처리

```python
from fastapi import Response, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    StreamingResponse,
)
```

### 3.4 에러 핸들링

```python
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
```

### 3.5 의존성 주입

```python
from fastapi import Depends
```

### 3.6 보안

```python
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBearer,
)
```

---

## 4. 기본 개념 상세 설명

### 4.1 첫 번째 FastAPI 애플리케이션

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**핵심 요소:**
- `FastAPI()`: 애플리케이션 인스턴스 생성
- `@app.get("/")`: GET 메서드로 "/" 경로 정의
- `async def`: 비동기 함수 (일반 함수도 가능)
- 반환값: 자동으로 JSON으로 변환

**실행 방법:**
```bash
# 개발 모드
fastapi dev main.py

# 프로덕션 모드
fastapi run main.py

# 또는 uvicorn 직접 사용
uvicorn main:app --reload
```

**자동 문서:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI Schema: `http://127.0.0.1:8000/openapi.json`

### 4.2 Path Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**검증 추가:**
```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="Item ID", ge=1, le=1000)
):
    return {"item_id": item_id}
```

**파라미터:**
- `...`: 필수 파라미터
- `title`: 문서화용 제목
- `ge`: greater than or equal (>=)
- `le`: less than or equal (<=)
- `gt`: greater than (>)
- `lt`: less than (<)

### 4.3 Query Parameters

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**검증 추가:**
```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    q: str | None = Query(None, min_length=3, max_length=50)
):
    return {"q": q}
```

**파라미터:**
- `None`: 선택적 파라미터
- `min_length`, `max_length`: 문자열 길이 제한
- `regex`: 정규식 패턴 매칭

### 4.4 Request Body (Pydantic 모델)

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**고급 검증:**
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    tax: float | None = Field(None, ge=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
```

### 4.5 Response Model

```python
class ItemResponse(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    # DB 저장 로직 등
    return item
```

**장점:**
- 응답 데이터 필터링
- 자동 검증
- 자동 문서화

---

## 5. 필수 함수 및 개념

### 5.1 비동기 vs 동기

```python
# 비동기 (I/O 작업이 많을 때)
@app.get("/async")
async def async_endpoint():
    result = await some_async_function()
    return result

# 동기 (CPU 집약적 작업)
@app.get("/sync")
def sync_endpoint():
    result = some_sync_function()
    return result
```

### 5.2 상태 코드

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None
```

### 5.3 에러 핸들링

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in database:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Custom error header"},
        )
    return {"item_id": item_id}
```

### 5.4 의존성 주입

```python
from fastapi import Depends

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

---

## 6. 학습 체크리스트

### Week 1-2: 기초
- [ ] FastAPI 설치 및 환경 설정
- [ ] 첫 API 만들기 (Hello World)
- [ ] Path Parameters 이해
- [ ] Query Parameters 이해
- [ ] Request Body (Pydantic) 기초
- [ ] 자동 문서 활용법 익히기

### Week 3-4: 중급
- [ ] Pydantic 모델 심화
- [ ] 데이터 검증 (Field, validator)
- [ ] Response Model 활용
- [ ] HTTPException 에러 처리
- [ ] 의존성 주입 기초

### Week 5-6: 실전
- [ ] 데이터베이스 연동 (SQLAlchemy)
- [ ] 인증/인가 구현 (JWT)
- [ ] 파일 업로드/다운로드
- [ ] CORS 설정
- [ ] 미들웨어 활용

### Week 7-8: 고급
- [ ] Background Tasks
- [ ] WebSocket
- [ ] Testing (pytest)
- [ ] Docker 배포
- [ ] 성능 최적화

---

## 7. 추천 실습 프로젝트

### 프로젝트 1: TODO API
- CRUD 기본 구현
- Pydantic 모델 활용
- 데이터 검증 연습

### 프로젝트 2: 블로그 API
- 사용자 인증
- 게시글 CRUD
- 댓글 기능
- 파일 업로드

### 프로젝트 3: 실시간 채팅 API
- WebSocket 활용
- 실시간 메시징
- 사용자 관리

---

## 8. 유용한 리소스

### 공식 문서
- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- Pydantic 문서: https://docs.pydantic.dev/

### 추가 학습 자료
- FastAPI GitHub: https://github.com/tiangolo/fastapi
- FastAPI 튜토리얼: https://fastapi.tiangolo.com/tutorial/

### 필수 패키지
```bash
pip install "fastapi[standard]"  # FastAPI + 기본 의존성
pip install uvicorn[standard]    # ASGI 서버
pip install sqlalchemy           # ORM
pip install python-jose[cryptography]  # JWT
pip install passlib[bcrypt]      # 비밀번호 해싱
pip install python-multipart     # Form, File 업로드
```

---

## 9. 다음 단계

1. **환경 설정**: 가상환경 생성 및 FastAPI 설치
2. **첫 API 만들기**: `main.py` 생성 및 실행
3. **공식 튜토리얼 따라하기**: 순차적으로 학습
4. **실습 프로젝트 진행**: 실전 경험 쌓기
5. **코드 리뷰 및 개선**: 베스트 프랙티스 적용

---

**학습 목표**: 8주 안에 실무에서 사용 가능한 FastAPI 백엔드 개발 능력 습득
