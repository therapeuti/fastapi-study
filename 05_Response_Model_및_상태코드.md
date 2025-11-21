# 05. Response Model과 상태 코드

이 장에서는 응답 데이터를 구조화하고 적절한 HTTP 상태 코드를 반환하는 방법을 배웁니다.

## 1. Response Model 기초

### 1.1 Response Model이란?

Response Model은 API가 반환하는 응답 데이터의 구조를 정의합니다.

**주요 이점:**
- 응답 데이터 검증
- 응답 데이터 필터링
- 자동 문서화
- 타입 힌팅

### 1.2 기본 사용법

```python
from fastapi import FastAPI
from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """
    ItemResponse 형식으로 응답합니다.
    """
    return {
        "id": item_id,
        "name": "Laptop",
        "price": 1500,
        "internal_notes": "This should not be returned"
    }
```

**요청:**
```
GET http://localhost:8000/items/1
```

**응답:**
```json
{"id": 1, "name": "Laptop", "price": 1500}
```

**주의:** `internal_notes`는 응답에 포함되지 않습니다. (필터링됨)

---

## 2. 다양한 Response Model

### 2.1 Request와 Response 모델 분리

```python
from fastapi import FastAPI
from pydantic import BaseModel

# Request 모델 (클라이언트가 보내는 데이터)
class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

# Response 모델 (서버가 반환하는 데이터)
class Item(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    created_at: str

app = FastAPI()

@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate):
    """
    ItemCreate를 받아 Item 형식으로 응답합니다.
    """
    return {
        "id": 1,
        "name": item.name,
        "price": item.price,
        "description": item.description,
        "created_at": "2024-01-01T12:00:00"
    }
```

### 2.2 리스트 응답

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

@app.get("/items/", response_model=List[Item])
async def list_items():
    """
    Item 리스트로 응답합니다.
    """
    return [
        {"id": 1, "name": "Laptop", "price": 1500},
        {"id": 2, "name": "Mouse", "price": 50},
    ]
```

### 2.3 선택적 응답

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float

app = FastAPI()

@app.get("/items/{item_id}", response_model=Item | None)
async def get_item(item_id: int):
    """
    Item 또는 None을 응답합니다.
    """
    if item_id == 1:
        return {"id": 1, "name": "Laptop", "price": 1500}
    return None
```

---

## 3. 응답 모델 고급 기능

### 3.1 exclude로 필드 제외

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float
    cost: float  # 내부용 필드

app = FastAPI()

@app.get("/items/{item_id}", response_model=Item, response_model_exclude={"cost"})
async def get_item(item_id: int):
    """
    cost 필드를 제외하고 응답합니다.
    """
    return {
        "id": item_id,
        "name": "Laptop",
        "price": 1500,
        "cost": 1000
    }
```

**응답:**
```json
{"id": 1, "name": "Laptop", "price": 1500}
```

### 3.2 include로 필드 포함

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float
    description: str

app = FastAPI()

@app.get("/items/{item_id}", response_model_include={"id", "name", "price"})
async def get_item(item_id: int):
    """
    id, name, price 필드만 응답합니다.
    """
    return {
        "id": item_id,
        "name": "Laptop",
        "price": 1500,
        "description": "High-performance laptop"
    }
```

### 3.3 네스트된 exclude/include

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Address

app = FastAPI()

@app.get(
    "/users/{user_id}",
    response_model_exclude={"address": {"zip_code"}}
)
async def get_user(user_id: int):
    """
    address.zip_code를 제외하고 응답합니다.
    """
    return {
        "id": user_id,
        "name": "Alice",
        "email": "alice@example.com",
        "address": {
            "street": "123 Main St",
            "city": "Seoul",
            "zip_code": "12345"
        }
    }
```

---

## 4. HTTP 상태 코드

### 4.1 상태 코드 기본

HTTP 상태 코드는 요청의 결과를 나타냅니다.

**주요 상태 코드:**
- `2xx`: 성공
- `3xx`: 리다이렉션
- `4xx`: 클라이언트 오류
- `5xx`: 서버 오류

### 4.2 status_code 파라미터

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item_data: dict):
    """
    201 Created 상태 코드로 응답합니다.
    """
    return item_data

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    204 No Content 상태 코드로 응답합니다.
    """
    return None
```

