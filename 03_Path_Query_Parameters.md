# 03. Path 파라미터와 Query 파라미터

API에서 클라이언트로부터 데이터를 받는 가장 기본적인 방법은 URL을 통하는 것입니다. 이 장에서는 Path 파라미터와 Query 파라미터를 배웁니다.

## 1. Path 파라미터

### 1.1 기본 개념

Path 파라미터는 URL 경로의 일부로 전달되는 파라미터입니다.

```
URL: /items/5
    ^^^^^^^ ↑
   경로   Path 파라미터
```

### 1.2 기본 사용법

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}
```

**요청:**
```
GET http://localhost:8000/items/42
```

**응답:**
```json
{"item_id": "42"}
```

**문제점:** `item_id`가 문자열로 반환됩니다.

### 1.3 타입 힌팅 추가

타입을 지정하면 FastAPI가 자동으로 변환하고 검증합니다.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**요청:**
```
GET http://localhost:8000/items/42
```

**응답:**
```json
{"item_id": 42}
```

**자동 기능:**
- 타입 변환: 문자열 → 정수
- 타입 검증: 정수가 아니면 오류 반환
- 자동 문서화: 타입 정보 표시

### 1.4 여러 Path 파라미터

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: int):
    return {"user_id": user_id, "item_id": item_id}
```

**요청:**
```
GET http://localhost:8000/users/1/items/42
```

**응답:**
```json
{"user_id": 1, "item_id": 42}
```

---

## 2. Path 파라미터 검증

### 2.1 Path() 사용법

Path 파라미터에 검증 규칙을 추가합니다.

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="Item ID", description="Item의 고유 ID")
):
    return {"item_id": item_id}
```

**Path() 파라미터:**
- `...` (또는 `Ellipsis`): 필수 파라미터
- `title`: 문서에서 사용할 제목
- `description`: 파라미터 설명

### 2.2 숫자 범위 검증

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., ge=1, le=1000)
):
    return {"item_id": item_id}
```

**검증 조건:**
- `ge`: Greater than or Equal (>=)
- `le`: Less than or Equal (<=)
- `gt`: Greater Than (>)
- `lt`: Less Than (<)

**테스트:**
```
# 유효한 요청
GET http://localhost:8000/items/500
응답: {"item_id": 500}

# 범위를 벗어난 요청 (422 Unprocessable Entity)
GET http://localhost:8000/items/2000
```

### 2.3 정규식 검증

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/files/{file_path}")
def read_file(
    file_path: str = Path(..., regex="^[a-zA-Z0-9_-]+\\.txt$")
):
    return {"file_path": file_path}
```

**정규식:** `.txt` 확장자를 가진 파일명만 허용

**테스트:**
```
# 유효
GET http://localhost:8000/files/document.txt

# 무효
GET http://localhost:8000/files/document.pdf
```

### 2.4 복잡한 검증

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(
    user_id: int = Path(..., ge=1, le=10000, title="User ID"),
    post_id: int = Path(..., ge=1, le=100000, title="Post ID")
):
    return {"user_id": user_id, "post_id": post_id}
```

---

## 3. Query 파라미터

### 3.1 기본 개념

Query 파라미터는 URL의 쿼리 문자열로 전달되는 파라미터입니다.

```
URL: /items?skip=0&limit=10
           ↑
    Query string
```

### 3.2 기본 사용법

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**요청:**
```
GET http://localhost:8000/items?skip=20&limit=5
```

**응답:**
```json
{"skip": 20, "limit": 5}
```

**특징:**
- 함수 파라미터에 기본값을 지정하면 선택적 파라미터
- 쿼리 문자열에서 해당 파라미터를 생략하면 기본값 사용
- 자동 타입 변환

### 3.3 선택적 Query 파라미터

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/items/")
def read_items(q: Optional[str] = None):
    return {"q": q}
```

또는 Union 사용:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(q: str | None = None):
    return {"q": q}
```

**테스트:**
```
# q 파라미터 제공
GET http://localhost:8000/items?q=foo
응답: {"q": "foo"}

# q 파라미터 생략
GET http://localhost:8000/items
응답: {"q": null}
```

### 3.4 필수 Query 파라미터

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(skip: int, limit: int):
    return {"skip": skip, "limit": limit}
