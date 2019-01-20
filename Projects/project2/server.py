import utils.server_lib as library
from utils.general_utils import PPrint, MessageHandler, MessageBuilder
import socket
import sys
import random
import threading

server_address = "localhost"
server_port = 9999

connected_clients = library.ConnectedClients()


def client_handler(connection, address):
    while True:
        try:
            raw_data = connection.recv(1024)
            handler = MessageHandler(raw_data).message_loads()

            if handler[0] == "valid_client":
                PPrint.show("{}{}".format("New valid client connected ", address), "green")
                client_info = {
                    "address": handler[1],
                    "port": int(handler[2]),
                    "page_space": library.page_space,
                    "busy": False,
                }
                connected_clients.add_element("{}/{}".format(address[0], address[1]), client_info)
                library.page_space += 1
                connection.send(MessageBuilder((str(client_info.get("page_space", "")))
                                               , "assigned_space").get_message())

            elif handler[0] == "request_pages":

                clients_list = connected_clients.list_elements()
                result = None
                client_instance = None
                for client in clients_list:
                    client_info = clients_list.get(client)
                    if client_info.get("page_space", None) == int(handler[1]):
                        client_instance = client_info
                        result = (client_info.get("address", None), client_info.get("port"))

                if result:
                    if client_instance.get("busy", None):
                        message = MessageBuilder((), "queued")
                    else:
                        client_instance["busy"] = True
                        message = MessageBuilder(result, "call_him")

                else:
                    message = MessageBuilder((), "no_exist")

                connection.send(message.get_message())

            elif handler[0] == "request_list_pages":
                PPrint.show("{}{}".format("New request to list space of pages from: ", address), "green")
                clients_list = connected_clients.list_elements()
                result = []
                for client in clients_list:
                    client_info = clients_list.get(client, None)
                    result.append(client_info.get("page_space", None))
                message = MessageBuilder(result, "list_pages")
                connection.send(message.get_message())

            else:
                connection.send("Roger".encode())
        except Exception as e:
            if isinstance(e, ConnectionAbortedError):
                PPrint.show("{}{}".format("Connection lost or aborted with the client ", address), "yellow")
            else:
                PPrint.show("{}{}".format("Connection lost or aborted with the client ", address), "red")
            raise e
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
