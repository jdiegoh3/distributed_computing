import socket
import sys
import lib.ProtocolUtils as protocolUtils
import threading as thread


def switch_operations(operation):
    switcher = {
        "+": ["localhost", 9991],
        "-": ["localhost", 9992],
        "*": ["localhost", 9993],
        "/": ["localhost", 9994],
        "^": ["localhost", 9995],
        "log": ["localhost", 9996],
        "root": ["localhost", 9997],
    }
    return switcher.get(operation, None)


def message_handler(conn, addr):
    raw_data = conn.recv(1024)
    data = protocolUtils.MessageHandler(raw_data).message_loads()
    server_interface = switch_operations(data[1])

    server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_instance.connect((server_interface[0], server_interface[1]))

    server_instance.send(raw_data)
    result = server_instance.recv(1024)
    conn.send(result)
    # Close the thread to save hardware.
    # sys.exit()


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, addr = socket_instance.accept()
        temp_thread = thread.Thread(target=message_handler, args=(conn, addr,))
        threads_list.append(temp_thread)
        temp_thread.start()
