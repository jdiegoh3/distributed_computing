import lib.MyUtils as MyUtils
import socket
import sys
import threading


def client_handler(conn, address):
    while True:
        try:
            raw_data = conn.recv(1024)
            split_data = MyUtils.MessageHandler(raw_data).message_loads()
            print(split_data)
            operation = split_data[0]
            if operation == "occupied":
                print("Ocupado")
                unclassified_clients.remove_element(address)
                free_devices.remove_element(address)
                occupied_devices.add_element(address)
                conn.send("Received".encode())

            elif operation == "get_resources":
                print("PEDIDIENDO REQIEOS")
                free_devices_list = free_devices.list_elements()
                if len(free_devices_list) > 0:
                    message = MyUtils.MessageBuilder(free_devices_list[0], "free_device")
                else:
                    message = MyUtils.MessageBuilder([0], "free_device")
                conn.send(message.get_message())

            elif operation == "free":
                print("free")
                unclassified_clients.remove_element(address)
                occupied_devices.remove_element(address)
                free_devices.add_element(address)
                conn.send("Received".encode())
            print("free", free_devices.list_elements())
            print("occ", occupied_devices.list_elements())



        except Exception as e:
            print("Connection lost.", e)
            sys.exit(0)


if __name__ == '__main__':

    free_devices = MyUtils.FreeDevices()
    occupied_devices = MyUtils.OccupiedDevices()
    unclassified_clients = MyUtils.UnClassifiedClients()

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, address = socket_instance.accept()
        print("New connection entry from ", address)

        unclassified_clients.add_element(address)

        temp_thread = threading.Thread(target=client_handler, args=(conn, address,))

        threads_list.append(temp_thread)
        temp_thread.start()
