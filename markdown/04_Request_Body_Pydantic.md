# 04. Request Body와 Pydantic 모델

FastAPI의 가장 강력한 기능 중 하나는 Pydantic을 이용한 자동 데이터 검증입니다. 이 장에서는 Request Body 처리와 Pydantic 모델 사용법을 배웁니다.

## 1. Pydantic 모델 기초

### 1.1 Pydantic이란?

Pydantic은 Python 데이터 검증 라이브러리입니다.

- 타입 힌팅을 이용한 자동 검증
- JSON 직렬화/역직렬화
- 타입 강제 및 자동 변환
- 상세한 에러 메시지

### 1.2 첫 번째 Pydantic 모델

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
```

**특징:**
- `BaseModel` 상속
- 필드 타입 선언
- 기본값 없으면 필수 필드

### 1.3 FastAPI에서 사용

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

**요청:**
```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 1000}'
```

**응답:**
```json
{"name": "Laptop", "price": 1000}
```

---

## 2. Pydantic 모델 필드

### 2.1 기본값 설정

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str                      # 필수
    description: str | None = None # 선택적
    price: float                   # 필수
    tax: float | None = None       # 선택적
```

**테스트:**
```json
// 최소 요청 (필수 필드만)
{
  "name": "Laptop",
  "price": 1000
}

// 모든 필드 포함
{
  "name": "Laptop",
  "description": "High-end laptop",
  "price": 1000,
  "tax": 100
}
```

### 2.2 기본값이 있는 필드

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tax: float = 0.0           # 기본값 있는 필수 필드
    in_stock: bool = True      # 기본값 있는 필드
    category: str = "general"  # 기본값 있는 필드
```

### 2.3 선택적 필드

```python
from typing import Optional
from pydantic import BaseModel

# 방법 1: Optional
class Item(BaseModel):
    name: str
    description: Optional[str] = None

# 방법 2: Union (Python 3.10+)
class Item(BaseModel):
    name: str
    description: str | None = None
```

---

## 3. Field를 이용한 고급 검증

### 3.1 Field() 기본 사용

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., title="Item Name", description="Item의 이름")
    price: float = Field(..., title="Price", description="Item의 가격")
```

### 3.2 문자열 검증

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(None, max_length=500)
    sku: str = Field(..., pattern="^[A-Z]{3}-[0-9]{4}$")
```

**검증 조건:**
- `min_length`, `max_length`: 길이 제한
- `pattern`: 정규식 패턴

### 3.3 숫자 검증

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    price: float = Field(..., gt=0, le=1000000)      # 0 < price <= 1000000
    quantity: int = Field(..., ge=1, le=10000)       # 1 <= quantity <= 10000
    discount: float = Field(0, ge=0, le=0.99)        # 0 <= discount <= 0.99
```

**검증 조건:**
- `gt`: Greater Than (>)
- `ge`: Greater than or Equal (>=)
- `lt`: Less Than (<)
- `le`: Less than or Equal (<=)

### 3.4 복잡한 검증

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(
        ...,
        title="Item Name",
        description="Item의 이름 (1-100 글자)",
        min_length=1,
        max_length=100
    )
    price: float = Field(
        ...,
        title="Price",
        description="Item의 가격 (0 초과)",
        gt=0
    )
    quantity: int = Field(
        0,
        title="Quantity",
        description="재고 수량",
        ge=0,
        le=10000
    )
```

---

## 4. Validator를 이용한 커스텀 검증

### 4.1 field_validator 사용

```python
from pydantic import BaseModel, field_validator

class Item(BaseModel):
    name: str
    price: float

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
```

### 4.2 여러 필드 검증

```python
from pydantic import BaseModel, field_validator

class Item(BaseModel):
    name: str
    price: float
    discount: float

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v

    @field_validator("discount")
    @classmethod
    def discount_must_be_valid(cls, v):
        if not (0 <= v <= 1):
            raise ValueError("Discount must be between 0 and 1")
        return v
```

### 4.3 모델 검증

```python
from pydantic import BaseModel, model_validator

