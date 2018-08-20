import socketserver
import protocol_utils as protocolUtils


class MessageHandler(socketserver.BaseRequestHandler):

    def operation(self, a, b):
        print("New operation in queue ", a, " ", b)
        return float(a)+float(b)

    def handle(self):
        protocol_instance = protocolUtils.MessageHandler(self.request.recv(1024))
        array_operands = protocol_instance.message_loads()
        if array_operands[1] == "+":
            result = self.operation(array_operands[0], array_operands[2])
            self.request.send(str(result).encode())
        else:
            self.request.send("Bad Request")


def main():
    server = socketserver.TCPServer((protocolUtils.server_add_host, protocolUtils.server_add_port), MessageHandler)
    print("Server sub running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
