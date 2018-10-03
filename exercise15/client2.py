import socket
import datetime
import threading
import pytz
import time
from lib.MyUtils import TimeBuilder, ClientIncrementBuilder, get_time_server_delay


def set_time_from_server(raw_timestamp):
    datetime_updated = TimeBuilder(
        datetime.datetime.fromtimestamp(raw_timestamp))

    if datetime_updated.get_time() < datetime_actual.get_time():
        offset = datetime_actual.get_time() - datetime_updated.get_time()
        print(offset * 2)
        client_increment.set_values(True, 2, offset * 2, datetime.timedelta())

    elif datetime_updated.get_time() > datetime_actual.get_time():
        datetime_actual.time = datetime_updated.get_time()

    print("[Server]: Updated time.")


def timer():
    while True:
        if client_increment.client_so_fast:
            print("Client so fast")
            if client_increment.added_offset < client_increment.client_increment_time:
                client_increment.add_offsed_added(datetime.timedelta(seconds=1))
                datetime_actual.add(datetime.timedelta(seconds=1))
                time.sleep(client_increment.client_increment)
            else:
                client_increment.set_values(False, 1, 0, datetime.timedelta())
        else:
            datetime_actual.add(datetime.timedelta(seconds=1))
            time.sleep(client_increment.client_increment)


def listen_handler(conn, address):
    raw_data = conn.recv(1024)
    print("New message from ", address, " : ", raw_data)
    set_time_from_server(float(raw_data.decode()))


def my_listener(socket_instance):
    print("Started client listener")
    group_data = socket_instance.getsockname()
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_socket.bind((group_data[0], group_data[1]))
    listener_socket.listen(10)

    while True:
        conn, address = listener_socket.accept()
        temp_thread = threading.Thread(target=listen_handler, args=(conn, address,))
        temp_thread.start()


if __name__ == "__main__":
    # Client upper for 5 minutes
    print("Client upper for 5 minutes running..")

    datetime_actual = None
    datetime_updated = None

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.connect(("localhost", 9999))
    print(socket_instance.getsockname())

    listen_thread = threading.Thread(target=my_listener, args=(socket_instance,))
    listen_thread.start()

    datetime_actual = TimeBuilder(datetime.datetime.now() - datetime.timedelta(minutes=5))

    socket_instance.send(("my_time|" + str(datetime_actual.get_timestamp())).encode())
    result = socket_instance.recv(1024)

    print(result)
    client_increment = ClientIncrementBuilder()

    socket_instance.close()
