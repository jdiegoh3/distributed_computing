import socket
import threading
import datetime
import time
import pytz
import os
import ntplib


class TimeFromServer(object):
    time = None

    def __init__(self, actual_time):
        self.time = actual_time

    def add(self, timedelta):
        self.time = self.time + timedelta

    def get_time(self):
        return self.time

    def get_timestamp(self):
        return self.time.timestamp()

def client_handler(conn, address):
    while True:
        raw_data = conn.recv(1024)
        print(raw_data)
        conn.send(str(datetime_server.get_timestamp()).encode())

def main():
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()


def timer():
    while True:
        datetime_server.add(datetime.timedelta(seconds=1))
        time.sleep(1)

def pprint_timezone():
    val = 1
    while val:
        val = int(input("Get time? "))
        print("Datetime: ", datetime_server.get_time())
        print("Datetime: ", datetime_server.get_timestamp())

if __name__ == '__main__':
    ntp = ntplib.NTPClient()
    # Provide the respective ntp server ip in below function
    response = ntp.request('3.south-america.pool.ntp.org')

    datetime_server = TimeFromServer(datetime.datetime.fromtimestamp(response.tx_time, pytz.timezone('America/Bogota')))

    # utc = datetime.datetime.utcnow().astimezone(pytz.utc)

    # Verify TimeZone are to UTC-5
    # utc_offset = utc - datetime_server

    thread_get_time = threading.Thread(target=pprint_timezone)
    thread_get_time.start()

    main()

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, address = socket_instance.accept()
        print("New connection entry from ", address)

        temp_thread = threading.Thread(target=client_handler, args=(conn, address,))

        threads_list.append(temp_thread)
        temp_thread.start()
    
