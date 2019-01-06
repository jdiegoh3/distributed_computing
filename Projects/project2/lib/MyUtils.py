import socket

class Elements(object):
    def __init__(self, elements):
        self.elements = elements

    def add_element(self, id, process_info):
        self.elements[id] = process_info

    def remove_element(self, id):
        try:
            del self.elements[id]
        except KeyError as error:
            pass

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
