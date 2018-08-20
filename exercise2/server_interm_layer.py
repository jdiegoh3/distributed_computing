import socketserver
import socket
import protocol_utils as protocolUtils


class MessageHandler(socketserver.BaseRequestHandler):

    def handle(self):
        protocol_instance = protocolUtils.MessageHandler(self.request.recv(1024))
        array_operands = protocol_instance.message_loads()
        server_propietys = protocol_instance.switch_operations(array_operands[1])

        if server_propietys:
            socket_instance = socket.socket()
            socket_instance.connect((server_propietys[0], server_propietys[1]))

            message_builder = protocolUtils.MessageBuilder(array_operands[0], array_operands[2], array_operands[1])
            socket_instance.send(message_builder.message_builder().encode())

            result = socket_instance.recv(1024)
            if result:
                self.request.send(result)
            else:
                pass
        else:
            # Error
            pass


def main():
    server = socketserver.TCPServer((protocolUtils.host, protocolUtils.port), MessageHandler)
    print("Server interm layer running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
