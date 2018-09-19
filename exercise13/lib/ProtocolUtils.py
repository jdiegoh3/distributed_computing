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

    @staticmethod
    def switch_operations(number):
        options = {
            1: "list_groups",
            2: "create_group",
            3: "send_message",
            4: "join_group"
        }
        return options.get(number, None)

    def start_client(self):
        while True:
            print("Supported Operations: \n1. List of groups\n2.Create a group\n3.Send a message to a group")

            operation = input("Insert your operation: ")
            try:
                operation = int(operation)
            except ValueError as e:
                print("Please choose a valid operation")

            operation = self.switch_operations(operation)

            if operation == "list_groups":
                instance_builder = MessageBuilder(operation, None, None)
                self.socket_client.send(instance_builder.get_message_encoded())
                result = MessageHandler(self.socket_client.recv(1024)).message_loads()
                print("--------------------------")
                print("Existing groups: ")
                for group in result:
                    print(group)
                print("--------------------------")

            elif operation == "create_group":
                instance_builder = MessageBuilder(operation, None, None)
                self.socket_client.send(instance_builder.get_message_encoded())
                result = self.socket_client.recv(1024)
                print("--------------------------")
                print(result.decode("utf-8"))
                print("--------------------------")

            elif operation == "join_group":

                instance_builder = MessageBuilder("list_groups", None, None)
                self.socket_client.send(instance_builder.get_message_encoded())

                result = MessageHandler(self.socket_client.recv(1024)).message_loads()
                print("--------------------------")
                print("Existing groups: ")
                for group in result:
                    print(group)
                print("--------------------------")

                group_id = input("Which one group do you want to send the join request?: ")
                instance_builder = MessageBuilder(operation, None, group_id)
                self.socket_client.send(instance_builder.get_message_encoded())
                result = self.socket_client.recv(1024)
                print("--------------------------")
                print(result.decode("utf-8"))
                print("--------------------------")

            elif operation == "send_message":
                message = input("Insert your message: ")
                instance_builder = MessageBuilder("list_groups", None, None)
                self.socket_client.send(instance_builder.get_message_encoded())

                result = MessageHandler(self.socket_client.recv(1024)).message_loads()
                print("--------------------------")
                print("Existing groups: ")
                for group in result:
                    print(group)
                print("--------------------------")

                group_id = input("Which one group do you want to send the message?: ")
                instance_builder = MessageBuilder(operation, message, group_id)
                self.socket_client.send(instance_builder.get_message_encoded())
                result = self.socket_client.recv(1024)
                print("--------------------------")
                print(result.decode("utf-8"))
                print("--------------------------")

    @staticmethod
    def listen_handler(conn, address):
        raw_data = conn.recv(1024)
        print("New message from ", address, " : ", raw_data)

    def start_listen(self):
        group_data = self.socket_client.getsockname()
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind((group_data[0], group_data[1]))
        socket_instance.listen(10)

        while True:
            conn, address = socket_instance.accept()
            temp_thread = threading.Thread(target=self.listen_handler, args=(conn, address,))
            temp_thread.start()


class ProcessGroup(object):
    process_groups = {}
    group_id = 1

    def __init__(self):
        pass

    def add_process(self, sender, group_id=None):
        if not group_id:
            self.process_groups[self.group_id] = [sender]
            self.group_id += 1
        else:
            group = self.process_groups.get(group_id, None)
            if group:
                group.append(sender)
                return True
            else:
                return False

    def get_all_groups(self):
        total_groups = ""
        for key in self.process_groups.keys():
            total_groups += str(key) + "|"
        if len(total_groups) > 0:
            return total_groups.encode()
        else:
            return "No groups".encode()

    def get_group(self, group):
        return self.process_groups.get(group, None)


class MessageHandler(object):
    body = None

    def __init__(self, message):
        self.body = message.decode("utf-8")

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result


class MessageBuilder(object):
    # Operations :  create_group
    #               list_groups
    #               send_message
    #               group_id
    operation = None
    message = None
    group_id = None

    def __init__(self, operation, message, group_id):
        self.operation = operation
        self.message = message
        self.group_id = group_id

    def get_message(self):
        result = str(self.operation) + "|" + str(self.message) + "|" + str(self.group_id)
        return result

    def get_message_encoded(self):
        return self.get_message().encode()







