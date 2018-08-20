import socketserver
import math
import protocol_utils as protocolUtils


class MessageHandler(socketserver.BaseRequestHandler):

    @staticmethod
    def operation(a, b):
        print("New operation in queue ", a, " ", b)
        try:
            val1 = float(a)
            val2 = float(b)
        except ValueError:
            return "The operands requires be numbers"
        return val1*val2

    def handle(self):
        protocol_instance = protocolUtils.MessageHandler(self.request.recv(1024))
        array_operands = protocol_instance.message_loads()
        if array_operands[1] == "*":
            result = self.operation(array_operands[0], array_operands[2])
            self.request.send(str(result).encode())
        else:
            self.request.send("Bad Request")


def main():
    server = socketserver.TCPServer((protocolUtils.server_mul_host, protocolUtils.server_mul_port), MessageHandler)
    print("Server multi running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
