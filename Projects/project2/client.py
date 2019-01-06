import lib.MyUtilsClient as MyUtilsClient

server_host = "192.168.0.19"
server_port = 9999


if __name__ == "__main__":
    print("Occupied client")
    client = MyUtilsClient.Client(server_host, server_port)

    while 1:
        print("Options:")
        print("1: List my page numbers")
        print("2: Show my local page")
        print("3: Need other page")
        mss = input('Type the option and press enter')
