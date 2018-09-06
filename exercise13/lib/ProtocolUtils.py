import socket
import threading


class ClientBuilder(object):
    client_thread = None
    listen_thread = None
    socket_client = None

    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(("localhost", 9999))

        self.client_thread = threading.Thread(target=self.start_client, args=())
        self.client_thread.start()

        self.listen_thread = threading.Thread(target=self.start_listen, args=())
        self.listen_thread.start()

    def start_client(self):
        while True:
            num1 = input("Ingrese un numero: ")
            num2 = input("Ingrese un numero: ")
            op = input("Ingrese la operacion a realizar: ")

            self.socket_client.send("mensaje".encode())

            result = self.socket_client.recv(1024)
            print("Resultado de la operacion fue ", result.decode("utf-8"))

    @staticmethod
    def listen_handler(conn, address):
        raw_data = conn.recv(1024)
        print(raw_data)

    def start_listen(self):
        group_data = self.socket_client.getsockname()
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind((group_data[0], group_data[1]))
        socket_instance.listen(10)

        while True:
            conn, address = socket_instance.accept()
            temp_thread = threading.Thread(target=self.listen_handler, args=(conn, address,))
            temp_thread.start()