class Item(BaseModel):
    name: str
    price: float
    discount: float

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount >= 1:
            raise ValueError("Discount cannot be 100% or more")
        return self
```

---

## 5. 중첩된 모델

### 5.1 기본 중첩

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    age: int
    address: Address
```

**요청:**
```json
{
  "name": "Alice",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "Seoul",
    "country": "Korea"
  }
}
```

### 5.2 선택적 중첩 모델

```python
from pydantic import BaseModel

class Contact(BaseModel):
    email: str
    phone: str | None = None

class User(BaseModel):
    name: str
    contact: Contact | None = None
```

### 5.3 리스트 중첩

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    order_id: int
    items: List[Item]
    total_price: float
```

**요청:**
```json
{
  "order_id": 1,
  "items": [
    {"name": "Laptop", "price": 1000},
    {"name": "Mouse", "price": 50}
  ],
  "total_price": 1050
}
```

---

## 6. 실제 예제

### 예제 1: 사용자 회원가입 API

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
import re

app = FastAPI(title="사용자 회원가입 API")

class User(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="사용자명 (3-20 글자)"
    )
    email: str = Field(
        ...,
        description="이메일 주소"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="비밀번호 (8글자 이상)"
    )
    age: int = Field(
        ...,
        ge=18,
        le=150,
        description="나이 (18-150)"
    )
    phone: str | None = Field(
        None,
        pattern="^[0-9]{10,11}$",
        description="전화번호 (선택사항)"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

@app.post("/register")
async def register_user(user: User):
    """
    사용자를 등록합니다.
    """
    return {
        "message": "User registered successfully",
        "user": user
    }
```

**테스트:**
```bash
# 유효한 요청
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "age": 25,
    "phone": "01012345678"
  }'

# 무효한 요청 (비밀번호 너무 짧음)
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "short",
    "age": 25
  }'
```

### 예제 2: 상품 생성 API

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="상품 관리 API")

class Tag(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str | None = None

class Image(BaseModel):
    url: str
    alt: str | None = None

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, title="상품명")
    description: str | None = Field(None, max_length=500, title="설명")
    price: float = Field(..., gt=0, title="가격")
    tax: float | None = Field(None, ge=0, title="세금")
    tags: List[str] = Field(default=[], title="태그")
    images: List[Image] | None = None
    in_stock: bool = True

items_db = []

@app.post("/items/")
async def create_item(item: Item):
    """
    새로운 상품을 생성합니다.
    """
    items_db.append(item)
    return {
        "message": "Item created",
        "item": item
    }

@app.get("/items/")
async def list_items():
    """
    모든 상품을 조회합니다.
    """
    return {"items": items_db}
```

**요청 예시:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 1500,
  "tax": 150,
  "tags": ["electronics", "computers"],
  "images": [
    {
      "url": "https://example.com/laptop.jpg",
      "alt": "Laptop image"
    }
  ],
  "in_stock": true
}
```

### 예제 3: 블로그 포스트 API

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

app = FastAPI(title="블로그 API")

class Comment(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.now)

class Post(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    author: str = Field(..., min_length=1, max_length=100)
    tags: List[str] = Field(default=[], max_length=10)
    published: bool = False
    comments: List[Comment] = Field(default=[])
    views: int = Field(default=0, ge=0)

posts_db = []

@app.post("/posts/")
async def create_post(post: Post):
    """
    새로운 포스트를 생성합니다.
    """
    posts_db.append(post)
    return {
        "message": "Post created",
        "post": post
    }

@app.post("/posts/{post_id}/comments/")
async def add_comment(post_id: int, comment: Comment):
    """
    포스트에 댓글을 추가합니다.
    """
    if 0 <= post_id < len(posts_db):
        posts_db[post_id].comments.append(comment)
        return {
            "message": "Comment added",
            "comment": comment
        }
    return {"error": "Post not found"}

@app.get("/posts/")
async def list_posts():
    """
    모든 포스트를 조회합니다.
    """
    return {"posts": posts_db}
```

---

## 7. 모델 설정

### 7.1 Config 클래스

```python
from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "price": 1500,
                "description": "A powerful laptop"
            }
        }
    )

    name: str
    price: float
    description: str | None = None
