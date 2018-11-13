import threading
import socket
import time


class Elements(object):
    def __init__(self, elements):
        self.elements = elements

    def add_element(self, id, process_info):
        self.elements[id] = process_info

    def remove_element(self, id):
        try:
            del self.elements[id]
        except KeyError as error:
            print("Doesn't exist")

    def list_elements(self):
        return self.elements


class FreeDevices(Elements):
    elements = {}

    def __init__(self):
        super().__init__(self.elements)
        pass


class OccupiedDevices(Elements):
    elements = {}

    def __init__(self):
        super().__init__(self.elements)
        pass


class UnClassifiedClients(Elements):
    elements = {}

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
    server_host = "LocalHost"
    server_port = 9999
    my_host = ""
    my_port = 0
    occupied = False
    resources = None
    socket_to_server = None
    listener_socket = None

    def __init__(self, server_host, server_port, occupied, cpu, memory):
        print("Client running ...")
        # Server variable instances
        self.server_host = server_host
        self.server_port = server_port
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_to_server.connect((self.server_host, self.server_port))
        # Client variable instances
        self.my_host = self.socket_to_server.getsockname()[0]
        self.my_port = self.socket_to_server.getsockname()[1]
        print("my_host: "+self.my_host+", my_port: "+str(self.my_port))
        self.resources = Resources(cpu, memory)
        self.occupied = occupied
        # Notify state to server
        self.notify_status_to_server()
        listen_thread = threading.Thread(target=self.start_listening)
        listen_thread.start()

    def start_listening(self):
        if self.my_port == 0:
            print("can not start_listening because the constructor is running, trying again in 1s...")
            time.sleep(1)
            self.start_listening()
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.bind((self.my_host, self.my_port))
        self.listener_socket.listen(10)
        while 1:
            sc, addr = self.listener_socket.accept()
            print("connection IP: " + str(addr[0]) + " port: " + str(addr[1]))
            instance = threading.Thread(target=self.read_message, args=(sc, addr))
            instance.start()

    def read_message(self, sc, addr):
        message = sc.recv(1024)
        split_message = MessageHandler(message).message_loads()
        if split_message[0] == 'get_resources':
            if not self.occupied:
                if split_message[1] <= self.resources.free_cpu and split_message[2] <= self.resources.free_memory:
                    # the message have cpu [1], memory [2], time_factor [3]
                    id = self.resources.add_task(split_message[1], split_message[2], addr, split_message[3])
                    if id != 0:
                        sc.send(MessageBuilder([id], 'ok').get_message())
                        instance = threading.Thread(target=self.resolveTask, args=(id))
                        instance.start()
                    else:
                        sc.send(MessageBuilder(['No have resources'], 'error').get_message())
            else:
                sc.send(MessageBuilder(['No have resources'], 'error').get_message())
        else:
            sc.send(MessageBuilder(['No exist function: '+split_message[0]], 'error').get_message())
        sc.close()

    def resolveTask(self, id):
        task = self.resources.get_task(id)
        time_of_task = (task[1].memory / task[1].cpu) * task[1].time_factor
        print("running task id: "+str(id)+", time: "+str(time_of_task))
        time.sleep(time_of_task)
        message = MessageBuilder([id], 'task_resolved').get_message()
        send_message(task[2][0], task[2][1], message)
        self.resources.delete_task(id)
        print("Task is resolved id: " + str(id) + ", time: " + str(time_of_task))
        self.notify_status_to_server()

    def free_client(self):
        self.occupied = False
        self.notify_status_to_server()

    def occupied_client(self):
        self.occupied = True
        self.notify_status_to_server()
        for task in self.resources.tasks:
            self.delegate_task(task[1])
            self.resources.delete_task(task[0])

    def delegate_task(self, cpu, memory, time_factor=1):
        print("delegating task cpu: " + str(cpu) + ", memory: " + str(memory) + ", time_factor: " + str(time_factor))
        message = MessageBuilder([cpu, memory, time_factor], 'get_resources').get_message()
        self.socket_to_server.send(message)
        response = self.socket_to_server.recv(1024)
        split_message = MessageHandler(response).message_loads()
        if split_message[0] == "400":
            print("can not delegate task, trying again in 10s...")
            time.sleep(10)
            self.delegate_task(cpu,memory,time_factor)
        elif split_message[0] == "not_working":
            response = send_message(split_message[1], int(split_message[2]), message)
            split_message1 = MessageHandler(response).message_loads()
            if split_message1[0] == "ok":
                print("delegated task to: "+split_message[1]+", "+split_message[2]+", task_id: "+split_message1[1])
            else:
                print("response: "+split_message1[0]+", "+split_message1[1])
                print("can not delegate task, trying again in 10s...")
                time.sleep(10)
                self.delegate_task(cpu, memory, time_factor)
        else:
            print("error-ER0001 - Unknown error")

    def notify_status_to_server(self):
        if self.occupied:
            message = MessageBuilder([
                self.resources.cpu,
                self.resources.memory
            ], 'occupied').get_message()
            print("Sending state to server: " + message.decode())
            self.socket_to_server.send(message)
            result = self.socket_to_server.recv(1024)
            print(result.decode())
        else:
            message = MessageBuilder([
                self.resources.free_cpu,
                self.resources.free_memory
            ], 'not_working').get_message()
            print("Sending state to server: " + message.decode())
            self.socket_to_server.send(message)
            result = self.socket_to_server.recv(1024)
            print(result.decode())


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


    def add_task(self, cpu, memory, address, time_factor=0):
        if cpu <= self.free_cpu and memory <= self.free_memory:
            id = self.get_id()
            # Task -> id [0], ObjectTask [1], Address [2]
            self.tasks.append([id, Task(cpu, memory, time_factor), address])
            self.update_resources()
            return id
        else:
            return 0

    def get_task(self, id):
        count = 0
        while count < len(self.tasks):
            if self.tasks[count][0] == id:
                return self.tasks[count]
            else:
                count = count+1
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
    time_factor = 1

    def __init__(self, cpu, memory, time_factor):
        self.cpu = cpu
        self.memory = memory
        self.time_factor = time_factor