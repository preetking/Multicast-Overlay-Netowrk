import socket

class MulticastSocket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.socket.bind((self.ip, self.port))

    def connect(self, ip, port):
        self.socket.connect((ip, port))

    def send(self, data):
        self.socket.sendall(data.encode())

    def receive(self, buffer_size=1024):
        return self.socket.recv(buffer_size).decode()

    def close(self):
        self.socket.close()
