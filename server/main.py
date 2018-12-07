from network import Network


def main():
    s = Network()
    while 1:
        command = input('>')
        s.send_command(command)


if __name__ == '__main__':
    main()
