import threading
import socket


class Elements(object):
    def __init__(self, elements):
        self.elements = elements

    def add_element(self, process_info):
        self.elements.append(process_info)

    def remove_element(self, device_info):
        try:
            self.elements.remove(device_info)
        except ValueError as error:
            print("Doesn't exist")

    def list_elements(self):
        return self.elements


class FreeDevices(Elements):
    elements = []

    def __init__(self):
        super().__init__(self.elements)
        pass


class OccupiedDevices(Elements):
    elements = []

    def __init__(self):
        super().__init__(self.elements)
        pass


class UnClassifiedClients(Elements):
    elements = []

    def __init__(self):
        super().__init__(self.elements)
        pass


class MessageHandler(object):
    body = None

    def __init__(self, message):
        if not isinstance(message, str):
            message = message.decode("utf-8")
        self.body = message

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result


def send_message(host, port, message):
    temporal_socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temporal_socket_instance.connect((host, port))
    temporal_socket_instance.send(message)
    result = temporal_socket_instance.recv(1024)
    return result

class MessageBuilder(object):
    message = ""
    operation = None

    def __init__(self, message_elements, op=None):
        self.message += op + "|"
        for string in message_elements:
            self.message += str(string) + "|"

    def get_message(self):
        return self.message.encode()


class Client(object):
    server_host = ""
    server_port = 0
    occupied = False
    resources = None
    socket_to_server = None

    def __init__(self, server_host, server_port, occupied, cpu, memory):
        self.server_host = server_host
        self.server_port = server_port
        self.occupied = occupied
        self.resources = Resources(cpu, memory)
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket_to_server.bind(('localhost', 99))
        self.socket_to_server.listen(10)
        while 1:
            sc, addr = self.socket_to_server.accept()
            print("connection IP: " + str(addr[0]) + " port: " + str(addr[1]))
            instance = threading.Thread(target=self.read_message, args=(sc, addr))
            instance.start()

    def read_message(self, sc, addr):
        message = sc.recv(1024)
        split_message = MessageHandler(message).message_loads()
        if split_message[0] == 'get_resources':
            if not self.occupied:
                if split_message[1] <= self.resources.free_cpu and split_message[2] <= self.resources.free_memory:
                    id = self.resources.add_task(split_message[1], split_message[2])
                    sc.send(MessageBuilder([id], 'ok').get_message())
            else:
                sc.send(MessageBuilder(['No have resources'], 'error').get_message())
        else:
            sc.send(MessageBuilder(['No exist function: '+split_message[0]], 'error').get_message())
        sc.close()

    def free_client(self):
        self.occupied = False
        self.notify_status_to_server()

    def occupied_client(self):
        self.occupied = True
        self.notify_status_to_server()
        for task in self.resources.tasks:
            self.delegate_task(task[1])
            self.resources.delete_task(task[0])

    def delegate_task(self, task):
        pass

    def notify_status_to_server(self):
        if self.occupied:
            self.socket_to_server.send(MessageBuilder([
                self.resources.cpu,
                self.resources.memory
            ], 'occupied').get_message())
            result = self.socket_to_server.recv(1024)
            print(result)
        else:
            self.socket_to_server.send(MessageBuilder([
                self.resources.cpu,
                self.resources.memory,
                self.resources.free_cpu,
                self.resources.free_memory
            ], 'free').get_message())
            result = self.socket_to_server.recv(1024)
            print(result)


class Resources:
    cpu = 0
    used_cpu = 0
    free_cpu = 0
    memory = 0
    used_memory = 0
    free_memory = 0

    tasks = []

    def __init__(self, cpu, memory):
        self.cpu = cpu
        self.memory = memory
        self.update_resources()

    def update_resources(self):
        used_cpu = 0
        used_memory = 0
        for task in self.tasks:
            used_cpu = used_cpu + task[1].cpu
            used_memory = used_memory + task[1].memory
        self.used_cpu = used_cpu
        self.used_memory = used_memory
        self.free_cpu = self.cpu - self.used_cpu
        self.free_memory = self.memory - self.used_memory


    def add_task(self, cpu, memory):
        if cpu <= self.free_cpu and memory <= self.free_memory:
            id = self.get_id()
            self.tasks.append([id, Task(cpu, memory)])
            self.update_resources()
            return id
        else:
            return 0

    def delete_task(self, id):
        count = 0
        while count < len(self.tasks):
            if self.tasks[count][0] == id:
                self.tasks.pop(count)
                break
            else:
                count = count+1
        self.update_resources()

    def get_id(self, id=1):
        for task in self.tasks:
            if task[0] == id:
                id = id+1
                return self.get_id(id)
        return id


class Task:
    cpu = 0
    memory = 0

    def __init__(self, cpu, memory):
        self.cpu = cpu
        self.memory = memory