from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import lib.ProtocolUtils as protocolUtils


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RegisteredFunctions:
    @staticmethod
    def add(num1, num2):
        result = add_server.call_function(num1, num2)
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
    server = protocolUtils.ServerThread("localhost", 8060)
    server.register_class_functions(RegisteredFunctions())
    server.start()

    
if __name__ == "__main__":
    # Create the rpc to the specifics servers
    add_server = protocolUtils.ClientThread('http://localhost:9001')
    add_server.start()

    sub_server = protocolUtils.ClientThread('http://localhost:9002')
    sub_server.start()

    div_server = protocolUtils.ClientThread('http://localhost:9003')
    div_server.start()

    mul_server = protocolUtils.ClientThread('http://localhost:9004')
    mul_server.start()
    
    pow_server = protocolUtils.ClientThread('http://localhost:9005')
    pow_server.start()

    root_server = protocolUtils.ClientThread('http://localhost:9006')
    root_server.start()

    log_server = protocolUtils.ClientThread('http://localhost:9007')
    log_server.start()
    
    main()