### 4.3 자주 사용되는 상태 코드

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

# 200 OK - GET 요청 성공
@app.get("/items/", status_code=status.HTTP_200_OK)
async def list_items():
    return {"items": []}

# 201 Created - 리소스 생성 성공
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# 204 No Content - 응답 본문 없음
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None

# 206 Partial Content - 부분 콘텐츠
@app.get("/items/", status_code=status.HTTP_206_PARTIAL_CONTENT)
async def list_items_partial():
    return {"items": []}

# 400 Bad Request - 잘못된 요청
@app.post("/items/validate", status_code=status.HTTP_400_BAD_REQUEST)
async def validate_item(item: Item):
    if item.price < 0:
        return {"error": "Price cannot be negative"}
    return item

# 401 Unauthorized - 인증 필요
@app.get("/private", status_code=status.HTTP_401_UNAUTHORIZED)
async def get_private():
    return {"error": "Authentication required"}

# 403 Forbidden - 접근 권한 없음
@app.get("/admin", status_code=status.HTTP_403_FORBIDDEN)
async def get_admin():
    return {"error": "Access forbidden"}

# 404 Not Found - 리소스를 찾을 수 없음
@app.get("/items/{item_id}", status_code=status.HTTP_404_NOT_FOUND)
async def get_item(item_id: int):
    return {"error": "Item not found"}

# 500 Internal Server Error - 서버 오류
@app.get("/error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
async def get_error():
    return {"error": "Internal server error"}
```

### 4.4 상태 코드 상수

FastAPI에서 제공하는 주요 상태 코드:

```python
from fastapi import status

# 2xx 성공
status.HTTP_200_OK = 200
status.HTTP_201_CREATED = 201
status.HTTP_202_ACCEPTED = 202
status.HTTP_204_NO_CONTENT = 204

# 3xx 리다이렉션
status.HTTP_301_MOVED_PERMANENTLY = 301
status.HTTP_302_FOUND = 302
status.HTTP_304_NOT_MODIFIED = 304
status.HTTP_307_TEMPORARY_REDIRECT = 307

# 4xx 클라이언트 오류
status.HTTP_400_BAD_REQUEST = 400
status.HTTP_401_UNAUTHORIZED = 401
status.HTTP_403_FORBIDDEN = 403
status.HTTP_404_NOT_FOUND = 404
status.HTTP_409_CONFLICT = 409
status.HTTP_422_UNPROCESSABLE_ENTITY = 422

# 5xx 서버 오류
status.HTTP_500_INTERNAL_SERVER_ERROR = 500
status.HTTP_502_BAD_GATEWAY = 502
status.HTTP_503_SERVICE_UNAVAILABLE = 503
```

---

## 5. 응답 헤더

### 5.1 Response에 헤더 추가

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/items/")
async def get_items():
    """
    커스텀 헤더를 포함하여 응답합니다.
    """
    return JSONResponse(
        content={"items": []},
        headers={"X-Custom-Header": "Custom Value"}
    )
```

### 5.2 path operation에서 헤더 지정

```python
from fastapi import FastAPI

app = FastAPI()

@app.get(
    "/items/",
    headers={"X-Custom-Header": "Custom Value"}
)
async def get_items():
    """
    응답에 커스텀 헤더를 포함합니다.
    """
    return {"items": []}
```

---

## 6. 실제 예제

### 예제 1: 상품 CRUD API

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="상품 관리 API")

# Request 모델
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)

# Response 모델
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: datetime

# 데이터베이스
items_db = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 1500,
        "created_at": datetime.now()
    }
]

# GET - 모든 상품 조회
@app.get("/items/", response_model=List[Item], status_code=status.HTTP_200_OK)
async def list_items():
    """
    모든 상품을 조회합니다.
    """
    return items_db

