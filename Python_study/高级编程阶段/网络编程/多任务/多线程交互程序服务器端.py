import socket
import threading

def send(new_socket,ip_addr):
    try:
        print(f"现在正在与{ip_addr}进行对话~输入114514结束对话~")
        while True:
            send_content = input()
            if send_content == "114514":
                print("结束对话！")
                break
            elif send_content == "":
                print("无效内容！")
                continue
            send_content = send_content.encode("utf-8")
            new_socket.send(send_content)
    except Exception as e:
        print(f"发送出错：{e}")
    finally:
        new_socket.close()

def recv(new_socket,ip_addr):
    try:
        while True:
            recv_content = new_socket.recv(1024)
            if not recv_content:
                print("对方已结束对话~")
                break
            recv_content = recv_content.decode("utf-8")
            print(recv_content)
    except Exception as e:
        print(f"接收消息出错：{e}")

def turn(new_socket,ip_addr):
    send_thread = threading.Thread(target=send,args=(new_socket,ip_addr))
    recv_thread = threading.Thread(target=recv,args=(new_socket,ip_addr))
    send_thread.start()
    recv_thread.start()
    send_thread.join()
    recv_thread.join()

def main():
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server_socket.bind(("",8848))
    tcp_server_socket.listen(128)
    try:
        new_socket,ip_addr = tcp_server_socket.accept()
        turn(new_socket,ip_addr)
    except Exception as e:
        print(f"连接出错:{e}")
    finally:
        tcp_server_socket.close()

if __name__ == '__main__':
    main()