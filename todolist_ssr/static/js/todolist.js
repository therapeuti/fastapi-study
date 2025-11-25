// 미션1. /api/todo에 crud 추가
// GET /api/todo => 조회는 SSR로 진행
// POST /api/todo
// PUT /api/todo/${id}
// DELETE /api/todo/${id}



// 페이지 로드 시 투두리스트 조회

// 투두리스트 추가 -> 폼 제출 사용


// 투두리스트 상태변경
const todolist = document.getElementById('todo-list')
document.addEventListener('click', async (e) => {
    console.log('투두리스트 클릭')
    console.log(e.target.tagName)
    if (e.target.tagName == 'LI') {
        const li = e.target
        const id = e.target.dataset.id
        console.log('id : ', id)
        console.log(typeof(id))

        const response = await fetch(`/api/todo/${id}`, {
            method: 'PATCH',
            headers: {'content-type': 'application/json'}
        })

        if (response.ok) {
            // 서버에서 반환한 업데이트된 리스트로 화면 갱신
            const data = await response.json()
            console.log(data.status)
            li.className = data.status
        }
    }

    // 투두리스트 삭제
    else {
        console.log(e.target)
        const delBtn = e.target.closest('BUTTON')
        const id = delBtn.dataset.id
        const li = delBtn.closest('LI')
        console.log(delBtn)

        const response = await fetch(`/api/todo/${id}`, {
            method: 'Delete'
        })

        if (response.ok) {
            const data = await response.json()
            console.log('투두 개수 : ', data)
            console.log(li)
            li.remove()
            
            if (data == 0) {
                todolist.innerHTML = `
                <div class="empty-message">
                    <i class="bi bi-list-task"></i>
                    <h3>할 일이 없습니다</h3>
                    <p>새로운 할 일을 추가해보세요!</p>
                </div>`

            }

        }
    }
})


