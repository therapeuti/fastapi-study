from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from pydantic import BaseModel

class Todo(BaseModel):
    # id: int                 # 필수값
    todo: str               # 필수값
    status: bool = False    # 기본값 False


todolist = [{'todo': '투두리스트', 'status': False, 'id': 1}]
todo_id = 2



app = FastAPI(debug=True)

# 정적파일
app.mount('/static', StaticFiles(directory='static'), name='static')


# 페이지 렌더링
@app.get('/')
def index():
    return FileResponse('static/todolist.html')


# 투두리스트 조회
@app.get('/api/todo/')
def get_todo():
    return {'todolist': todolist}


# 투두리스트 추가
@app.post('/api/todo/')
def add_todolist(todo: Todo):
    global todo_id

    print(f'요청 들어온 데이터 : {todo}')
    todo = todo.dict()
    print(f'딕셔너리로 변경해줌 {todo}')

    todo['id'] = todo_id
    todo_id += 1
    print('다음 투두 아이디는? ', todo_id)
    print(f'id 추가 변경해줌 {todo}')

    todolist.append(todo)
    return {'todolist': todolist}

# 투두리스트 체크
@app.put('/api/todo/{todoid}')
def update_status(todoid: int):
    global todolist

    print(f'상태 변경할 투두 아이디 : {todoid}')
    for l in todolist:
        if todoid == l['id'] and l['status'] == True:
            l['status'] = False
        elif todoid == l['id'] and l['status'] == False:
            l['status'] = True
    
    print(f'상태 변경된 투두리스트 {todolist}')
    
    return {'todolist': todolist}



# 투두리스트 삭제
@app.delete('/api/todo/{todoid}')
def delete_todo(todoid: int):
    global todolist

    print(f'삭제할 투두 아이디 : {todoid}')

    todolist = [l for l in todolist if l['id'] != todoid]

    print(f'삭제 후 투두 리스트 {todolist}')
    return {'todolist' : todolist}






if __name__=='__main__':
    uvicorn.run('todolist:app', reload=True)