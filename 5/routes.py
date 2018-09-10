from utils import log
from models import Message
from models import User

import random

message_list = []

session = {}

def random_str():
    seed = 'abdefyiajw34odjqwepflgkihoifjgoaginiofd23895728495023'
    s = ''
    for i in range(16):
        random_index = random.randint(0,len(seed)-2)
        s += seed[random_index]
    return s

def template(name):

    path = 'templates/' + name
    with open(path, 'r',encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id =request.cookies.get('user','')
    username = session.get(session_id,'[游客]')
    return username


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}',username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers,code=200):
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    headers = {
        'Location':url,
    }
    r = response_with_headers(headers,302) + '\r\n'
    return r.encode('utf-8')

def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method =='POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名和密码错误!'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    log('login 的响应', r)
    return r.encode(encoding='utf-8')

def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u =User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    username = current_user(request)
    if username == '[游客]':
        log("**debug, route msg 未登录")
        return redirect('/')
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post',form)
        message_list.append(msg)

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}






