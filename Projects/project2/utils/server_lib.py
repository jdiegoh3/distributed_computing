import threading
import socket
import time

page_space = 0


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


class ConnectedClients(Elements):
    elements = {}

    def __init__(self):
        super().__init__(self.elements)