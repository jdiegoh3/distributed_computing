import lib.MyUtils as MyUtils
import threading

server_host = "LocalHost"
server_port = 999
occupied = False
cpu = 1000
memory = 2000


if __name__ == "__main__":
    print("Not working client")
    client = MyUtils.Client(server_host, server_port, occupied, cpu, memory)

    while 1:
        pass
