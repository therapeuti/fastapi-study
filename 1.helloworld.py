# from flask import Flask, render_template, jsonify

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "hello flask"

# @app.route('/items/<int: item_id>')
# def get_item(item_id):
#     return f'item_id: {item_id}'

# @app.route('/')

# @app.route('/home')
# def home():
#     return render_template('index.html')


from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(debug=True, title='fastapi연습')

@app.get("/")
def index():
    return "hello fastapi"
    # return {'message': 'Hello, fastapi'}

@app.get("/json")
def get_json():
    return {"key": "value", "number": 42, "array": [1, 2, 3]}

@app.get("/list")
def get_list():
    return [1, 2, 3, 4, 5]

@app.get("/string")
def get_string():
    return "Hello World"

@app.get("/number")
def get_number():
    return 42

@app.get('/cart')
def get_cart_root():
    return HTMLResponse('<H1>장바구니 루트 페이지</H1>')

# path 파라미터
@app.get('/items/{item_id}')
def get_item(item_id: int = Path(..., gt=0)):
    return {'item_id': item_id}




if __name__=="__main__":
    # app.run(debug=True)
    uvicorn.run("helloworld:app", reload=True)

