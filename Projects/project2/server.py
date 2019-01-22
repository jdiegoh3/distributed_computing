import utils.server_lib as library
from utils.general_utils import PPrint, MessageHandler, MessageBuilder
import socket
import sys
import random
import threading

server_address = "192.168.0.5"
server_port = 9999

connected_clients = library.ConnectedClients()
queued_clients = library.QueuedClients()


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

                        listener_info = clients_list.get("{}/{}".format(address[0], address[1]))
                        listener_bone = (listener_info.get("address", None), listener_info.get("port", None))

                        list_wait = queued_clients.list_elements()
                        element = list_wait.get(int(handler[1]), None)
                        if element:
                            element.append(listener_bone)
                        else:
                            queued_clients.add_element(int(handler[1]), [listener_bone])


                        print(list_wait)

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

            elif handler[0] == "free_resource":
                PPrint.show("{}{}".format("New request to free a resource from: ", address), "green")
                clients_list = connected_clients.list_elements()
                client_owner = None
                for client in clients_list:
                    client_info = clients_list.get(client, None)
                    if client_info.get("page_space", None) == int(handler[1]):
                        client_owner = client_info
                        client_info["busy"] = False
                message = MessageBuilder((), "request_ok")

                list_wait = queued_clients.list_elements()
                element = list_wait.get(int(handler[1]), None)
                client_to_call = None
                if element:
                    client_to_call = element.pop()

                if client_to_call and client_owner:
                    request_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    request_file.connect(client_to_call)
                    message_use_res = MessageBuilder((client_owner.get("address", None), client_owner.get("port", None), client_owner.get("page_space", None)), "call_resource")
                    request_file.send(message_use_res.get_message())

                connection.send(message.get_message())
            else:
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
    PPrint.show("{}{}".format("Server running on ", socket.gethostbyname(socket.gethostname())), "green")

    while True:
        connection, address = socket_instance.accept()
        PPrint.show("{}{}".format("New connection entry from ", address), "green")

        temp_thread = threading.Thread(target=client_handler, args=(connection, address,))

        temp_thread.start()
