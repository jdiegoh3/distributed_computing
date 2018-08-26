from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def switch_operations(operation):
        switcher = {
            "+": 'http://localhost:9001',
            "*": 'http://localhost:9004',
            "-": 'http://localhost:9002',
            "/": 'http://localhost:9003',
            "^": 'http://localhost:9005',
            "log": 'http://localhost:9007',
            "root": 'http://localhost:9006'
        }
        return switcher.get(operation, None)

    def get_operation_server(self, operation):
        return self.switch_operations(operation)


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

