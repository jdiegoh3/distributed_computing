import lib.MyUtils as MyUtils
import socket
import random
import threading


def client_handler(conn, address):
    while True:
        raw_data = conn.recv(1024)
        split_data = MyUtils.MessageHandler(raw_data).message_loads()
        print(split_data)
        operation = split_data[0]

        if operation == "not_working":
            try:
                processor = split_data[1]
                ram = split_data[2]
            except Exception as e:
                # Return
                message = MyUtils.MessageBuilder([0], "400")
                conn.send(message.get_message())

            identifier = str(address[0]) + str(address[1])
            body = {
                "ip": address[0],
                "port": address[1],
                "cpu": processor,
                "ram": ram
            }
            unclassified_clients.remove_element(identifier)
            occupied_devices.remove_element(identifier)
            free_devices.add_element(identifier, body)
            print(free_devices.list_elements())
            message = MyUtils.MessageBuilder([0], "received")
            conn.send(message.get_message())

        elif operation == "occupied":
            try:
                processor = split_data[1]
                ram = split_data[2]
            except Exception as e:
                # Return
                message = MyUtils.MessageBuilder([0], "400")
                conn.send(message.get_message())

            identifier = str(address[0]) + str(address[1])
            body = {
                "ip": address[0],
                "port": address[1],
                "cpu": processor,
                "ram": ram
            }
            unclassified_clients.remove_element(identifier)
            free_devices.remove_element(identifier)
            occupied_devices.add_element(identifier, body)
            print(occupied_devices.list_elements())

            message = MyUtils.MessageBuilder([0], "received")
            conn.send(message.get_message())

        elif operation == "get_resources":
            try:
                processor = split_data[1]
                ram = split_data[2]
            except Exception as e:
                # Return
                message = MyUtils.MessageBuilder([0], "400")
                conn.send(message.get_message())

            message = MyUtils.MessageBuilder([0], "400")
            if processor and ram:
                device_list = free_devices.list_elements()
                for device in device_list:
                    if device.get("cpu", None) >= processor and device.get("ram") >= ram:
                        message = MyUtils.MessageBuilder([device.get("ip"), device.get("port")], "not_working")
            else:
                device_list = free_devices.list_elements()
                rand = random.randint(0, len(device_list))
                device = free_devices.list_elements()[list(free_devices.list_elements())[rand]]
                message = MyUtils.MessageBuilder([device.get("ip"), device.get("port")], "not_working")

            conn.send(message.get_message())


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

        identifier = str(address[0]) + str(address[1])
        body = {
            "ip": address[0],
            "port": address[1],
            "cpu": None,
            "ram": None
        }

        unclassified_clients.add_element(identifier, body)

        temp_thread = threading.Thread(target=client_handler, args=(conn, address,))

        threads_list.append(temp_thread)
        temp_thread.start()
