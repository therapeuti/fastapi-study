from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# request & response 모델
class Todo(BaseModel):
    id: int | None = None
    todo: str
    status: bool = False


app = FastAPI(debug=True)
app.mount('/static', StaticFiles(directory='static'), name='static')

# templates 폴더에서 템플릿 로드
templates = Jinja2Templates(directory='templates')


todolist = [{'id': 1, 'todo': '투두리스트', 'status': False}]


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('todolist.html', {
        'request': request,
        'title': '마이 투두리스트',
        'todolist': todolist
    })


# 투두리스트 추가
@app.post('/api/todo')
def get_todo(todo):
    
    return

# 투두리스트 상태 수정
@app.patch('/api/todo')
def modify_status(todoid: int):
    return

# 투두리스트 삭제





if __name__=='__main__':
    uvicorn.run('todolist:app', reload=True)