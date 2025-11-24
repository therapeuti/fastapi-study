from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(debug=True, title='fastapi docs에 뜨는 타이틀')

@app.get('/')
def index():
    return HTMLResponse('<H1> path 파라미터, query 파라미터 사용하기 </H1>')


@app.get('/cart/{user_id}')
def get_cart(user_id: str): # 타입 힌팅
    return {'user_id': user_id}

@app.get('/items/{item_id}')
def get_item(item_id: int = Path(..., ge=1, le=1000)): # path 파라미터 검증, 필수 파라미터 ... , 1~1000
    return {'item_id': item_id}



# query 파라미터

#from flask import request
#item_id = request.args.get('item_id')


@app.get('/items')
def get_item2(item_a : int = 1, item_b : int = 2):  # 타입 힌팅, 디폴트 값
    # 첫 번째 변수에 기본값 넣으면 다음 변수도 기본값있어야 함.
    # ✅ 올바른 순서
    # def func(a, b=0):  # a는 필수, b는 선택
    # def func(a: int, b: int = 0):  # 타입도 지정

    # ❌ 잘못된 순서
    # def func(a=0, b):  # SyntaxError!
    
    return {'item_id': item_a + item_b}


# 선택적 query 파라미터

from typing import Optional

@app.get('/selected-items')
def read_items(q: Optional[str] = None):
    return {'q': q}

@app.get('/optional-items')
def read_items2(q: str | None = None):
    return {'q' : q}


# 검증 규칙 추가
from fastapi import Query

@app.get('/query')
def query(q: str = Query(..., min_length=3, max_length=10)): #문자열 길이 검증
    return {'q': q}


@app.get("/reg") # 정규식 검증
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}

from typing import List

@app.get('/list')
def get_list(q: List[str] = Query([])):
    return {'q': q}

@app.get('/integer-list')
# def int_list(q: List[int] = Query([10])): # 기본값 10
# def int_list(q: List[int] = Query(None)): # 기본값 없음
def int_list(q: List[int] = Query(...)): #필수값 : 필수로 파라미터를 입력해야함
    return {'result': q}

if __name__=='__main__':
    uvicorn.run('2_path_query_param:app', reload=True)