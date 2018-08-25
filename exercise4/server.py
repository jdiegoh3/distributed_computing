from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
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


def main():
    # Create server
    server = SimpleXMLRPCServer(("localhost", 9000),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()

    server.register_instance(RegisteredFunctions())

    # Run the server's main loop
    server.serve_forever()


if __name__ == "__main__":
    main()