```

### 7.2 예제 데이터

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(
        ...,
        example="Laptop"
    )
    price: float = Field(
        ...,
        example=1500.00
    )
    description: str | None = Field(
        None,
        example="A powerful laptop for work"
    )
```

---

## 8. 타입 변환

### 8.1 자동 타입 변환

Pydantic은 요청 데이터를 자동으로 변환합니다.

```python
from pydantic import BaseModel

class Item(BaseModel):
    price: float
    quantity: int

# 요청
{
  "price": "19.99",  # 문자열
  "quantity": "5"    # 문자열
}

# 변환 후
Item(price=19.99, quantity=5)
```

### 8.2 지원하는 타입

```python
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class Example(BaseModel):
    name: str                    # 문자열
    age: int                     # 정수
    height: float                # 부동소수점
    is_active: bool              # 불린
    created_at: datetime         # 날짜시간
    birth_date: date            # 날짜
    tags: list                   # 리스트
    metadata: dict               # 딕셔너리
    user_id: UUID               # UUID
```

---

## 9. 모델 메서드

### 9.1 model_dump()

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

item = Item(name="Laptop", price=1500)

# 딕셔너리로 변환
item_dict = item.model_dump()
# {'name': 'Laptop', 'price': 1500}

# JSON 직렬화 가능한 딕셔너리
item_json_dict = item.model_dump(mode="json")
```

### 9.2 model_dump_json()

```python
from pydantic import BaseModel
import json

class Item(BaseModel):
    name: str
    price: float

item = Item(name="Laptop", price=1500)

# JSON 문자열로 변환
json_str = item.model_dump_json()
# '{"name":"Laptop","price":1500}'

# 포맷팅
json_str_pretty = item.model_dump_json(indent=2)
```

### 9.3 model_construct()

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

# 검증 없이 모델 생성 (성능 최적화)
item = Item.model_construct(name="Laptop", price=1500)
```

---

## 10. 일반적인 실수

### 10.1 필수 vs 선택적 혼동

```python
# ❌ 잘못됨 - price가 선택적으로 해석될 수 있음
class Item(BaseModel):
    name: str
    price = 100  # 타입 힌팅 없음

# ✅ 올바름 - price는 필수
class Item(BaseModel):
    name: str
    price: float

# ✅ 올바름 - price는 기본값이 100
class Item(BaseModel):
    name: str
    price: float = 100
```

### 10.2 None 타입 혼동

```python
# ❌ 잘못됨 - None을 전달할 수 없음
class Item(BaseModel):
    description: str

# ✅ 올바름 - None을 전달할 수 있음
class Item(BaseModel):
    description: str | None = None
```

### 10.3 모델 재사용 안함

```python
# ❌ 잘못됨 - 중복 코드
@app.post("/items/")
def create_item(name: str, price: float, description: str | None = None):
    return {"name": name, "price": price, "description": description}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float, description: str | None = None):
    return {"item_id": item_id, "name": name, "price": price, "description": description}

# ✅ 올바름 - 모델 재사용
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

---

## 11. HTML Form 데이터 전송

### 11.1 Form 데이터란?

HTML `<form>` 요소에서 제출되는 데이터는 기본적으로 `application/x-www-form-urlencoded` 또는 `multipart/form-data` 형식으로 전송됩니다.

### 11.2 Form 데이터 받기 (URLencoded)

**HTML:**
```html
<form method="POST" action="/submit">
    <input type="text" name="username" placeholder="사용자명">
    <input type="password" name="password" placeholder="비밀번호">
    <button type="submit">제출</button>
</form>
```

**FastAPI 백엔드:**
```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/submit")
async def submit_form(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}
```

**설명:**
- `Form(...)`: HTML Form 데이터를 받음
- `...`: 필수 필드

### 11.3 여러 Form 필드

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    newsletter: bool = Form(False)
):
    return {
        "username": username,
        "email": email,
        "password": password,
        "age": age,
        "newsletter": newsletter
    }
```

### 11.4 Form + Pydantic 모델 (권장)

**문제:** Form 필드가 많으면 매개변수가 너무 많아짐

