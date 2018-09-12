var log = function () {
    console.log.apply(console,arguments)
}

var e = function (sel) {
    return document.querySelector(sel)
}

//ajax函数

var ajax = function (method,path,data,respinseCallback) {
    var r = new XMLHttpRequest()
    r.open(method,path,true)
    r.setRequestHeader('Content-Type','application/json')
    r.onreadystatechange = function () {
        if(r.readyState === 4){
            respinseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// TODO API
// 获取所有 todo
var apiTodoAll = function (callback) {
    var path = '/api/todo/all'
    ajax('GET',path,'',callback)
}

//增加一个 todo
var apiTodoAdd = function (form,callback) {
    var path = '/api/todo/add'
    ajax('GET',path,form,callback)
}

//删除一个 todo
var apiTodoDelete = function (id,callback) {
    var path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
    //    get(path, callback)
}

//更新一个 todo
var apiTodoUpdate = function (form,callback) {
    var path = '/api/todo/update'
    ajax('POST',path,form,callback)
    // post(path,form,callback)
}

//load weibo all
var apiWeiboAll = function (callback) {
    var path = '/api/weibo/all'
    ajax('GET',path,'',callback)
}

//增加一个 todo
var apiWeiboAdd = function (form,callback) {
    var path = '/api/weibo/add'
    ajax('POST',path,form,callback)
}