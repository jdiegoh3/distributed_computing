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
        self.operand1 = float(num1)
        self.operand2 = float(num2)
        self.operation = op

    def get_operands(self):
        try:
            self.operand1 = float(self.operand1)
            self.operand2 = float(self.operand2)
        except ValueError:
            print("Not be numbers")
        return self.operand1, self.operand2

    def message_builder(self):
        result = str(self.operand1) + "|" + str(self.operation) + "|" + str(self.operand2)
        return result