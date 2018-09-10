from utils import log
from todo import Todo
from models import User
from routes import current_user

def template(name):
    #根据名字读取 templates 文件夹里的一个文件并返回
    path = 'templates/' + name
    with open(path,'r',encoding='utf-8') as f:
        return f.read()

def response_with_headers(headers,code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}:{}\r\n'.format(k,v) for k,v in headers.items()])
    return header

def redirect(url):
    headers = {
        'Location':url,
    }
    r = response_with_headers(headers,302) + '\r\n'
    return r.encode('utf-8')

def login_required(route_function):
    def f(request):
        uname =current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return f

def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{}:{}{}{}</h3>'.format(t.id,t.title,edit_link,delete_link)
        todos.append(s)
        todo_html = ''.join(todos)
        body = template('todo_index.html')
        body = body.replace('{{todos}}',todo_html)
        header = response_with_headers(headers)
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')

def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = int(request.query.get('id',-1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}',str(t.id))
    body = body.replace('{{todo_title}}'),str(t.title)
    header = response_with_headers(headers)
    r = header + '\r\n' +body
    return r.encode(encoding='utf-8')
