import lib.MyUtils as MyUtils
import socket
import threading

cpu = "3100"  # 3.1 GHz
ram = "2048"  # 2 GB


def listen_handler(conn, address):
    raw_data = conn.recv(1024)
    print("New message from ", address, " : ", raw_data)
    conn.send("Received".encode())


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
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.connect(("LocalHost", 999))
    print(socket_instance.getsockname())

    listen_thread = threading.Thread(target=my_listener, args=(socket_instance,))
    listen_thread.start()

    socket_instance.send(MyUtils.MessageBuilder([cpu, ram], 'not_working').get_message())
    result = socket_instance.recv(1024)

    while 1:
        mss = input('not_working or occupied : ')
        socket_instance.send(MyUtils.MessageBuilder([cpu, ram], mss).get_message())
        result = socket_instance.recv(1024)
        print(result.decode())
