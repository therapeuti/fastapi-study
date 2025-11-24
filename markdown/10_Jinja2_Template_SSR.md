# FastAPI에서 Jinja2 템플릿을 이용한 SSR (Server-Side Rendering)

## 📚 학습 목표
- Jinja2 템플릿 엔진 이해하기
- FastAPI에서 템플릿 설정하기
- SSR을 통한 동적 HTML 렌더링
- 템플릿 상속과 블록 활용
- 템플릿에서 데이터 처리

---

## 1️⃣ SSR (Server-Side Rendering)이란?

### 정의
서버에서 HTML을 완전히 렌더링하여 클라이언트에게 전송하는 방식입니다.

### SSR vs CSR 비교

| 항목 | SSR | CSR |
|------|-----|-----|
| 렌더링 위치 | 서버 | 클라이언트(브라우저) |
| 초기 로딩 속도 | 빠름 | 느림 |
| SEO | 좋음 | 나쁨 |
| 서버 부하 | 높음 | 낮음 |
| 상호작용성 | 낮음 | 높음 |
| 예시 | 전통 웹사이트 | React, Vue SPA |

### FastAPI에서 SSR을 하는 이유
- 전통적인 웹 애플리케이션 구축 (게시판, 블로그 등)
- SEO가 중요한 경우
- 빠른 초기 페이지 로딩이 필요한 경우

---

## 2️⃣ Jinja2 템플릿 엔진

### Jinja2란?
Flask와 Django에서도 사용하는 파이썬 템플릿 엔진입니다.

### 설치
```bash
pip install jinja2
```

### FastAPI에서 Jinja2 설정
```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

# templates 폴더에서 템플릿 로드
templates = Jinja2Templates(directory="templates")
```

---

## 3️⃣ 기본 사용법

### 1단계: 템플릿 파일 생성

**templates/index.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ message }}</h1>
    <p>{{ content }}</p>
</body>
</html>
```

### 2단계: 라우트에서 템플릿 렌더링

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "홈페이지",
        "message": "환영합니다!",
        "content": "이것은 Jinja2 템플릿입니다."
    })
```

### 3단계: 브라우저에서 확인
```
http://localhost:8000/
```

---

## 4️⃣ Jinja2 템플릿 문법

### 변수 출력
```html
<!-- 변수 출력 -->
<p>{{ variable_name }}</p>

<!-- 속성 접근 -->
<p>{{ user.name }}</p>

<!-- 딕셔너리 접근 -->
<p>{{ data['key'] }}</p>
```

### 조건문 (if)
```html
{% if user.is_admin %}
    <p>관리자입니다.</p>
{% elif user.is_moderator %}
    <p>모더레이터입니다.</p>
{% else %}
    <p>일반 사용자입니다.</p>
{% endif %}
```

### 반복문 (for)
```html
<ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
</ul>
```

### 필터
```html
<!-- 대문자 변환 -->
<p>{{ name | upper }}</p>

<!-- 소문자 변환 -->
<p>{{ name | lower }}</p>

<!-- 길이 -->
<p>항목 개수: {{ items | length }}</p>

<!-- 기본값 설정 -->
<p>{{ username | default("Anonymous") }}</p>

<!-- 조인 -->
<p>{{ tags | join(", ") }}</p>
```

### 주석
```html
{# 이 부분은 렌더링되지 않습니다 #}
```

---

## 5️⃣ 템플릿 상속

### 개념
기본 템플릿을 만들고 자식 템플릿이 상속받아 확장하는 방식입니다.

### 기본 템플릿 (base.html)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}기본 제목{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <header>
        <h1>My Website</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
        </nav>
    </header>

    <main>
        {% block content %}
            기본 콘텐츠
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 My Website</p>
    </footer>
</body>
</html>
```

### 자식 템플릿 (home.html)
```html
{% extends "base.html" %}

{% block title %}홈페이지{% endblock %}

{% block content %}
    <h2>환영합니다!</h2>
    <p>이것은 홈페이지입니다.</p>
{% endblock %}
```

### 자식 템플릿 (about.html)
```html
{% extends "base.html" %}

{% block title %}소개{% endblock %}

{% block content %}
    <h2>소개</h2>
    <p>이것은 소개 페이지입니다.</p>
{% endblock %}
```

### FastAPI 라우트
```python
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
```

---

## 6️⃣ 실전 예제

### 상황: 사용자 목록과 상세 페이지 표시

#### 1. base.html (기본 레이아웃)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}사용자 관리{% endblock %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        a { color: #0066cc; }
    </style>
</head>
<body>
    <header>
        <h1>사용자 관리 시스템</h1>
    </header>

    {% block content %}{% endblock %}
</body>
</html>
```

