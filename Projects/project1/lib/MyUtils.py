
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


class MessageBuilder(object):
    message = ""
    operation = None

    def __init__(self, message_elements, op=None):
        self.message += op + "|"
        for string in message_elements:
            self.message += str(string) + "|"

    def get_message(self):
        return self.message.encode()





