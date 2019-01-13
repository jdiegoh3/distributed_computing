import threading
import utils.general_utils as library
import socket


class Client(object):
    listen_host = None
    listen_port = None
    server_connection = None
    my_listener = None
    my_listen_address = None
    my_listen_port = None

    def __init__(self, server_host, server_port):

        # Server variable instances
        self.server_host = server_host
        self.server_port = server_port
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((self.server_host, self.server_port))

        self.start_listen()

        self.notify_valid_client()
        listen_thread = threading.Thread(target=self.message_receiver)
        listen_thread.start()

    def message_receiver(self):
        self.my_listener.listen(10)
        while 1:
            connection, address = self.my_listener.accept()
            thread = threading.Thread(target=self.receiver_connection, args=(connection, address))
            thread.start()

    @staticmethod
    def receiver_connection(connection, address):
        message = connection.recv(1024)
        split_message = connection.MessageHandler(message).message_loads()
        if split_message[0] == 'need_page':
            pass
        elif split_message[0] == 'change_page':
            pass
        else:
            connection.send(connection.MessageBuilder(['No exist function: ' + split_message[0]]
                                                      , 'error').get_message())
        connection.close()

    def notify_valid_client(self):
        self.server_connection.send(library.MessageBuilder((self.my_listen_address, self.my_listen_port)
                                                           , "valid_client").get_message())

    def start_listen(self):
        self.my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_listener.bind(('', 0))
        socket_vars = self.my_listener.getsockname()
        self.my_listen_address = socket_vars[0]
        self.my_listen_port = socket_vars[1]


