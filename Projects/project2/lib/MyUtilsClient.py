import threading
import socket
import MyUtils as MyUtils

class Client(object):
    identifier = ""
    server_host = "LocalHost"
    server_port = 9999
    my_host = ""
    my_port_to_listen = 0
    socket_to_server = None
    listener_socket = None
    my_pages_numbers = []

    def __init__(self, server_host, server_port, identifier=""):
        print("Client it's running ...")
        self.identifier = identifier
        # Server variable instances
        self.server_host = server_host
        self.server_port = server_port
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server.connect((self.server_host, self.server_port))
        # Listener variable
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_host = self.listener_socket.getsockname()[0]
        self.my_port_to_listen = self.listener_socket.getsockname()[1]
        print("my_host: "+self.my_host+", my_port_to_listen: "+str(self.my_port_to_listen))
        # Notify state to server
        self.notify_status_to_server()
        listen_thread = threading.Thread(target=self.start_listening)
        listen_thread.start()

    def start_listening(self):
        self.listener_socket.listen(10)
        while 1:
            sc, addr = self.listener_socket.accept()
            print("connection IP: " + str(addr[0]) + " port: " + str(addr[1]))
            instance = threading.Thread(target=self.read_message, args=(sc, addr))
            instance.start()

    def read_message(self, sc, addr):
        message = sc.recv(1024)
        split_message = MyUtils.MessageHandler(message).message_loads()
        if split_message[0] == 'need_page':
            pass
        elif split_message[0] == 'change_page':
            pass
        else:
            sc.send(MyUtils.MessageBuilder(['No exist function: '+split_message[0]], 'error').get_message())
        sc.close()

    def notify_status_to_server(self):
        if self.identifier == "":
            message = MyUtils.MessageBuilder([self.my_port_to_listen], 'new_client').get_message()
        else:
            message = MyUtils.MessageBuilder([self.my_port_to_listen, self.identifier], 'new_client').get_message()
        print("Sending state to server: " + message.decode())
        self.socket_to_server.send(message)
        result = self.socket_to_server.recv(1024)
        split_message = MyUtils.MessageHandler(result).message_loads()
        print(result.decode())
        if split_message[0] != 'error':
            self.identifier = split_message[0]
            i = 1
            while i < len(split_message):
                self.add_page_number(split_message[i])
                i=i+1
        else:
            print("error: "+split_message[1])
            exit()

    def add_page_number(self, number):
        self.my_pages_numbers.append(number)

    def have_page_number(self, number):
        i = 1
        while i < len(self.my_pages_numbers):
            if self.my_pages_numbers[i] == number:
                return True
            i = i + 1
        return False


def send_page(socket_to_send, page_number):
    file = open("page"+page_number+".txt", "r")
    send_file(socket_to_send, file)

def send_file(socket_to_send, file):
    while (True):
        print "Sending..."
        data = file.read(1024)
        socket_to_send.send(data)
        if len(data) < 1024:
            break
    file.close()
    return True

def receive_page(socket_to_receive, page_number):
    file = open("page"+page_number+".txt", "w+")
    receive_file(socket_to_receive, file)

def receive_file(socket_to_receive, file):
    while (True):
        print "Receiving..."
        info = socket_to_receive.recv(1024)
        file.write(info)
        if len(info) < 1024:
            break
    file.close()
    return True