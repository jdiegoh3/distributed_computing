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


def main():

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()


def timer():
    while True:
        datetime_server.add(datetime.timedelta(seconds=1))
        print(datetime_server.get_time())
        time.sleep(1)
        os.system("cls")


if __name__ == '__main__':
    ntp = ntplib.NTPClient()
    # Provide the respective ntp server ip in below function
    response = ntp.request('3.south-america.pool.ntp.org')

    datetime_server = TimeFromServer(datetime.datetime.fromtimestamp(response.tx_time, pytz.timezone('America/Bogota')))

    # utc = datetime.datetime.utcnow().astimezone(pytz.utc)

    # Verify TimeZone are to UTC-5
    # utc_offset = utc - datetime_server
    main()
