from xmlrpc import client
import lib.ProtocolUtils as protocolUtils


def main():
    try:
        num1 = input("Insert a number: ")
        num2 = input("Insert a number: ")
        op = input("Insert the operation that you wants: ")

        message_builder = protocolUtils.MessageBuilder(num1, num2, op)
        function_op = protocolUtils.ClientThread(server_of_names.get_server(message_builder.operation))
        function_op.start()

        op1, op2 = message_builder.get_operands()
        print("The result are: ", function_op.call_function(op1, op2))

    except client.Fault as e:
        print(e)


if __name__ == '__main__':
    server_of_names = client.ServerProxy('http://localhost:8060')
    main()
