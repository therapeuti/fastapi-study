// 미션1. /api/todo에 crud 추가
// GET /api/todo
// POST /api/todo
// PUT /api/todo/${id}
// DELETE /api/todo/${id}

// fetch 시. 예외처리 해야함. try catch




get_todolist()

const todoinput = document.getElementById('todo-input')
const submit = document.getElementById('submit')

// 투두리스트 추가
submit.addEventListener('click', async (e) => {
    e.preventDefault();
    
    
    await fetch('/api/todo/', {
        method: 'post',
        headers: {'content-type':'application/json'},
        body: JSON.stringify(todoinput.value)
    })


    await get_todolist()
    todoinput.value = ''
})

document.addEventListener('click', (e) => {
    if ((e.target.tagName === 'LI') && (!e.target.classList.contains('del'))) {
        // 서버로 보내서 정보 수정하고 받아와서 적용
        console.log('클릭: ', e.target)
        updateStatus(e.target.dataset.id);
        get_todolist()
    }

    const delButton = e.target.closest('button.del');
    if (delButton) {
        console.log('삭제 버튼 누름')

        deleteTodo(delButton.dataset.id)  
        get_todolist()      
    }
})


async function get_todolist() {
    const response = await fetch('/api/todo/');
    const data = await response.json();
    console.log(data.todolist);

    addTodolist(data.todolist)
}

function addTodolist(todolist) {
    const todoList = document.getElementById('todo-list')
    todoList.innerHTML = ''

    if (todolist.length === 0) {
        todoList.innerHTML = `
            <div class="empty-message">
                <i class="bi bi-list-task"></i>
                <h3>할 일이 없습니다</h3>
                <p>새로운 할 일을 추가해보세요!</p>
            </div>
        `;
        return;
    }

    for (todo of todolist){
        const li = document.createElement('li')
        li.innerText = todo.todo;
        li.classList.add(todo.status)
        li.dataset.id = todo.id

        const delBtn = document.createElement('button')
        delBtn.classList.add('del')
        delBtn.innerHTML = '<i class="bi bi-trash3"></i>'
        delBtn.dataset.id = todo.id
        li.appendChild(delBtn)
        
        todoList.appendChild(li)
    }
}


async function updateStatus(todoid) {
    console.log(todoid)
    const response = await fetch(`/api/todo/${todoid}`,{
        method: 'put',
        headers: {'content-type':'application/json'},
        body: JSON.stringify(todoid)
    })

}

async function deleteTodo(todoid) {
    console.log(todoid)
    await fetch(`/api/todo/${todoid}`, {
        method: 'delete',
        headers: {'content-type':'application/json'},
    })
}