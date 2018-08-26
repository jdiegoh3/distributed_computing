from xmlrpc import client
import lib.ProtocolUtils as protocolUtils


def main():
    try:
        num1 = input("Insert a number: ")
        num2 = input("Insert a number: ")
        op = input("Insert the operation that you wants: ")

        message_builder = protocolUtils.MessageBuilder(num1, num2, op)

        # Get the absolute URL to do the connection directly
        server_op = names_resolver_server.get_operation_server(message_builder.operation)
        # Do the connection
        server_op = client.ServerProxy(server_op)

        op1, op2 = message_builder.get_operands()
        print("The result are: ", server_op.function(op1, op2))
    except client.Fault:
        print("Error: The operation is not supported")


if __name__ == '__main__':
    names_resolver_server = client.ServerProxy('http://localhost:9000')
    main()
