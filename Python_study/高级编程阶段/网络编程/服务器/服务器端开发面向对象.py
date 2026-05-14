import socket

class WebServer(object):

    def __init__(self):
        self.tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_client_socket.bind(("",8099))
        self.tcp_client_socket.listen(128)
    def start(self):
        while True:
            new_socket,ip_addr = self.tcp_client_socket.accept()
            self.handle_client_request(new_socket,ip_addr)
    def handle_client_request(self,new_socket,ip_addr):
        print(new_socket.recv(1024).decode(encoding="gbk"))
        new_socket.send("wocaonima".encode(encoding="gbk"))
        new_socket.close()
if __name__ == "__main__":
    ws = WebServer()
    ws.start()