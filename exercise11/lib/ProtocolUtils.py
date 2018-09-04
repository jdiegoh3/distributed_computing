from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import socketserver

class MessageHandler(object):
    body = None

    def __init__(self, message):
        self.body = message.decode("utf-8")

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result


class MessageBuilder(object):
    operand1 = None
    operand2 = None
    operation = None

    def __init__(self, num1=None, num2=None, op=None):
        self.operand1 = float(num1)
        self.operand2 = float(num2)
        self.operation = op

    def get_operands(self):
        try:
            self.operand1 = float(self.operand1)
            self.operand2 = float(self.operand2)
        except ValueError:
            print("Not be numbers")
        return self.operand1, self.operand2

    def message_builder(self):
        if self.operand1 and self.operand2 and self.operation:
            result = str(self.operand1) + "|" + str(self.operation) + "|" + str(self.operand2)
            return result


class SimpleThreadedXMLRPCServer(socketserver.ThreadingMixIn, SimpleXMLRPCServer):
        pass


class ServerThread(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.local_server = SimpleThreadedXMLRPCServer((address, port))

    def register_class_functions(self, class_instance):
        self.local_server.register_instance(class_instance)

    def register_function(self, function):
        self.local_server.register_function(function)

    def run(self):
        self.local_server.serve_forever()


class ClientThread(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.local_client = client.ServerProxy(address)

    def get_client(self):
        return self.local_client

    def call_function(self, arg1, arg2):
        return self.local_client.function(arg1, arg2)

    def run(self):
        pass