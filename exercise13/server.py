import socket
import sys
import threading as thread


def message_handler(conn, address):
    while True:
        raw_data = conn.recv(1024)
        conn.send("yesss".encode())
    # Close the thread to save hardware.
    # sys.exit()


def thread_call_client(address):
    while True:
        socketInsa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketInsa.connect((address[0], address[1]))
        socketInsa.send("Yupale".encode())


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, address = socket_instance.accept()
        print("Yes of course bitch:", address)
        temp_thread = thread.Thread(target=message_handler, args=(conn, address,))
        threads_list.append(temp_thread)
        temp_thread.start()

        temp_thread = thread.Thread(target=thread_call_client, args=(address,))
        temp_thread.start()