#### 2. users.html (사용자 목록)
```html
{% extends "base.html" %}

{% block title %}사용자 목록{% endblock %}

{% block content %}
    <h2>사용자 목록</h2>

    {% if users %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>이름</th>
                    <th>이메일</th>
                    <th>상태</th>
                    <th>액션</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>
                            {% if user.is_active %}
                                <span style="color: green;">활성</span>
                            {% else %}
                                <span style="color: red;">비활성</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="/users/{{ user.id }}">상세보기</a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>사용자가 없습니다.</p>
    {% endif %}
{% endblock %}
```

#### 3. user_detail.html (사용자 상세)
```html
{% extends "base.html" %}

{% block title %}{{ user.name }} - 상세정보{% endblock %}

{% block content %}
    <h2>{{ user.name }} 상세정보</h2>

    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
        <p><strong>ID:</strong> {{ user.id }}</p>
        <p><strong>이름:</strong> {{ user.name }}</p>
        <p><strong>이메일:</strong> {{ user.email }}</p>
        <p><strong>나이:</strong> {{ user.age }}</p>
        <p><strong>상태:</strong>
            {% if user.is_active %}
                <span style="color: green;">활성</span>
            {% else %}
                <span style="color: red;">비활성</span>
            {% endif %}
        </p>
        <p><strong>가입일:</strong> {{ user.created_at }}</p>
    </div>

    <div style="margin-top: 20px;">
        <a href="/users">← 사용자 목록으로 돌아가기</a>
    </div>
{% endblock %}
```

#### 4. FastAPI 앱 (app.py)
```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 더미 데이터
users_db = [
    {
        "id": 1,
        "name": "김철수",
        "email": "kim@example.com",
        "age": 28,
        "is_active": True,
        "created_at": "2024-01-15"
    },
    {
        "id": 2,
        "name": "이영희",
        "email": "lee@example.com",
        "age": 32,
        "is_active": True,
        "created_at": "2024-02-20"
    },
    {
        "id": 3,
        "name": "박민수",
        "email": "park@example.com",
        "age": 25,
        "is_active": False,
        "created_at": "2024-03-10"
    }
]

@app.get("/users")
def list_users(request: Request):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users_db
    })

@app.get("/users/{user_id}")
def get_user(user_id: int, request: Request):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return {"error": "사용자를 찾을 수 없습니다"}

    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "user": user
    })
```

---

## 7️⃣ 주의사항

### 1. Request 객체는 필수
```python
# ❌ 잘못된 예
return templates.TemplateResponse("index.html", {
    "title": "제목"
})

# ✅ 올바른 예
return templates.TemplateResponse("index.html", {
    "request": request,
    "title": "제목"
})
```

### 2. 템플릿 경로
```python
# FastAPI 실행 위치에서 templates 폴더가 있어야 함
# 프로젝트 구조:
# project/
# ├── app.py
# ├── templates/
# │   ├── base.html
# │   └── index.html
```

### 3. 정적 파일 제공
```python
from fastapi.staticfiles import StaticFiles

# CSS, JavaScript, 이미지 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿에서 사용
# <link rel="stylesheet" href="/static/style.css">
```

---

## 8️⃣ 자주 사용하는 필터 모음

| 필터 | 설명 | 예시 |
|------|------|------|
| `upper` | 대문자 변환 | `{{ 'hello' \| upper }}` → HELLO |
| `lower` | 소문자 변환 | `{{ 'HELLO' \| lower }}` → hello |
| `length` | 길이 | `{{ items \| length }}` → 5 |
| `default` | 기본값 | `{{ name \| default('Anonymous') }}` |
| `join` | 문자열 연결 | `{{ tags \| join(', ') }}` |
| `replace` | 문자열 치환 | `{{ 'hello' \| replace('l', 'L') }}` → heLLo |
| `first` | 첫 번째 요소 | `{{ items \| first }}` |
| `last` | 마지막 요소 | `{{ items \| last }}` |
| `reverse` | 역순 | `{{ items \| reverse }}` |
| `sort` | 정렬 | `{{ items \| sort }}` |
| `abs` | 절댓값 | `{{ -5 \| abs }}` → 5 |
| `round` | 반올림 | `{{ 3.14159 \| round(2) }}` → 3.14 |

---

## 9️⃣ 정리

### 핵심 개념
1. **SSR**: 서버에서 HTML을 렌더링하여 전송
2. **Jinja2**: 파이썬 템플릿 엔진
3. **TemplateResponse**: FastAPI에서 템플릿을 렌더링하는 방식
4. **상속**: base.html로 공통 레이아웃 관리
5. **필터**: 데이터 포맷팅 및 변환

### 언제 사용?
- 전통적인 웹 애플리케이션
- SEO가 중요한 경우
- 서버에서 완전히 렌더링된 페이지 필요 시

### 다음 단계
- 폼 처리 (POST 요청)
- 데이터베이스와 연동
- 세션 및 인증
