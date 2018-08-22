import socket
import lib.ProtocolUtils as protocolUtils


def main():
    socket_instance = socket.socket()
    socket_instance.connect((protocolUtils.host, protocolUtils.port))

    num1 = input("Ingrese un numero: ")
    num2 = input("Ingrese un numero: ")
    op = input("Ingrese la operacion a realizar: ")

    message_builder = protocolUtils.MessageBuilder(num1, num2, op)

    socket_instance.send(message_builder.operation.encode())

    server = socket_instance.recv(1024)
    print("Server direct ", server.decode("utf-8"))

    socket_instance.close()


if __name__ == "__main__":
    main()
