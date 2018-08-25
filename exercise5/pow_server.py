import math
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def function(num1, num2):
        print("New operation in queue ", num1, " ", num2)
        try:
            val1 = float(num1)
            val2 = float(num2)
        except ValueError:
            return "The operands requires be numbers"
        return math.pow(float(val1), float(val2))


def main():
    # Create server
    server = SimpleXMLRPCServer(("localhost", 9005),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()

    server.register_instance(RegisteredFunctions())

    # Run the server's main loop
    server.serve_forever()


if __name__ == '__main__':
    main()
