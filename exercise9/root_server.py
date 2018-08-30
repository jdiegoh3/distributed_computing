import socket
import sys
import math
import lib.ProtocolUtils as protocolUtils
import threading as thread


def message_handler(conn, addr):
    data = protocolUtils.MessageHandler(conn.recv(1024)).message_loads()

    print("New operation in queue ", data[0], " ", data[2])
    try:
        val1 = float(data[0])
        val2 = float(data[2])
    except ValueError:
        result = "The operands requires be numbers"
        conn.send(result.encode())

    try:
        result = str(math.pow(val1, (1 / val2)))
        conn.send(result.encode())
    except ZeroDivisionError as e:
        result = "You cant do root by 0"
        conn.send(result.encode())

    # Close the thread to save hardware.
    # sys.exit()


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9997))
    socket_instance.listen(10)

    threads_list = []
    print("Add Server running ...")
    while True:
        conn, addr = socket_instance.accept()
        temp_thread = thread.Thread(target=message_handler, args=(conn, addr,))
        threads_list.append(temp_thread)
        temp_thread.start()
