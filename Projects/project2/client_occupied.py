import lib.MyUtils as MyUtils
import threading

server_host = "192.168.0.19"
server_port = 9999
occupied = True
cpu = 1000
memory = 1000


if __name__ == "__main__":
    print("Occupied client")
    client = MyUtils.Client(server_host, server_port, occupied, cpu, memory)

    while 1:
        mss = input('For create new task to delegate press enter')
        cpu = input('cpu: ')
        memory = input('memory: ')
        time_factor = input('time_factor: ')
        client.delegate_task(int(cpu), int(memory), int(time_factor))
