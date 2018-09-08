import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict

class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k,v = arg.split('=')
            f[k] = v
        return f

request = Request()

def error(request, code=404):

    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path,{}
    else:
        path,query_string = path.split('?',1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k,v =arg.split('=')
            query[k] = v
        return path,query


def response_for_path(path):
    path,query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query',path,query)

    r = {
        '/static':route_static,
    }
    r.update(route_dict)
    response = r.get(path,error)
    return response(request)

def run(host='',port=3000):
    log('start at','{}:{}'.format(host,port))
    with socket.socket() as s:
        s.bind((host,port))
        while True:
            s.listen(5)
            connection,address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            log('原始请求',r)
            if len(r.split()) <2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            # 把 body 放入 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            # 处理完请求, 关闭连接
            connection.close()

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


