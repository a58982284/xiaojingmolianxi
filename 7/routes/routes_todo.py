from models import Todo
from routes.session import session
from utils import log
from utils import template
#from routes.routes import current_user
'''
def template(name):
    #根据名字读取 templates 文件夹里的一个文件并返回
    path = 'templates/' + name
    with open(path,'r',encoding='utf-8') as f:
        return f.read()
'''


def response_with_headers(headers,code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}:{}\r\n'.format(k,v) for k,v in headers.items()])
    return header

def redirect(location):
    headers = {
        'Content-Type': 'text/html',
    }
    headers['Location'] = location
    # 301 永久重定向 302 普通定向
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')

'''
def login_required(route_function):
    def f(request):
        uname =current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return f
'''

def index(request):
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        session_id = request.cookies.get('user','')
        user_id = session.get(session_id)
        todo_list =Todo.find_all(user_id=user_id)
        log('index debug', user_id, todo_list)
        body = template('todo_index.html',todos=todo_list)
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')

def add(request):
    """
        接受浏览器发过来的添加 todo 请求
        添加数据并发一个 302 定向给浏览器
        浏览器就会去请求 / 从而回到主页
        """
    form = request.form()
    session_id = request.cookies.get('user','')
    user_id = session.get(session_id)
    #创建一个todo
    Todo.new(form,user_id)
    return redirect('/todo/index')

def delete(request):
    """
        通过下面这样的链接来删除一个 todo
        /delete?id=1
        """
    todo_id = int(request.query.get('id'))
    session_id = request.cookies.get('user','')
    user_id = session.get(session_id)
    t = Todo.find(todo_id)
    if t.user_id == user_id:
        Todo.delete(todo_id,user_id=user_id)
    return redirect('/login')


def edit(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    todo_id = int(request.query.get('id'))
    t = Todo.find(todo_id)
    body = template('simple_todo_edit.html', todo=t)
    r = header + '\r\n' +body
    return r.encode(encoding='utf-8')



def update(request):
    form = request.form()
    print('debug update',form)
    todo_id = int(form.get('id'))
    Todo.update(todo_id,form)
    return redirect('/todo')



# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete,
}


