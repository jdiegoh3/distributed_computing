import socketserver
import protocol_utils


class MessageHandler(socketserver.BaseRequestHandler):

    def handle(self):
        protocol_instance = protocol_utils.MessageHandler(self.request.recv(1024))
        result = str(protocol_instance.make_operation()).encode()
        self.request.send(result)

def main():
    server = socketserver.TCPServer((protocol_utils.host, protocol_utils.port), MessageHandler)
    print("Server running ...")
    server.serve_forever()

if __name__ == "__main__":
    main()
        