**해결:** Pydantic 모델을 사용하되, 각 필드에 `Form()` 지정

```python
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    age: int
    newsletter: bool = False

# ❌ 이렇게 하면 안 됨 (JSON Body 형식을 기대함)
# @app.post("/register")
# async def register(user: UserRegistration):
#     return user

# ✅ 올바른 방법: 각 필드를 Form으로 지정
@app.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    newsletter: bool = Form(False)
):
    user = UserRegistration(
        username=username,
        email=email,
        password=password,
        age=age,
        newsletter=newsletter
    )
    return user
```

### 11.5 Pydantic 모델 직접 사용 (더 간단)

**FastAPI 0.109+에서 가능:**
```python
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    age: int
    newsletter: bool = False

@app.post("/register")
async def register(user: UserRegistration = Form(...)):
    return user
```

### 11.6 파일 업로드 + Form 데이터

```python
from fastapi import FastAPI, Form, File, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    return {
        "name": name,
        "filename": file.filename,
        "content_type": file.content_type
    }
```

**HTML:**
```html
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="text" name="name" placeholder="이름">
    <input type="file" name="file">
    <button type="submit">업로드</button>
</form>
```

### 11.7 Form vs JSON Body

| 방식 | Content-Type | 용도 | 예시 |
|------|-------------|------|------|
| **Form** | application/x-www-form-urlencoded | HTML Form 제출 | 로그인, 회원가입 |
| **JSON** | application/json | API 요청 | fetch API, REST 클라이언트 |
| **Multipart** | multipart/form-data | 파일 업로드 | 이미지, 문서 업로드 |

### 11.8 실제 예제: TODO 추가 (Form)

**HTML:**
```html
<form method="POST" action="/api/todo/add">
    <input type="text" name="todo" placeholder="할 일 입력" required>
    <input type="hidden" name="status" value="false">
    <button type="submit">추가</button>
</form>
```

**FastAPI:**
```python
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse

app = FastAPI()
todolist = []
todo_id = 1

@app.post("/api/todo/add")
async def add_todo(todo: str = Form(...), status: str = Form(...)):
    global todo_id
    new_todo = {
        "id": todo_id,
        "todo": todo,
        "status": status.lower() == "true"
    }
    todolist.append(new_todo)
    todo_id += 1
    return RedirectResponse(url="/", status_code=303)  # 페이지 새로고침
```

### 11.9 Form + JavaScript fetch (JSON 전송)

**HTML:**
```html
<form id="todo-form">
    <input type="text" id="todo-input" placeholder="할 일 입력" required>
    <button type="submit">추가</button>
</form>
```

**JavaScript:**
```javascript
document.getElementById('todo-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const todoInput = document.getElementById('todo-input');
    const todoValue = todoInput.value;

    // Form 데이터를 JSON으로 변환해서 전송
    await fetch('/api/todo/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            todo: todoValue,
            status: false
        })
    });

    todoInput.value = '';
    location.reload();
});
```

**FastAPI (JSON 받음):**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TodoCreate(BaseModel):
    todo: str
    status: bool = False

@app.post("/api/todo/")
async def add_todo(todo: TodoCreate):
    # JSON 형식으로 받음
    return {"created": todo}
```

---

## 요약

### Pydantic 모델의 장점
- 자동 타입 검증
- 자동 타입 변환
- 상세한 에러 메시지
- 중첩된 모델 지원
- JSON 직렬화/역직렬화
- 자동 문서화

### 주요 기능
- `BaseModel`: 기본 모델 클래스
- `Field()`: 필드 검증 및 메타데이터
- `field_validator()`: 커스텀 필드 검증
- `model_validator()`: 모델 수준 검증
- `model_dump()`: 딕셔너리로 변환
- `model_dump_json()`: JSON 문자열로 변환
- `Form()`: HTML Form 데이터 받기

### 데이터 전송 방식
- **Form**: HTML `<form>` 제출 (SSR 방식)
- **JSON**: JavaScript fetch (REST API 방식)
- **Multipart**: 파일 업로드

**다음 장**: Response Model과 상태 코드에 대해 배웁니다.
