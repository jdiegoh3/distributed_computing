import lib.ProtocolUtils as protocolUtils


class RegisteredFunctions:
    @staticmethod
    def function(num1, num2):
        try:
            result = float(num1) / float(num2)
        except ZeroDivisionError:
            result = "You cant divide by 0"
        except ValueError:
            result = "The operands required be numbers."
        return result


def main():
    # Create server
    server = protocolUtils.ServerThread("localhost", 9003)
    server.register_class_functions(RegisteredFunctions())
    server.start()


if __name__ == '__main__':
    main()
