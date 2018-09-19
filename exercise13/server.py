import socket
import sys
import threading as thread
import lib.ProtocolUtils as protocolUtils


def message_handler(conn, address):
    while True:
        raw_data = conn.recv(1024)
        received_data = protocolUtils.MessageHandler(raw_data).message_loads()

        if received_data[0] == "list_groups":
            print("New list_groups operation from ", address)
            conn.send(process_group_instance.get_all_groups())

        elif received_data[0] == "create_group":
            print("New group created by ", address)
            process_group_instance.add_process(address)
            conn.send("Group already created.".encode())

        elif received_data[0] == "join_group":
            error = False
            try:
                group_id = int(received_data[2])
            except ValueError as e:
                error = True
                conn.send("Incorrect group id.".encode())
            print("New request to join into a group from ", address, " to the group ", group_id)
            result = process_group_instance.add_process(address, group_id)
            if result:
                conn.send("You're now into the group".encode())
            else:
                conn.send("Incorrect group id.".encode())

        elif received_data[0] == "send_message":
            error = False
            try:
                group_id = int(received_data[2])
            except ValueError as e:
                error = True
                conn.send("Incorrect group id.".encode())
            list_members = process_group_instance.get_group(group_id)
            print("New message from ", address, " to the group ", group_id)
            if list_members:
                send_messages = thread.Thread(target=thread_broadcast_group, args=(list_members, received_data[1],))
                send_messages.start()
            else:
                error = True
                conn.send("Incorrect group id or the group doesn't have members.".encode())

            if not error:
                conn.send("Message sent.".encode())

        else:
            conn.send("yesss".encode())
    # Close the thread to save hardware.
    # sys.exit()


def thread_broadcast_group(list_of_members, message):
    for member in list_of_members:
        try:
            socket_temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_temp.connect((member[0], member[1]))
            socket_temp.send(message.encode())
        except Exception as e:
            print("Disconnected client.")
    # while True:
    #     socketInsa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     socketInsa.connect((address[0], address[1]))
    #     socketInsa.send("Yupale".encode())


if __name__ == "__main__":

    process_group_instance = protocolUtils.ProcessGroup()

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind(('', 9999))
    socket_instance.listen(10)

    threads_list = []
    print("Server running ...")
    while True:
        conn, address = socket_instance.accept()
        print("New connection entry from ", address)
        temp_thread = thread.Thread(target=message_handler, args=(conn, address,))
        threads_list.append(temp_thread)
        temp_thread.start()

