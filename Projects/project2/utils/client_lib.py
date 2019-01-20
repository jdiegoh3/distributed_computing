import threading
import utils.general_utils as library
import socket

PPrint = library.PPrint


class Client(object):
    listen_host = None
    listen_port = None
    server_connection = None
    my_listener = None
    my_listen_address = None
    my_listen_port = None
    pages_space = None

    def __init__(self, server_host, server_port):

        PPrint.show("\n\nClient main menu.", "green")
        PPrint.show("In this client you can do this operations:", "green")
        PPrint.show("1. Request a space of pages.", "green")
        PPrint.show("2. List the space of pages with their owners", "green")
        print("\n\n")

        # Server variable instances
        self.server_host = server_host
        self.server_port = server_port
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.connect((self.server_host, self.server_port))

        self.start_listen()

        self.notify_valid_client()
        listen_thread = threading.Thread(target=self.message_receiver)
        listen_thread.start()

        client_options_thread = threading.Thread(target=self.interative_menu)
        client_options_thread.start()

    def interative_menu(self):
        while True:
            try:
                value = int(input())
            except ValueError as e:
                value = None
            if value == 1:
                try:
                    space_of_pages = int(input("What space of pages do you want? "))
                except ValueError as e:
                    space_of_pages = None
                message = library.MessageBuilder([space_of_pages], "request_pages")
                self.server_connection.send(message.get_message())

                raw_data = self.server_connection.recv(1024)
                handler = library.MessageHandler(raw_data).message_loads()
                if handler[0] == "no_exist":
                    PPrint.show("Resource does not exist", "red")
                elif handler[0] == "call_him":
                    address = handler[1]
                    port = int(handler[2])

                    if self.my_listen_address == address and self.my_listen_port == port:
                        print("Soy yo mismo mk")

                    else:
                        request_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        request_file.connect((address, port))
                        message = library.MessageBuilder((), "give_me")
                        request_file.send(message.get_message())

                        file = open("{}x.txt".format(space_of_pages), "w+")
                        while True:
                            info = request_file.recv(1024)
                            file.write(info.decode("utf-8"))
                            if len(info) < 1024:
                                break
                        file.close()
                        print(request_file.recv(1024))

            elif value == 2:
                message = library.MessageBuilder((), "request_list_pages")
                self.server_connection.send(message.get_message())
                handler = library.MessageHandler(self.server_connection.recv(1024)).message_loads()
                PPrint.show("List of clients:", "green")
                for space in handler[1]:
                    PPrint.show(space, "green")

            else:
                PPrint.show("You must choose a valid option", "red")

    def message_receiver(self):
        self.my_listener.listen(10)
        while 1:
            connection, address = self.my_listener.accept()
            thread = threading.Thread(target=self.receiver_connection, args=(connection, address))
            thread.start()

    def receiver_connection(self, connection, address):
        message = connection.recv(1024)
        split_message = library.MessageHandler(message).message_loads()
        if split_message[0] == 'give_me':
            file = open("{}.txt".format(self.pages_space), "r")
            while True:
                data = file.read(1024).encode()
                connection.send(data)
                if len(data) < 1024:
                    break
            file.close()
        else:
            connection.send(connection.MessageBuilder(['No exist function: ' + split_message[0]]
                                                      , 'error').get_message())
        connection.close()

    def notify_valid_client(self):
        self.server_connection.send(library.MessageBuilder((self.my_listen_address, self.my_listen_port)
                                                           , "valid_client").get_message())
        message = library.MessageHandler(self.server_connection.recv(1024)).message_loads()
        if message[0] == "assigned_space":
            self.pages_space = int(message[1])
            PPrint.show("Assigned space:" + str(self.pages_space), "green")
            f = open("{}{}".format(self.pages_space, ".txt"), "w+")
            f.close()

    def start_listen(self):
        self.my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_listener.bind((socket.gethostbyname(socket.gethostname()), 0))
        socket_vars = self.my_listener.getsockname()
        print(socket_vars)
        self.my_listen_address = socket_vars[0]
        self.my_listen_port = socket_vars[1]


