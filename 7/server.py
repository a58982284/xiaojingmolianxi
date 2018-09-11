import socket
import urllib.parse

from utils import log

from routes.routes import route_static
from routes.routes import route_dict

from routes.routes_todo import route_dict as todo_route


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')

                self.cookies[k] = v

    def add_headers(self, header):
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()

    # 从客户端页面得到数据
    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
        根据 path 调用相应的处理函数
        没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    r.update(todo_route)
    response = r.get(path,error)
    return response(request)

def run(host='', port=3000):
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, r))
            if len(r.split()) < 2:
                continue
            path = r.split()[1]

            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            log('debug **', 'sendall')
            # 把响应发送给客户端
            connection.sendall(response)
            log('debug ****', 'close')
            # 处理完请求, 关闭连接
            connection.close()
            log('debug *', 'closed')


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
