import socket
#1.创建tcp服务器端套接字对象
tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#2.绑定ip和端口号（本机或当前服务器）bind也是元组类型
tcp_server_socket.bind(("",8099))
print(tcp_server_socket)

#3.设置监听（让代码监听端口传输过来的数据）
tcp_server_socket.listen(128)

#4.等待客户端连接（重难点） 接受过后有两个信息，一个是新产生的套接字，一个是客户端ip和端口
#客户端和服务器端连接成功后信息发送与接受都要考新产生的套接字，其内部保存了客户端和服务器端的相关信息
new_socket,ip_addr = tcp_server_socket.accept()
print(new_socket,ip_addr)

#5.接受客户端发来的消息
data = new_socket.recv(1024).decode(encoding="gbk")
print(f"{ip_addr}客户端发送数据：{data}")

#6.处理客户端请求并返回数据给客户端
new_socket.send("wocaonima".encode(encoding="gbk"))
#7.关闭服务器端套接字对象及新产生的套接字对象
new_socket.close()
tcp_server_socket.close()