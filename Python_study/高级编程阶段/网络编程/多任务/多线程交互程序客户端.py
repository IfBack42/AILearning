import socket
import threading

def send(new_socket):
    try:
        print("输入114514退出对话~")
        while True:
            content = input()
            if content == "114514":
                print("退出程序")
                break
            elif content == "":
                print("无效内容")
                continue
            content = content.encode("utf-8")
            new_socket.send(content)
    except Exception as e:
        print(f"发送失败：{e}")
    finally:
        new_socket.close()

def recv(new_socket):
    try:
        while True:
            content = new_socket.recv(1024).decode("utf-8")
            if not content:
                print("对方已结束对话")
                break
            print(f"对方说:{content}")
    except Exception as e:
        print(f"接收消息出错：{e}")

def main():
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # tcp_client_socket.connect((ip_addr,port))
        tcp_client_socket.connect(("192.168.0.11", 8848))
        print("连上哩！发送“114514”退出对话或者暴力关掉！")
    except Exception as e:
        print(f"妹连上，重来:{e}")
        exit(114)

    send_process = threading.Thread(target=send, args=(tcp_client_socket,))
    recv_process = threading.Thread(target=recv, args=(tcp_client_socket,))
    send_process.start()
    recv_process.start()
    #join : 让主线程等待子线程结束再结束
    send_process.join()
    recv_process.join()
    tcp_client_socket.close()
if __name__ == '__main__':
    main()
