# Created by: jdiegoh3@gmail.com
# This file contains the "protocol" to do operations between socket client and socket server
# Parse structure number1|op|number2

host = "localhost"
port = 9999


class MessageHandler(object):
    body = None

    def __init__(self, message):
        self.body = message.decode("utf-8")

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result


class MessageBuilder(object):
    operand1 = None
    operand2 = None
    operation = None

    def __init__(self, num1=None, num2=None, op=None):
        self.operand1 = num1
        self.operand2 = num2
        self.operation = op

    def message_builder(self):
        if self.operand1 and self.operand2 and self.operation:
            result = str(self.operand1) + "|" + str(self.operation) + "|" + str(self.operand2)
            return result

