import math
import lib.ProtocolUtils as protocolUtils


class RegisteredFunctions:
    @staticmethod
    def function(num1, num2):
        try:
            result = math.pow(float(num1), 1/float(num2))
        except ZeroDivisionError:
            result = "Log base of 0 don't have sense."
        except ValueError:
            result = "The operands required be numbers."
        return result


def main():
    # Create server
    server = protocolUtils.ServerThread("localhost", 9007)
    server.register_class_functions(RegisteredFunctions())
    server.start()


if __name__ == '__main__':
    main()
