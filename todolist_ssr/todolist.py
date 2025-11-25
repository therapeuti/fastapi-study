from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
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
new_id = 2

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('todolist.html', {
        'request': request,
        'title': '마이 투두리스트',
        'todolist': todolist
    })


# 투두리스트 추가
@app.post('/api/todo')
def get_todo(todo: str = Form()):
    global new_id
    print(f'추가된 투두 {todo}, 투두 아이디 {new_id}')

    new_todo = Todo(
        id = new_id,
        todo = todo,
        status = False
    )
    print(f'new todo {new_todo}')
    todo_dict = new_todo.dict()
    print(f'딕셔너리로 변경 {todo_dict}')

    todolist.append(todo_dict)
    new_id += 1
    return RedirectResponse(url='/', status_code=303)

# 투두리스트 상태 수정
@app.patch('/api/todo/{todoid}')
def modify_status(todoid: int):
    global todolist
    print(f'상태 수정할 투두 아이디 : {todoid}')

    for l in todolist:
        if l['id'] == todoid:
            l['status'] = not l['status']
            todo = l
            print(todo)
    
    print(todolist)

    return todo

# 투두리스트 삭제
@app.delete('/api/todo/{todoid}')
def delete_todo(todoid: int):
    global todolist
    print(f'삭제할 아이디 : {todoid}')

    todolist = [ todo for todo in todolist if todo['id'] != todoid]
    print(todolist)

    return len(todolist)



if __name__=='__main__':
    uvicorn.run('todolist:app', reload=True)