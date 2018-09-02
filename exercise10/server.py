from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socketserver
import threading
import math


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def add(num1, num2):
        result = float(num1) + float(num2)
        return result

    @staticmethod
    def mult(num1, num2):
        result = float(num1) * float(num2)
        return result

    @staticmethod
    def div(num1, num2):
        try:
            result = float(num1) / float(num2)
            return result
        except ZeroDivisionError as e:
            print("You cant divide by 0")
            return None

    @staticmethod
    def sqrt(num1, num2):
        try:
            result = math.pow(float(num1), (1 / float(num2)))
            return result
        except ZeroDivisionError as e:
            print("You cant do root of a number by 0")
            return None

    @staticmethod
    def pow(num1, num2):
        result = math.pow(float(num1), float(num2))
        return result

    @staticmethod
    def sub(num1, num2):
        result = float(num1) - float(num2)
        return result

    @staticmethod
    def log(num1, num2):
        result = math.log(float(num1), float(num2))
        return result


class SimpleThreadedXMLRPCServer(socketserver.ThreadingMixIn, SimpleXMLRPCServer):
    pass


class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.localServer = SimpleThreadedXMLRPCServer(("localhost", 9000))
        self.localServer.register_instance(RegisteredFunctions())

    def run(self):
        self.localServer.serve_forever()


def main():
    # Create server
    server = ServerThread()
    server.start()  # The server is now running
    print("Server running ...")


if __name__ == "__main__":
    main()









