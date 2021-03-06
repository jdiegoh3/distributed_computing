import lib.ProtocolUtils as protocolUtils


class RegisteredFunctions:
    @staticmethod
    def function(num1, num2):
        result = float(num1) - float(num2)
        return result


def main():
    # Create server
    server = protocolUtils.ServerThread("localhost", 9002)
    server.register_class_functions(RegisteredFunctions())
    server.start()
    print("Running sub server...")


if __name__ == '__main__':
    main()
