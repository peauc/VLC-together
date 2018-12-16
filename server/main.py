from server import Server


def main():
    s = Server()
    while 1:
        command = input('>')
        s.send_command(command)


if __name__ == '__main__':
    main()
