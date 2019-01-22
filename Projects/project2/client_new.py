import utils.client_lib as library
from utils.general_utils import PPrint
server_address = "192.168.0.5"
server_port = 9999


def main():
    try:
        library.Client(server_address, server_port)
    except Exception as e:
        if isinstance(e, ConnectionRefusedError):
            PPrint.show("No connection with the server. Do you start him?", "red")
        else:
            PPrint.show("Unknown error connecting with the server", "red")


if __name__ == "__main__":
    main()
