import socket

tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#设置端口复用
tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
tcp_server_socket.bind(("",8989))
tcp_server_socket.listen()
while True:
    try:
        #第一个 try 的主要作用是预防在 tcp_server_socket.accept() 方法调用时可能出现的网络异常、
        # 资源限制或其他意外情况。通过捕获这些异常，可以避免程序因意外错误而崩溃，并提供更友好的错误处理逻辑。
        new_socket,ip_addr = tcp_server_socket.accept()
        while True:
            try:
                data = new_socket.recv(1024).decode("gbk")
                if len(data) == 0:
                    print("客户端中断连接")
                    new_socket.close()
                    raise "滚"
                else:
                    print(f"{ip_addr}：{data}")
                    content = input("me:").encode("gbk")
                    new_socket.send(content)
            except ConnectionResetError:
                print("客户端已经断开")
                new_socket.close()
                break

    except:
        print("accept用户或服务器出现异常，退出监听")
        break
tcp_server_socket.close()
