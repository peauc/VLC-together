import time
import sys
import logging
import select
import pickle
from Client.CommandInterpreter import CommandInterpreter
from Client.ServerConnection import ServerConnection


def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def get_connection_infos():
    ip = input("Please input connection Ip")
    port = input("Please enter connection port")
    return ip, port


def main():
    setup_logging()
    # ip, port = get_connection_infos()
    # TODO: Remove testing placeholder
    ip = 'localhost'

    port = 8080
    server = ServerConnection(ip, port)
    ci = CommandInterpreter()
    while 1:
        packets = ci.parse_and_execute_commands()
        if packets:
            for packet in packets:
                server.add_to_output_queue(packet)
        out = []

        if len(server.output_queue) > 0:
            out.append(server)

        r, w, e = select.select([server], out, [server], 1)

        for item in r:
            data = item.socket.recv(1048)
            if data:
                logging.debug(f'received \"{data}\" from {item.socket.getpeername()}')
                packet = pickle.loads(data)
                logging.debug(f'Received a packet {packet}')

        for item in w:
            logging.debug(f"sending {len(item.output_queue)} packets to host")
            for packet in item.output_queue:
                print(packet)
                logging.debug(f"sending {packet} to {item.socket.getpeername()}")
                item.socket.send(pickle.dumps(packet))
            item.output_queue.clear()
        # TODO: Add the exceptionnal case


if __name__ == '__main__':
    main()
