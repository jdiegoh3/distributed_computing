import socket
import threading
import datetime
import time
import pytz
import os
import sys
import ntplib
from lib.MyUtils import TimeBuilder, ProcessManager


def client_handler(conn, address):
    while True:
        try:
            raw_data = conn.recv(1024)
            split_data = raw_data.decode("utf-8").split("|")
            print(15)
            if split_data[0] == "my_time":
                print(split_data[1])
                timestamp = float(split_data[1])
                process_manager.add_datetime(timestamp)
                process_manager.send_broadcast()
            print("Message received from ", split_data)
            conn.send("Received".encode())
        except Exception as e:
            print("Connection lost.")
            sys.exit(0)

def main():
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()


def timer():
    while True:
        if datetime_server:
            datetime_server.add(datetime.timedelta(seconds=1))
            time.sleep(1)


if __name__ == '__main__':
    # utc = datetime.datetime.utcnow().astimezone(pytz.utc)

    # Verify TimeZone are to UTC-5
    # utc_offset = utc - datetime_server
    datetime_server = None
    main()

    process_manager = ProcessManager()
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, address = socket_instance.accept()
        print("New connection entry from ", address)

        process_manager.add_process(address)

        temp_thread = threading.Thread(target=client_handler, args=(conn, address,))

        threads_list.append(temp_thread)
        temp_thread.start()

