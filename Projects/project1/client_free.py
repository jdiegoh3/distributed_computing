import lib.MyUtils as MyUtils

server_host = "localhost"
server_port = 99
occupied = False
cpu = 1000
memory = 2000


if __name__ == "__main__":
    client = MyUtils.Client(server_host, server_port, occupied, cpu, memory)
    client.start()
