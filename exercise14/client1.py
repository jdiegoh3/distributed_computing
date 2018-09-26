import socket
import datetime
import pytz


def get_time_from_server():
    pass


if __name__ == "__main__":

    datetime_actual = None

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.connect(("localhost", 9999))
    print(socket_instance.getsockname())
    val = 1
    while val:
        val = int(input("Get time zone? "))
        socket_instance.send("yes".encode())
        result = socket_instance.recv(1024)

        datetime_actual = datetime.datetime.fromtimestamp(float(result.decode()), pytz.timezone('America/Bogota'))

        print("Resultado de la operacion fue ", datetime_actual)

    socket_instance.close()
