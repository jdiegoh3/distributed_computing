import math
import lib.ProtocolUtils as protocolUtils


class RegisteredFunctions:
    @staticmethod
    def function(num1, num2):
        try:
            result = math.pow(float(num1), 1/float(num2))
        except ZeroDivisionError:
            result = "You cant do root of a number by 0"
        except ValueError:
            result = "The operands required be numbers."
        return result


def main():
    # Create server
    server = protocolUtils.ServerThread("localhost", 9006)
    server.register_class_functions(RegisteredFunctions())
    server.start()
    print("Running root server...")


if __name__ == '__main__':
    main()
