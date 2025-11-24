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

## 실습 결과 (실제 테스트)

### 범위 검증 테스트

**엔드포인트:**
```python
@app.get("/reg")
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}
```

**테스트 1: skip=1, limit=1**
```bash
curl "http://localhost:8000/reg?skip=1&limit=1"
```
**응답:**
```json
{"skip": 1, "limit": 1}
```

**테스트 2: skip만 지정 (limit은 기본값)**
```bash
curl "http://localhost:8000/reg?skip=1"
```
**응답:**
```json
{"skip": 1, "limit": 10}
```

**테스트 3: 파라미터 없음 (모두 기본값)**
```bash
curl "http://localhost:8000/reg"
```
**응답:**
```json
{"skip": 0, "limit": 10}
```

**테스트 4: skip=10**
```bash
curl "http://localhost:8000/reg?skip=10"
```
**응답:**
```json
{"skip": 10, "limit": 10}
```

**테스트 5: limit이 범위 초과 (1004 > 100)**
```bash
curl "http://localhost:8000/reg?skip=1&limit=1004"
```
**응답 (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["query", "limit"],
      "msg": "Input should be less than or equal to 100",
      "input": "1004",
      "ctx": {"le": 100}
    }
  ]
}
```

**분석:**
- `limit` 파라미터가 최대값(100)을 초과하면 검증 오류 발생
- FastAPI가 자동으로 상세한 에러 메시지 제공

---

### 리스트 Query 파라미터 테스트

**엔드포인트:**
```python
from typing import List

@app.get('/list')
def get_list(q: List[str] = Query([])):
    return {'q': q}
```

**테스트 1: 파라미터 없음 (빈 리스트)**
```bash
curl "http://localhost:8000/list"
```
**응답:**
```json
{"q": []}
```

**테스트 2: 단일 값**
```bash
curl "http://localhost:8000/list?q=dgh"
```
**응답:**
```json
{"q": ["dgh"]}
```

**테스트 3: 쉼표로 구분된 값 (1개 항목으로 처리됨)**
```bash
curl "http://localhost:8000/list?q=dgh,dg,h,h,h,e"
```
**응답:**
```json
{"q": ["dgh,dg,h,h,h,e"]}
```
**주의:** 쉼표는 단순 문자열로 취급되며, 자동으로 분리되지 않습니다.

**테스트 4: 같은 파라미터 여러 번 전달 (올바른 방법)**
```bash
curl "http://localhost:8000/list?q=dgh&q=dg,h,h,h,e"
```
**응답:**
```json
{"q": ["dgh", "dg,h,h,h,e"]}
```

**분석:**
- 리스트 파라미터는 **같은 파라미터를 여러 번 전달**해야 함
- 쉼표로 구분하면 1개의 문자열로 처리됨
- 각 `q=값` 형태로 전달하면 리스트에 추가됨

---

### 필수 파라미터와 선택 파라미터 비교

#### 선택적 Query 파라미터 (기본값 있음)

**엔드포인트:**
```python
from typing import Optional

@app.get('/selected-items')
def read_items(q: Optional[str] = None):
    return {'q': q}
```

**테스트 1: 파라미터 제공**
```bash
curl "http://localhost:8000/selected-items?q=hello"
```
**응답:**
```json
{"q": "hello"}
```

**테스트 2: 파라미터 생략 (기본값 None)**
```bash
curl "http://localhost:8000/selected-items"
```
**응답:**
```json
{"q": null}
```

---

#### Python 3.10+ 문법 (str | None)

**엔드포인트:**
```python
@app.get('/optional-items')
def read_items2(q: str | None = None):
    return {'q': q}
```

**테스트:**
```bash
curl "http://localhost:8000/optional-items?q=test"
응답: {"q": "test"}

curl "http://localhost:8000/optional-items"
응답: {"q": null}
```

**분석:**
- `Optional[str]` = `str | None` (동일한 의미)
- Python 3.10 이후는 `str | None` 문법을 권장

---

### 필수 Query 파라미터 테스트 (Query(...))

**엔드포인트:**
```python
from typing import List
from fastapi import Query

@app.get('/integer-list')
def int_list(q: List[int] = Query(...)):
    return {'result': q}
```

**Query(...) 의미:**
- `...` (Ellipsis) = **필수 파라미터**
- 파라미터가 없으면 422 Unprocessable Entity 에러 발생

**테스트 1: 올바른 요청 (파라미터 제공)**
```bash
curl "http://localhost:8000/integer-list?q=1&q=2&q=3"
```
**응답:**
```json
{"result": [1, 2, 3]}
```

**테스트 2: 필수 파라미터 누락 (422 에러)**
```bash
curl "http://localhost:8000/integer-list"
```
**응답 (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "q"],
      "msg": "Field required"
    }
  ]
}
```

**분석:**
- `Query(...)` = 필수 파라미터 (파라미터 없으면 에러)
- `Query(None)` = 선택적 (None 기본값)
- `Query(기본값)` = 선택적 (지정한 기본값)

---

### 문자열 길이 검증

**엔드포인트:**
```python
@app.get('/query')
def query(q: str = Query(..., min_length=3, max_length=10)):
    return {'q': q}
```

**특징:**
- `...` = 필수 파라미터
- `min_length=3` = 최소 3글자
- `max_length=10` = 최대 10글자

**테스트 1: 올바른 길이 (5글자)**
```bash
curl "http://localhost:8000/query?q=hello"
```
**응답:**
```json
{"q": "hello"}
```

**테스트 2: 길이 초과 (15글자 > 최대 10글자)**
```bash
curl "http://localhost:8000/query?q=verylongstring"
```
**응답 (422 에러):**
```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["query", "q"],
      "msg": "String should have at most 10 characters",
      "input": "verylongstring",
      "ctx": {"max_length": 10}
    }
  ]
}
```

**분석:**
- 필수 파라미터 + 길이 검증 동시 적용
- FastAPI가 자동으로 입력값 검증

---

## 필수 vs 선택 파라미터 정리

| 표현식 | 필수 여부 | 기본값 | 설명 |
|--------|---------|-------|------|
| `q: str` | 필수 | 없음 | 필수 파라미터 |
| `q: str = None` | ❌ 타입 오류 | - | Optional 필요 |
| `q: Optional[str] = None` | 선택 | None | 선택적 (None) |
| `q: str \| None = None` | 선택 | None | 선택적 (최신 문법) |
| `q: str = Query(...)` | **필수** | 없음 | 필수 (Query 명시) |
| `q: str = Query(None)` | 선택 | None | 선택적 (Query로) |
| `q: str = Query("default")` | 선택 | "default" | 선택적 (기본값) |
| `q: List[str] = Query(...)` | **필수** | 없음 | 필수 리스트 |
| `q: List[str] = Query([])` | 선택 | [] | 선택적 리스트 |

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
