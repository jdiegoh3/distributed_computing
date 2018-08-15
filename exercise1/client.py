import socket
import protocol_utils

socket_instance = socket.socket()
socket_instance.connect((protocol_utils.host, protocol_utils.port))
num1 = input("Ingrese un numero: ")
num2 = input("Ingrese un numero: ")
op = input("Ingrese la operacion a realizar: ")

message_builder = protocol_utils.MessageBuilder(num1, num2, op)
socket_instance.send(message_builder.message_builder().encode())

result = socket_instance.recv(1024)
print("Resultado de la operacion fue ", result.decode("utf-8"))
socket_instance.close()