import socket
if __name__ == '__main__':

    #1.创建套接字对象
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #2.设置端口复用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #3.绑定ip与端口
    tcp_server_socket.bind(("192.168.0.10",9999))
    #4.设置监听
    tcp_server_socket.listen(128)
    #5.等待连接
    while True:
        new_socket , ip_port = tcp_server_socket.accept()
        #6.接受消息（返回结果是一个http请求报文）
        client_request_data = new_socket.recv(1024).decode("utf-8")
        if client_request_data:
            # print(client_request_data)
            path_list = client_request_data.split(' ',2)
            path = path_list[1]
            print(path)
            #7.发送消息（返回结果是一个http响应报文）
            #①响应行
            response_line = "HTTP/1.1 200 OK\r\n"
            #②响应头
            response_header = "Server:XiaoJie\r\n"
            #③空行
            #④响应体
            try:
                if path == "/":
                    with open("source/html/index.html", "rb")as f:
                        response_body = f.read()
                else:
                    with open("source" + path,"rb") as f:
                        response_body = f.read()
            except:
                response_data = ("HTTP/1.1 404 Not Found\r\n" + response_header + "\r\n").encode("utf-8") + "找不到捏~\r\n".encode("gbk")
                new_socket.send(response_data)
            else:
                response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
                new_socket.send(response_data)
            finally:
                new_socket.close()