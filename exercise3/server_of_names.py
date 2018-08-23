import socketserver
import lib.ProtocolUtils as protocolUtils

server_add_host = "localhost"
server_add_port = 9991

server_sub_host = "localhost"
server_sub_port = 9992

server_root_host = "localhost"
server_root_port = 9993

server_mul_host = "localhost"
server_mul_port = 9994

server_div_host = "localhost"
server_div_port = 9995

server_pow_host = "localhost"
server_pow_port = 9996

server_log_host = "localhost"
server_log_port = 9997


class MessageHandler(socketserver.BaseRequestHandler):

    @staticmethod
    def get_server(operation):
        switcher = {
            "+": [server_add_host, server_add_port],
            "-": [server_sub_host, server_sub_port],
            "*": [server_mul_host, server_mul_port],
            "/": [server_div_host, server_div_port],
            "^": [server_pow_host, server_pow_port],
            "root": [server_root_host, server_root_port],
            "log": [server_log_host, server_log_port]
        }
        return switcher.get(operation, None)

    def handle(self):
        server_prop = self.request.recv(1024).decode("utf-8")
        server_prop = self.get_server(server_prop)

        if server_prop:
            builder_instance = protocolUtils.MessageBuilder(server_prop[0], server_prop[1], True)
            self.request.send(builder_instance.message_builder().encode())
        else:
            error = "Error: Operation doesnt exists"
            self.request.send(error.encode())


def main():
    server = socketserver.TCPServer((protocolUtils.host, protocolUtils.port), MessageHandler)
    print("Server of names running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
