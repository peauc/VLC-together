import logging
from Client import TerminalAsyncReader
from Common.Utils.packet import create_packet
import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2


class UserInputHandler(object):
    def __init__(self):
        self.__reader = TerminalAsyncReader.TerminalAsyncReader()
        self.__reader.start()
        # TODO: See maybe to add a tuple containing both the command_nb and the function to call
        self.__command_list = {
            'join': self.__join,
            'quit': self.__quit
        }

    def __del__(self):
        self.__reader.stop()
        self.__reader.join()

    def get_data(self) -> [str]:
        with self.__reader.lock:
            commands = self.__reader.command_queue.copy()
            self.__reader.command_queue.clear()
        return commands

    """
        This method will return a list of packets to be sent back to the server 
    """
    def poll_and_consume_packets(self) -> [packet_pb2.defaultPacket]:
        packets = []
        if self.__reader.is_data_available():
            commands = self.get_data()
            packets = self.parse_commands(commands)
        return packets

    """
        This method will send VLC command to VLC and prepare the others to be sent back to the server
    """
    def parse_commands(self, commands: [str]) -> [packet_pb2.defaultPacket.Commands]:
        packets = []
        for c in commands:
            # If the first character is a forward slash it means the command is to be interpreted by VLC-Together
            if c[0] == '/':
                cleaned_command = c[1:]
                ret = self.consume_commands(cleaned_command)
                if ret is not None:
                    packets.append(ret)
            else:
                packets.append(self.__build_vlc_command(c))
        return packets

    def consume_commands(self, full_command_line) -> packet_pb2.defaultPacket.Commands or None:
        # We split the command into two part, in the first, the action, in the second the params
        command = full_command_line.split(' ', 1)
        if command[0] in self.__command_list:
            if len(command) == 1:
                param = ''
            else:
                param = command[1]
            packet = self.__command_list[command[0]](param)
            return packet
        else:
            # Todo : Display the list of available commands
            logging.error("Command not recognized")
            return None

    def __build_vlc_command(self, vlc_command) -> packet_pb2.defaultPacket:
        packet = packet_pb2.defaultPacket()
        packet.command = packet_pb2.defaultPacket.VLC_COMMAND
        packet.param = vlc_command
        logging.info(f"Sending {vlc_command} to room")
        return packet

    def __quit(self, param: str) -> packet_pb2.defaultPacket:
        self.__reader.stop()
        packet = create_packet(packet_pb2.defaultPacket.QUIT, param)
        logging.info("Quitting the program and leaving rooms")
        return packet

    def __join(self, param: str) -> packet_pb2.defaultPacket:
        packet = create_packet(packet_pb2.defaultPacket.JOIN, param)
        logging.info(f"Joining the room {param}")
        return packet

    def should_run(self) -> bool:
        return self.__reader.is_alive()

