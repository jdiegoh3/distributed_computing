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

    server = protocolUtils.MessageHandler(socket_instance.recv(1024)).message_loads()
    server_host, server_port = server[0], int(server[2])

    # Close the actual session to start the new with the server of the operation
    socket_instance.close()

    socket_instance = socket.socket()
    socket_instance.connect((server_host, server_port))
    socket_instance.send(message_builder.message_builder().encode())
    result = socket_instance.recv(1024).decode()
    print("Result: ", result)


if __name__ == "__main__":
    main()
