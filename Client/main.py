import sys
import logging
import select
import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2
from Client.UserInputHandler import UserInputHandler
from Client.ServerConnection import ServerConnection
from Client.vlc import VLC


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
    ip = '127.0.0.1'

    port = 8080
    vlc = VLC()
    server = ServerConnection(ip, port)
    uih = UserInputHandler()
    while 1:
        packets = uih.poll_and_consume_packets()
        if packets:
            for packet in packets:
                server.add_to_output_queue(packet)
        out = []

        # If the server need to send back information we append his socket to the list so it can be polled by select
        if len(server.output_queue) > 0:
            out.append(server)

        r, w, e = select.select([server], out, [server], 1)

        for item in r:
            data = item.socket.recv(1048)
            if data:
                logging.debug(f'received \"{data}\" from {item.socket.getpeername()}')
                packet = packet_pb2.defaultPacket()
                packet.ParseFromString(data)
                logging.debug(f'Received a packet {packet}')
                if packet.command == packet_pb2.defaultPacket.VLC_COMMAND:
                    vlc.x(packet.param)
                else:
                    print(packet.param)

        for item in w:
            logging.debug(f"sending {len(item.output_queue)} packets to host")
            for packet in item.output_queue:
                print(packet)
                logging.debug(f"sending {packet} to {item.socket.getpeername()}")
                serialized_data = packet.SerializeToString()
                item.socket.send(serialized_data)
            item.output_queue.clear()

        for item in e:
            logging.error(f"handling exceptionnal conditions for {item.sock.getpeername()}")
            item.close()
            logging.error(f"Connection to remote host was closed")
            exit(1)


if __name__ == '__main__':
    main()
