import datetime
import socket

get_time_server_delay = 10


class ProcessManager(object):
    process_list = []
    datetime_list = []

    def __init__(self):
        pass

    def add_process(self, process_info):
        self.process_list.append(process_info)

    def add_datetime(self, datetime_from):
        self.datetime_list.append(datetime_from)

    def get_datetime_average(self):
        avg = 0
        counter = 0

        for time in self.datetime_list:
            avg = avg + time
            counter = counter + 1

        return avg/counter

    def send_broadcast(self):
        for process in self.process_list:
            try:
                socket_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_temp.connect((process[0], process[1]))
                socket_temp.send(str(self.get_datetime_average()).encode())
            except Exception as e:
                print("Client {} disconnected.".format(str(process[1])))


class TimeBuilder(object):
    time = None

    def __init__(self, actual_time):
        self.time = actual_time

    def add(self, timedelta):
        self.time = self.time + timedelta

    def get_time(self):
        return self.time

    def get_timestamp(self):
        return self.time.timestamp()


class ClientIncrementBuilder(object):
    client_so_fast = False
    client_increment = 1
    client_increment_time = 0
    added_offset = datetime.timedelta()
    
    def set_values(self, client_so_fast, client_increment, client_increment_time, added_offset):
        self.client_so_fast = client_so_fast
        self.client_increment = client_increment
        self.client_increment_time = client_increment_time
        self.added_offset = added_offset
    
    def add_offsed_added(self, timedelta):
        self.added_offset = self.added_offset + timedelta