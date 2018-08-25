from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def add(num1, num2):
        result = add_server.function(num1, num2)
        return result

    @staticmethod
    def mult(num1, num2):
        result = mul_server.function(num1, num2)
        return result

    @staticmethod
    def div(num1, num2):
        result = div_server.function(num1, num2)
        return result

    @staticmethod
    def root(num1, num2):
        result = root_server.function(num1, num2)
        return result

    @staticmethod
    def pow(num1, num2):
        result = pow_server.function(num1, num2)
        return result

    @staticmethod
    def sub(num1, num2):
        result = sub_server.function(num1, num2)
        return result

    @staticmethod
    def log(num1, num2):
        result = log_server.function(num1, num2)
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
    # Create the rpc to the specifics servers
    add_server = client.ServerProxy('http://localhost:9001')
    sub_server = client.ServerProxy('http://localhost:9002')
    div_server = client.ServerProxy('http://localhost:9003')
    mul_server = client.ServerProxy('http://localhost:9004')
    pow_server = client.ServerProxy('http://localhost:9005')
    root_server = client.ServerProxy('http://localhost:9006')
    log_server = client.ServerProxy('http://localhost:9007')
    main()

