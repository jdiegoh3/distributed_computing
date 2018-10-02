import datetime

get_time_server_delay = 10


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