<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>第八课复习</title>
    <style>
        .done{
            color:gray;
            text-decoration: line-through;
        }
    </style>
</head>
<body>
    <div class="todo-mian">
        <!-- todo输入框-->
        <div class="todo-form">
            <input id="id-input-todo" type="text">
            <button id = 'id-button-add' type="button">Add</button>
        </div>
        <!-- todo列表-->
        <div id="id-div-container">
             <!-- <div class='todo-cell'>
                    <button class='todo-done'>完成</button>
                    <button class='todo-delete'>删除</button>
                    <span contenteditable='true'>上课</span>
                </div> -->
        </div>
    </div>
<script>
var log = function () {
    console.log.apply(console,arguments)
}

var todoList = []

var addButton = document.querySelector('#id-button-add')
addButton.addEventListener('click',function () {
    var todoInput = document.querySelector('#id-input-todo')
    var task = todoInput.value
    //生成todo对象
    var todo = {
        'task':task,
        'time':currentTime()
    }
    todoList.push(todo)
    saveTodos()     //?
    insertTodo(todo)    //?
})

var templateTodo = function(todo) {
    var t = `
        <div class='todo-cell'>
            <button class='todo-done'>完成</button>
            <button class='todo-delete'>删除</button>
            <span contenteditable='true'>${todo.task}</span>
            <span>${todo.time}</span>
        </div>
    `
    return t
}

//事件委托
var todoContainer = document.querySelector('#id-div-container')

todoContainer.addEventListener('keydown',function (event) {
    log('container keydown', event, event.target)
    var target = event.target
    if(event.key ==='Enter'){
        log('按了回车')
        target.blur()
        event.preventDefault()
        var index = indexOfElement(target)
        log('update index',  index)
        // 把元素在 todoList 中更新
        todoList[index].task = target.innerHTML
        // todoList.splice(index, 1)
        saveTodos()
    }
})

todoContainer.addEventListener('click',function (event) {
    log('container click', event, event.target)
    var target = event.target
    if(target.classList.contains('todo-done')){
        log('done')
        var todoDiv = target.parentElement
        toggleClass(todoDiv,'done')
    }else if(target.classList.contains('todo-delete')){
        log('delete')
        var todoDiv = target.parentElement
        var index = indexOfElement(target)
        todoDiv.remove()
        // 把元素从 todoList 中 remove 掉
        // delete todoList[index]
        todoList.splice(index, 1)
        saveTodos()
    }
})

var saveTodos = function () {
    var s = localStorage.todoList
    return JSON.parse(s)
}

//返回自己在父元素中的下标
var indexOfElement = function (element) {
    var parent = element.parentElement
    for (var i = 0 ; i<parent.children.length;i++){
        var e = parent.children[i]
        if(e===element){
            return i
        }
    }
}


var toggleClass = function (element,className) {
    if(element.classList.contains(className)){
        element.classList.remove(className)
    }else{
        element.classList.add(className)
    }
}


todoList = loadTodos()
for (var i = 0; i < todoList.length; i++) {
    var todo = todoList[i]
    insertTodo(todo)
</script>

</body>
</html>