```

**특징:**
- 기본값이 없으므로 필수
- 파라미터를 생략하면 422 오류 반환

---

## 4. Query 파라미터 검증

### 4.1 Query() 사용법

Query 파라미터에 검증 규칙을 추가합니다.

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
def read_items(
    q: str = Query(..., title="Query", description="검색어")
):
    return {"q": q}
```

### 4.2 문자열 길이 검증

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
def read_items(
    q: str = Query(..., min_length=3, max_length=50)
):
    return {"q": q}
```

**검증 조건:**
- `min_length`: 최소 길이
- `max_length`: 최대 길이

**테스트:**
```
# 유효 (길이 5)
GET http://localhost:8000/items?q=hello

# 무효 (길이 2 - 최소값 미만)
GET http://localhost:8000/items?q=hi
```

### 4.3 정규식 검증

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
def read_items(
    q: str = Query(..., regex="^[a-zA-Z0-9]+$")
):
    return {"q": q}
```

**정규식:** 영문자와 숫자만 허용

### 4.4 기본값이 있는 검증

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}
```

**특징:**
- 기본값 첫 번째 인자로 지정
- 범위 검증 추가
- 생략하면 기본값 사용

---

## 5. 리스트 Query 파라미터

### 5.1 중복 Query 파라미터

같은 이름의 파라미터를 여러 번 전달할 수 있습니다.

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/items/")
def read_items(q: List[str] = Query([])):
    return {"q": q}
```

**요청:**
```
GET http://localhost:8000/items?q=foo&q=bar&q=baz
```

**응답:**
```json
{"q": ["foo", "bar", "baz"]}
```

### 5.2 기본값이 있는 리스트

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/items/")
def read_items(q: List[str] = Query(["default1", "default2"])):
    return {"q": q}
```

### 5.3 정수 리스트

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/items/")
def read_items(ids: List[int] = Query(...)):
    return {"ids": ids}
```

**요청:**
```
GET http://localhost:8000/items?ids=1&ids=2&ids=3
```

**응답:**
```json
{"ids": [1, 2, 3]}
```

---

## 6. Path와 Query 파라미터 혼합

### 6.1 기본 혼합

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items")
def read_user_items(user_id: int, skip: int = 0, limit: int = 10):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }
```

**요청:**
```
GET http://localhost:8000/users/1/items?skip=5&limit=20
```

**응답:**
```json
{"user_id": 1, "skip": 5, "limit": 20}
```

### 6.2 명시적 Path와 Query

```python
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int = Path(..., ge=1, title="User ID"),
    item_id: int = Path(..., ge=1, title="Item ID"),
    q: str = Query(None, title="Query", min_length=1)
):
    return {
        "user_id": user_id,
        "item_id": item_id,
        "q": q
    }
```

---

## 7. 실습 예제

### 예제 1: 상품 검색 API

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(title="상품 검색 API")

# 샘플 데이터
items_db = [
    {"id": 1, "name": "Laptop", "price": 1000, "category": "electronics"},
    {"id": 2, "name": "Phone", "price": 500, "category": "electronics"},
    {"id": 3, "name": "Desk", "price": 200, "category": "furniture"},
    {"id": 4, "name": "Chair", "price": 150, "category": "furniture"},
]

@app.get("/items/")
def search_items(
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(10, ge=1, le=100, description="반환할 최대 항목 수"),
    category: Optional[str] = Query(None, description="카테고리 필터"),
    min_price: Optional[int] = Query(None, ge=0, description="최소 가격"),
    max_price: Optional[int] = Query(None, ge=0, description="최대 가격"),
):
    """
    상품을 검색합니다.

    **파라미터:**
    - **skip**: 건너뛸 항목 수 (기본값: 0)
    - **limit**: 반환할 최대 항목 수 (기본값: 10)
    - **category**: 카테고리로 필터링 (선택사항)
    - **min_price**: 최소 가격 필터 (선택사항)
    - **max_price**: 최대 가격 필터 (선택사항)
    """
    results = items_db

    # 카테고리 필터
    if category:
        results = [item for item in results if item["category"] == category]

    # 가격 범위 필터
    if min_price:
        results = [item for item in results if item["price"] >= min_price]

    if max_price:
        results = [item for item in results if item["price"] <= max_price]

    # 페이지네이션
    results = results[skip : skip + limit]

    return {
        "items": results,
        "total": len(results)
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """
    ID로 특정 상품을 조회합니다.
    """
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}
```