# GET - 특정 상품 조회
@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    """
    특정 상품을 조회합니다.
    """
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

# POST - 상품 생성
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """
    새로운 상품을 생성합니다.
    """
    new_item = {
        "id": max([i["id"] for i in items_db]) + 1 if items_db else 1,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "created_at": datetime.now()
    }
    items_db.append(new_item)
    return new_item

# PUT - 상품 수정
@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def update_item(item_id: int, item: ItemCreate):
    """
    상품 정보를 수정합니다.
    """
    for i, db_item in enumerate(items_db):
        if db_item["id"] == item_id:
            updated_item = {
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "created_at": db_item["created_at"]
            }
            items_db[i] = updated_item
            return updated_item
    return {"error": "Item not found"}

# DELETE - 상품 삭제
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    상품을 삭제합니다.
    """
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            items_db.pop(i)
            return None
    return {"error": "Item not found"}
```

### 예제 2: 사용자 프로필 API

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI(title="사용자 프로필 API")

# Internal 모델 (DB에 저장되는 정보)
class UserDB(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str  # 비공개
    is_admin: bool  # 비공개
    created_at: datetime
    updated_at: datetime

# Public 모델 (API 응답)
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

# Request 모델
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(...)
    password: str = Field(..., min_length=8)

users_db = []

# 공개 프로필 조회
@app.get(
    "/users/{user_id}",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int):
    """
    사용자 공개 정보를 조회합니다.
    비공개 정보는 필터링됩니다.
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}

# 사용자 등록
@app.post(
    "/users/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate):
    """
    새로운 사용자를 등록합니다.
    """
    new_user = {
        "id": len(users_db) + 1,
        "username": user.username,
        "email": user.email,
        "password_hash": "hashed_password",  # 실제로는 해싱 필요
        "is_admin": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    users_db.append(new_user)
    return new_user
```

---

## 7. 조건부 상태 코드

### 7.1 상황에 따른 다른 상태 코드

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    """
    상황에 따라 다른 상태 코드를 반환합니다.
    """
    # 가격이 1000 이상이면 특별 처리
    if item.price >= 1000:
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"message": "High-value item pending approval"}
        )

    # 일반적인 상품은 201 반환
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=item.model_dump()
    )
```

---

## 8. 모범 사례

### 8.1 일관된 응답 구조

```python
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None

class Item(BaseModel):
    id: int
    name: str

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    일관된 응답 구조로 반환합니다.
    """
    # 성공
    return ResponseWrapper[Item](
        success=True,
        message="Item retrieved successfully",
        data=Item(id=item_id, name="Laptop")
    )

@app.get("/items/not-found/{item_id}")
async def get_item_not_found(item_id: int):
    """
    에러 응답도 동일한 구조입니다.
    """
    return ResponseWrapper[Item](
        success=False,
        message="Item not found",
        error=f"No item with id {item_id}"
    )
```

### 8.2 성공 응답

```python
# 읽기 작업 (GET)
@app.get("/items/", status_code=status.HTTP_200_OK)

# 쓰기 작업 (POST) - 새 리소스 생성
@app.post("/items/", status_code=status.HTTP_201_CREATED)

# 삭제 작업 (DELETE) - 응답 본문 없음
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)

# 긴 작업 (비동기 처리)
@app.post("/tasks/", status_code=status.HTTP_202_ACCEPTED)
```

---

## 요약

### Response Model의 역할
- 응답 데이터 검증
- 필드 필터링 및 선택
- 자동 문서화
- 타입 안정성

### HTTP 상태 코드
- `200 OK`: 성공적인 GET
- `201 Created`: 리소스 생성 성공
- `204 No Content`: 응답 본문 없음
- `400 Bad Request`: 클라이언트 오류
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스 없음
- `500 Internal Server Error`: 서버 오류

### 모범 사례
- Request와 Response 모델 분리
- 적절한 상태 코드 사용
- 일관된 응답 구조
- 비공개 필드 필터링

**다음 장**: 에러 핸들링에 대해 배웁니다.
