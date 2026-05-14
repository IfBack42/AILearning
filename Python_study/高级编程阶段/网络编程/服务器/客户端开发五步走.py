import socket
# 1.创建套接字对象（socket.AF_INET => IPv4,socket.SOCK_STREAM => TCP）
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(tcp_client_socket)

# 2 与服务器端连接(元组类型,ip+端口)
tcp_client_socket.connect(("192.168.0.17", 8099))
for i in range(1145):
    # 3.发送消息（必须转为字节流类型）
    tcp_client_socket.send("1145141919810我操你妈傻逼东西\n".encode(encoding="gbk"))

    # # 4.接收消息(括号内为接受数据字节大小)
    # recv_data = tcp_client_socket.recv(1024).decode(encoding="gbk")
    # print(recv_data)
    #
    # # 5.关闭套接字
    # tcp_client_socket.close()
tcp_client_socket.close()