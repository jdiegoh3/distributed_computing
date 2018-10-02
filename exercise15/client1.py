import socket
import datetime
import threading
import pytz
import time
from lib.MyUtils import TimeBuilder, ClientIncrementBuilder, get_time_server_delay


def get_time_from_server():
    while True:
        socket_instance.send("get_time".encode())
        result = socket_instance.recv(1024)
        datetime_updated = TimeBuilder(
            datetime.datetime.fromtimestamp(float(result.decode()), pytz.timezone('America/Bogota')))

        if datetime_updated.get_time() < datetime_actual.get_time():
            offset = datetime_actual.get_time() - datetime_updated.get_time()
            print(offset * 2)
            client_increment.set_values(True, 2, offset * 2, datetime.timedelta())

        elif datetime_updated.get_time() > datetime_actual.get_time():
            datetime_actual.time = datetime_updated.get_time()

        print("[Server]: Updated time.")
        time.sleep(get_time_server_delay)


def timer():
    while True:
        if client_increment.client_so_fast:
            if client_increment.added_offset < client_increment.client_increment_time:
                client_increment.add_offsed_added(datetime.timedelta(seconds=1))
                datetime_actual.add(datetime.timedelta(seconds=1))
                time.sleep(client_increment.client_increment)
            else:
                client_increment.set_values(False, 1, 0, datetime.timedelta())
        else:
            datetime_actual.add(datetime.timedelta(seconds=1))
            time.sleep(client_increment.client_increment)


if __name__ == "__main__":
    # Client upper for 5 minutes
    print("Client upper for 5 minutes running..")

    datetime_actual = None
    datetime_updated = None

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.connect(("localhost", 9999))
    print(socket_instance.getsockname())

    datetime_actual = TimeBuilder(datetime.datetime.now())

    socket_instance.send(("my_time|" + str(datetime_actual.get_timestamp())).encode())
    result = socket_instance.recv(1024)

    print(result)
    client_increment = ClientIncrementBuilder()

    socket_instance.close()
