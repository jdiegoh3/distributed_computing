import socketserver
import math
import lib.ProtocolUtils as protocolUtils


class MessageHandler(socketserver.BaseRequestHandler):

    @staticmethod
    def operation(a, b):
        print("New operation in queue ", a, " ", b)
        try:
            val1 = float(a)
            val2 = float(b)
        except ValueError:
            return "The operands requires be numbers"

        try:
            result = math.pow(val1, (1/val2))
            return result
        except ZeroDivisionError as e:
            print("You cant do root of a number by 0")
            return "You cant do root of 0"

    def handle(self):
        protocol_instance = protocolUtils.MessageHandler(self.request.recv(1024))
        array_operands = protocol_instance.message_loads()
        if array_operands[1] == "root":
            result = self.operation(array_operands[0], array_operands[2])
            self.request.send(str(result).encode())
        else:
            self.request.send("Bad Request")


def main():
    server = socketserver.TCPServer(("localhost", 9993), MessageHandler)
    print("Server root running ...")
    server.serve_forever()


if __name__ == "__main__":
    main()
