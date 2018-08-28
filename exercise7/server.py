import socket
import sys
import protocol_utils
import threading as thread


def message_handler(conn, addr):
    data = protocol_utils.MessageHandler(conn.recv(1024))
    result = str(data.make_operation()).encode()
    conn.send(result)
    # Close the thread to save hardware.
    # sys.exit()


if __name__ == "__main__":
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', protocol_utils.port))
    socket_instance.listen(10)
    
    threads_list = []
    print("Server running ...")
    while True:
        conn, addr = socket_instance.accept()
        temp_thread = thread.Thread(target=message_handler, args=(conn, addr,))
        threads_list.append(temp_thread)
        temp_thread.start()
  