**테스트:**
```
# 모든 상품 조회
GET http://localhost:8000/items/

# 카테고리별 필터링
GET http://localhost:8000/items/?category=electronics

# 가격 범위 필터링
GET http://localhost:8000/items/?min_price=100&max_price=500

# 페이지네이션
GET http://localhost:8000/items/?skip=2&limit=2

# 특정 상품 조회
GET http://localhost:8000/items/1
```

### 예제 2: 사용자 페이지 API

```python
from fastapi import FastAPI, Path, Query
from typing import Optional

app = FastAPI(title="사용자 페이지 API")

users_db = [
    {"id": 1, "name": "Alice", "age": 25, "city": "Seoul"},
    {"id": 2, "name": "Bob", "age": 30, "city": "Busan"},
    {"id": 3, "name": "Charlie", "age": 35, "city": "Seoul"},
    {"id": 4, "name": "David", "age": 28, "city": "Daegu"},
    {"id": 5, "name": "Eve", "age": 32, "city": "Incheon"},
]

@app.get("/users/")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    city: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None, ge=0),
    sort_by: str = Query("id", regex="^(id|name|age|city)$"),
):
    """
    사용자 목록을 조회합니다.

    **정렬 옵션:** id, name, age, city
    """
    results = users_db

    # 필터링
    if city:
        results = [u for u in results if u["city"] == city]

    if min_age:
        results = [u for u in results if u["age"] >= min_age]

    if max_age:
        results = [u for u in results if u["age"] <= max_age]

    # 정렬
    results = sorted(results, key=lambda x: x[sort_by])

    # 페이지네이션
    total = len(results)
    results = results[skip : skip + limit]

    return {
        "users": results,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., ge=1, title="User ID")
):
    """
    특정 사용자를 조회합니다.
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}

@app.get("/users/by-name/{name}")
def get_user_by_name(
    name: str = Path(..., min_length=1, title="User Name")
):
    """
    이름으로 사용자를 조회합니다.
    """
    for user in users_db:
        if user["name"].lower() == name.lower():
            return user
    return {"error": "User not found"}
```

**테스트:**
```
# 모든 사용자 조회
GET http://localhost:8000/users/

# 도시별 필터링
GET http://localhost:8000/users/?city=Seoul

# 나이 범위 필터링
GET http://localhost:8000/users/?min_age=25&max_age=30

# 정렬
GET http://localhost:8000/users/?sort_by=name

# 페이지네이션
GET http://localhost:8000/users/?skip=2&limit=2

# 특정 사용자 조회
GET http://localhost:8000/users/1

# 이름으로 조회
GET http://localhost:8000/users/by-name/Alice
```

---

## 8. 일반적인 실수

### 8.1 Path와 Query 혼동

```python
# ❌ 잘못된 예
@app.get("/items/{item_id}")
def read_item(item_id: int = Query(...)):  # item_id는 Path여야 함
    return {"item_id": item_id}

# ✅ 올바른 예
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(...)):
    return {"item_id": item_id}
```

### 8.2 필수 vs 선택적 혼동

```python
# ❌ 필수 Query가 선택적으로 작동
@app.get("/items/")
def read_items(q):  # 기본값이 없으면 필수
    return {"q": q}

# ✅ 명시적으로 필수
@app.get("/items/")
def read_items(q: str = Query(...)):
    return {"q": q}

# ✅ 명시적으로 선택적
@app.get("/items/")
def read_items(q: str | None = Query(None)):
    return {"q": q}
```

### 8.3 타입 검증 놓치기

```python
# ❌ 타입 지정 없음
@app.get("/items/")
def read_items(skip, limit):
    return {"skip": skip, "limit": limit}

# ✅ 타입 지정
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

---

## 요약

### Path 파라미터
- URL 경로의 일부로 전달
- `{parameter_name}` 형식
- `Path()`로 검증 추가
- 보통 리소스 ID 전달

### Query 파라미터
- URL 쿼리 문자열로 전달
- `?name=value&foo=bar` 형식
- `Query()`로 검증 추가
- 보통 필터, 정렬, 페이지네이션 등

### 검증 옵션
- `ge`, `le`, `gt`, `lt`: 숫자 범위
- `min_length`, `max_length`: 문자열 길이
- `regex`: 정규식 패턴
- `title`, `description`: 문서화

**다음 장**: Request Body와 Pydantic 모델에 대해 배웁니다.
