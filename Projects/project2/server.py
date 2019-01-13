import utils.server_lib as library
from utils.general_utils import PPrint, MessageHandler
import socket
import sys
import random
import threading

server_address = "localhost"
server_port = 9999


def client_handler(connection, address):
    while True:
        try:
            raw_data = connection.recv(1024)
            handler = MessageHandler(raw_data).message_loads()

            if handler[0] == "valid_client":
                PPrint.show("{}{}".format("New valid client connected ", address), "green")
            connection.send("Roger".encode())
        except Exception as e:
            if isinstance(e, ConnectionAbortedError):
                PPrint.show("{}{}".format("Connection lost or aborted with the client ", address), "yellow")
            else:
                PPrint.show("{}{}".format("Connection lost or aborted with the client ", address), "red")
            sys.exit(0)


if __name__ == '__main__':
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind((server_address, server_port))
    socket_instance.listen(10)
    PPrint.show("Server running ...", "green")

    while True:
        connection, address = socket_instance.accept()
        PPrint.show("{}{}".format("New connection entry from ", address), "green")

        temp_thread = threading.Thread(target=client_handler, args=(connection, address,))

        temp_thread.start()
