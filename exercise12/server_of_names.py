from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import lib.ProtocolUtils as protocolUtils


class RegisteredFunctions:
    @staticmethod
    def get_server(operation):
        switcher = {
            "+": "http://localhost:9001",
            "-": "http://localhost:9002",
            "/": "http://localhost:9003",
            "*": "http://localhost:9004",
            "^": "http://localhost:9005",
            "root": "http://localhost:9006",
            "log": "http://localhost:9007"
        }
        return switcher.get(operation, None)

def main():
    # Create server
    server = protocolUtils.ServerThread("localhost", 8060)
    server.register_class_functions(RegisteredFunctions())
    server.start()

    
if __name__ == "__main__":
    main()

