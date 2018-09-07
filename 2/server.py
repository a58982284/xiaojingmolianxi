import socket

def log(*args, **kwargs):
    print('log',*args,**kwargs)

def route_index():
    #主页的处理函数,返回主页的响应
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello liyi</h1><img src="/doge.gif">'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def page(name):
    with open(name,encoding='utf-8') as f:
        return f.read()


def route_msg():
    #msg 页面处理函数
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_image():
    #图片的处理函数,读取图片并生成响应返回
    with open('doge.gif','rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img

def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')

def response_for_path(path):
    r = {
        '/':route_index,
        '/doge.gif':route_image,
        '/msg':route_msg,
    }
    response = r.get(path,error)
    return response()

def run(host='',port=3000):
    with socket.socket() as s:
        s.bind((host,port))
        while True:
            s.listen(5)
            connection,address = s.accept()
            request = connection.recv(1024)
            log('raw, ',request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address,request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)

            except Exception as e:
                log('error',e)
            connection.close()

def main():
    config = dict(
        host='',
        port=3000,
    )
    run(**config)

if __name__ == '__main__':
    main()


