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

def ask_for_port() -> int:
    try:
        port = int(input("Port:"))
    except ValueError:
        print('The port should be a number')
        return ask_for_port()
    return port

def get_connection_infos() -> (str, int):
    ip = input("Server IP:")
    port = ask_for_port()
    return ip, port


def main():
    setup_logging()
    logging.debug(f"Current directory {os.getcwd()}")
    vlc = VLC()
    #TODO: If the informations are in the constant file. Do not prompt
    ip, port = get_connection_infos()
    server = ServerConnection(ip, port)
    slist = [server]
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
            out = slist
        r, w, e = select.select(slist, out, slist, 1)

        for item in r:
            data = item.socket.recv(1048)
            if data:
                packet = packet_pb2.defaultPacket()
                packet.ParseFromString(data)
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
    print('press Enter to quit')


if __name__ == '__main__':
    main()
