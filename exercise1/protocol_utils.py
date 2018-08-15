# Created by: jdiegoh3@gmail.com
# This file contains the "protocol" to do operations between socket client and socket server
# Parse structure number1|op|number2

import math


host = "localhost"
port = 9999


class MessageHandler(object):
    body = None

    def __init__(self, message):
        self.body = message.decode("utf-8")

    def message_loads(self):
        if self.body != None:
            result = self.body.split("|")
            return result

    def add(self, num1, num2):
        result = float(num1) + float(num2)
        return result

    def mult(self, num1, num2):
        result = float(num1) * float(num2)
        return result

    def div(self, num1, num2):
        try:
            result = float(num1) / float(num2)
            return result
        except ZeroDivisionError as e:
            print("You cant divide by 0")
            return None
        

    def sqrt(self, num1, num2):
        try:
            result = math.pow(float(num1),(1/float(num2)))
            return result
        except ZeroDivisionError as e:
            print("You cant do root of a number by 0")
            return None
        

    def pow(self, num1, num2):
        result = math.pow(float(num1), float(num2))
        return result

    def sub(self, num1, num2):
        result = float(num1) - float(num2)
        return result

    def log(self, num1, num2):
        result = math.log(float(num1), float(num2))
        return result
        
    def switch_operations(self, operation):
        switcher = {
            "+": self.add,
            "*": self.mult,
            "-": self.sub,
            "/": self.div,
            "^": self.pow,
            "log": self.log,
            "sqrt": self.sqrt
        }
        return switcher.get(operation, None)

    def make_operation(self):
        data_array = self.message_loads()
        print(data_array)
        try:
            if not len(data_array) == 3:
                print("Incorrect format, contact the support")
                raise
        except Exception as e:
            print("Incorrect format, contact the support")
            raise

        function = self.switch_operations(data_array[1])
        print(function)
        if function != None:
            result = function(data_array[0], data_array[2])
            if(result):
                return result
            else:
                return "Invalid operation"
        else:
            return "Bad operation, check the simbols."

        


class MessageBuilder(object):
    operand1 = None
    operand2 = None
    operation =  None

    def __init__(self, num1, num2, op):
        self.operand1 = num1
        self.operand2 = num2
        self.operation = op
    
    def message_builder(self):
        if self.operand1 and self.operand2 and self.operation:
            result = str(self.operand1) + "|" + str(self.operation) + "|" + str(self.operand2)
            return result

