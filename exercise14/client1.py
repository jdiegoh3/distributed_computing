import socket
import datetime
import threading
import pytz
import time
from lib.MyUtils import TimeBuilder, ClientIncrementBuilder

# This client desfaced 3 min.

def get_time_from_server():
    while True:
        time.sleep(10)
        socket_instance.send("yes".encode())
        result = socket_instance.recv(1024)
        datetime_updated = TimeBuilder(datetime.datetime.fromtimestamp(float(result.decode()), pytz.timezone('America/Bogota')))

        if datetime_updated.get_time() < datetime_actual.get_time():
            print("Estamos mas arriba macho")
            offset = datetime_actual.get_time() - datetime_updated.get_time()
            print(offset*2)
            client_increment.set_values(True, 2, offset*2, datetime.timedelta())

        elif datetime_updated.get_time() > datetime_actual.get_time():
            pass
        
        print("[Server]: Updated time.")


def timer(): 
    while True:
        if(client_increment.client_so_fast):
            if(client_increment.added_offset < client_increment.client_increment_time):
                client_increment.add_offsed_added(datetime.timedelta(seconds=1))
                datetime_actual.add(datetime.timedelta(seconds=1))
                time.sleep(client_increment.client_increment)
            else:
                client_increment.set_values(False, 1, 0, datetime.timedelta())
        else:
            datetime_actual.add(datetime.timedelta(seconds=1))
            time.sleep(client_increment.client_increment)

if __name__ == "__main__":

    datetime_actual = None
    datetime_updated = None

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.connect(("localhost", 9999))
    print(socket_instance.getsockname())
    
    
    socket_instance.send("yes".encode())
    result = socket_instance.recv(1024)

    client_increment = ClientIncrementBuilder()

    datetime_actual = TimeBuilder(datetime.datetime.fromtimestamp(float(result.decode()), pytz.timezone('America/Bogota')) + datetime.timedelta(minutes=1))

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()
    
    get_time_thread = threading.Thread(target=get_time_from_server)
    get_time_thread.start()


    while True:
        val = int(input("Get time zone? "))
        print("Resultado de la operacion fue ", datetime_actual.get_time())

    socket_instance.close()
