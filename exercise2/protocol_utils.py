# Created by: jdiegoh3@gmail.com
# This file contains the "protocol" to do operations between socket client and socket server
# Parse structure number1|op|number2

import math


host = "localhost"
port = 9999

server_add_host = "localhost"
server_add_port = 9991

server_sub_host = "localhost"
server_sub_port = 9992

server_root_host = "localhost"
server_root_port = 9993

server_mul_host = "localhost"
server_mul_port = 9994

server_div_host = "localhost"
server_div_port = 9995

server_pow_host = "localhost"
server_pow_port = 9996

server_log_host = "localhost"
server_log_port = 9997


class MessageHandler(object):
    body = None

    def __init__(self, message):
        self.body = message.decode("utf-8")

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result

    def switch_operations(self, operation):
        switcher = {
            "+": [server_add_host, server_add_port],
            "-": [server_sub_host, server_sub_port],
            "*": [server_mul_host, server_mul_port],
            "/": [server_div_host, server_div_port],
            "^": [server_pow_host, server_pow_port],
            "root": [server_root_host, server_root_port],
            "log": [server_log_host, server_log_port]
        }
        return switcher.get(operation, None)


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

