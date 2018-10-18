
class Elements(object):
    elements = []

    def add_element(self, process_info):
        self.elements.append(process_info)

    def remove_element(self, device_info):
        self.elements.remove(device_info)

    def list_elements(self):
        return self.elements


class FreeDevices(Elements):
    def __init__(self):
        pass


class OccupiedDevices(Elements):
    def __init__(self):
        pass


class UnClassifiedClients(Elements):
    def __init__(self):
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


class MessageBuilder(object):
    message = ""
    operation = None

    def __init__(self, message_elements, op=None):
        self.message += op + "|"
        for string in message_elements:
            self.message += string + "|"

    def get_message(self):
        return self.message.encode()





