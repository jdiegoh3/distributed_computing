
class BColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_COLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PrintHelper(object):

    @staticmethod
    def switch(color):
        mapped_colors = {
            "red": BColors.FAIL,
            "blue": BColors.FAIL,
            "yellow": BColors.WARNING,
            "green": BColors.OK_GREEN,
        }
        return mapped_colors.get(color, None)

    def show(self, text, color):
        color_print = self.switch(color)
        if color_print:
            # print(text)
            print("{}{}{}".format(color_print, text, BColors.END_COLOR))
        else:
            print(text)


class MessageHandler(object):
    body = None

    def __init__(self, message):
        if not isinstance(message, str):
            message = message.decode("utf-8")
        self.body = message

    def message_loads(self):
        if self.body:
            result = self.body.split("|")
            return result


class MessageBuilder(object):
    message = ""
    operation = None

    def __init__(self, message_elements, op=None):
        self.message += op + "|"
        for string in message_elements:
            self.message += str(string) + "|"

    def get_message(self):
        return self.message.encode()


PPrint = PrintHelper()

