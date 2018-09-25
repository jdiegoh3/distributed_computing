import threading
import datetime
import time
import pytz
import ntplib


def timer():
    seconds = 0
    while True:
        time.sleep(1)
        seconds = seconds+1
        print(seconds)


def main():
    ntp = ntplib.NTPClient()
    # Provide the respective ntp server ip in below function
    response = ntp.request('0.south-america.pool.ntp.org')

    datetime_server = datetime.datetime.fromtimestamp(response.tx_time, pytz.timezone('America/Bogota'))

    utc = datetime.datetime.utcnow().astimezone(pytz.utc)

    # Verify TimeZone are to UTC-5
    utc_offset = utc - datetime_server
    print(utc_offset)
    # timer_thread = threading.Thread(target=timer)
    # timer_thread.start()


if __name__ == '__main__':
    main()
