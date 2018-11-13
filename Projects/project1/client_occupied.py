import lib.MyUtils as MyUtils

server_host = "localhost"
server_port = 99
occupied = True
cpu = 1000
memory = 1000


if __name__ == "__main__":
    client = MyUtils.Client(server_host, server_port, occupied, cpu, memory)
    client.start()
