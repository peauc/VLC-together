import sys
import logging
import select
import os
import time
import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2
from Client.UserInputHandler import UserInputHandler
from Client.ServerConnection import ServerConnection
from Client.vlc import VLC


def setup_logging():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def get_connection_infos():
    ip = input("Server IP:")
    port = int(input("Port:"))
    return ip, port


def main():
    setup_logging()
    logging.debug(f"Current directory {os.getcwd()}")
    #TODO: If the informations are in the constant file. Do not prompt
    #ip, port = get_connection_infos()
    vlc = VLC()
    vlc.x('shutdown')
    time.sleep(10)
    return (0)
    server = ServerConnection(ip, port)
    uih = UserInputHandler()
    # TODO: Give the client a way to quit gracefully
    while uih.should_run():
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
                packet = packet_pb2.defaultPacket()
                packet.ParseFromString(data)
                logging.debug(f'Received a packet {packet}')
                if packet.command == packet_pb2.defaultPacket.VLC_COMMAND:
                    vlc.x(packet.param)
                else:
                    print(packet.param)
            else:
                logging.debug(f"0 byte read")

        for item in w:
            for packet in item.output_queue:
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
