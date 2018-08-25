from xmlrpc import client
import lib.ProtocolUtils as protocolUtils


def switch_operations(operation):
    switcher = {
        "+": s.add,
        "*": s.mult,
        "-": s.sub,
        "/": s.div,
        "^": s.pow,
        "log": s.log,
        "root": s.sqrt
    }
    return switcher.get(operation, None)


def main():
    try:
        num1 = input("Insert a number: ")
        num2 = input("Insert a number: ")
        op = input("Insert the operation that you wants: ")

        message_builder = protocolUtils.MessageBuilder(num1, num2, op)
        function_op = switch_operations(message_builder.operation)

        op1, op2 = message_builder.get_operands()
        print("The result are: ", function_op(op1, op2))

    except client.Fault:
        print("Error: The operation is not supported")


if __name__ == '__main__':
    s = client.ServerProxy('http://localhost:9000')
    main()
