from utils import log
from models import Message
from models import User

import random


message_list = []

session = {
    'session id':{
        'username': 'gua',
        '过期时间': '9.30 21:00:00'
    }
}

def random_str():
    """
        生成一个随机的字符串
        """
    seed = 'zaqolmqwert123985yuiopasdfghkjlzxcvbnm8541239754dadsfjrfvtgbnhyujm'
    s = ''
    for i in range(16):
        random_index = random.randint(0,len(seed)-2)
        s += seed[random_index]
    return s


def template(name):
    """
       根据名字读取 templates 文件夹里的一个文件并返回
       """
    path = 'templates/' + name
    with open(path,'r',encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user','')
    username = session.get(session_id,'[游客]')
    return username


def route_index(request):
    #主页的处理函数, 返回主页的响应
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}',username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def response_with_headers(headers):
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k,v)
                       for k ,v in headers.items()])
    return header

def route_login(request):
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = u.username
            headers['set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}',result)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
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
    """
        消息页面的路由函数
        """
    username = current_user(request)
    if username == '[游客]':
        log("**debug, route msg 未登录")
        pass
    log('本次请求的method',request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post',form)
        message_list.append(msg)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{message}}',msgs)
    r =header +'\r\n' + body
    return r.encode(encoding='utf-8')

def route_static(request):
    filename = request.query.get('file','doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img
# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/':route_index,
    '/login':route_login,
    '/register':route_register,
    '/messages':route_message,
}

