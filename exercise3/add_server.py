import socketserver
import lib.ProtocolUtils as protocolUtils


class MessageHandler(socketserver.BaseRequestHandler):

    @staticmethod
    def operation(a, b):
        print("New operation in queue ", a, " ", b)
        try:
            return float(a)+float(b)
        except ValueError:
            return "The operands requires be numbers"

    def handle(self):
        protocol_instance = protocolUtils.MessageHandler(self.request.recv(1024))
        array_operands = protocol_instance.message_loads()
        if array_operands[1] == "+":
            result = self.operation(array_operands[0], array_operands[2])
            self.request.send(str(result).encode())
        else:
            self.request.send("Bad Request")


def main():
    # The host and port must be the same declared in server of names
    server = socketserver.TCPServer(("localhost", 9991), MessageHandler)
    print("Server add running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
