import socket
import ssl
def parsed_url(url):
    protocol = 'http'
    if url[:7] == 'http://':
        u =url.split('://')[1]
        #print (u)
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
        #print (u)
    else:
        u = url
        #print (u)

    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    #print (host)
    #print (path)
    port_dict ={
        'http':80,
        'https':443,
    }
    #默认端口
    port = port_dict[protocol]
    if ":" in host:
        h = host.split(":")
        #print (h)
        host = h[0]
        port = int(h[1])
        '''
        print (protocol)
        print (host)
        print (path)
        print (port)
        '''

    return protocol,host,port,path


def socket_by_protocol(protocol):

    if protocol =="http":
        s =socket.socket()

    else:
        s = ssl.wrap_socket(socket.socket())

    return s

def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r =s.recv(buffer_size)
        if len(r) == 0:
            break
        else:
            response += r
    return response

def parsed_response(r):

    header,body = r.split('\r\n\r\n',1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k,v = line.split(': ')
        headers[k] = v
    return status_code,headers,body

def get(url):

    protocol,host,port,path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host,port))

    request = 'GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = "utf-8"
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    print ('get response, ', response)
    r = response.decode(encoding)

    status_code,headers,body = parsed_response(r)
    if status_code in [301,302]:
        url = headers['Location']
        return get(url)

    return status_code,headers,body

def main():
    url = 'http://movie.douban.com/top250'
    status_code,headers,body = get(url)
    print('main',status_code)
'''
url = 'http://g.cn'
parsed_url(url)
url = 'https://g.cn:1234/hello'
parsed_url(url)
url = 'g.cn:3000'
parsed_url(url)
url = 'g.cn:3000/search'
parsed_url(url)
'''

def test_get():
    """
    测试是否能正确处理 HTTP 和 HTTPS
    """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    # 这里就直接调用了 get 如果出错就会挂, 测试得比较简单
    for u in urls:
        get(u)


def test_parsed_url():
    """
    parsed_url 函数很容易出错, 所以我们写测试函数来运行看检测是否正确运行
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert 是一个语句, 名字叫 断言
        # 如果断言成功, 条件成立, 则通过测试
        # 否则为测试失败, 中断程序报错
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e

def test():
    """
    用于测试的主函数
    """
    test_parsed_url()
    # test_get()
    # test_parsed_response()


if __name__ == '__main__':
     test()
     main()