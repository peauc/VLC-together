import logging
from Client import TerminalAsyncReader
from Common.Network.packet import Packet, Commands


class CommandInterpreter:
    def __init__(self):
        self.__reader = TerminalAsyncReader.TerminalAsyncReader()
        self.__reader.start()
        self.__command_list = {
            'join': Commands.JOIN,
            'quit': Commands.QUIT
        }

    def get_data(self) -> [str]:
        with self.__reader.lock:
            commands = self.__reader.command_queue.copy()
            self.__reader.command_queue.clear()
        return commands

    """
        This method will return a list of command to be sent to the distant server
    """
    def parse_and_execute_commands(self) -> [Packet]:
        packets = []
        if self.__reader.is_data_available():
            commands = self.get_data()
            packets = self.parse_commands(commands)
        return packets

    def parse_commands(self, commands: [str]) -> [Packet]:
        packets = []
        for c in commands:
            if c[0] == '/':
                cleaned_command = c[1:]
                ret = self.interpret_command(cleaned_command)
                if ret is not None:
                    packets.append(ret)
            else:
                packets.append(self.__build_vlc_command(c))
        return packets

    def interpret_command(self, command_line) -> Packet or None:
        # We split the command into two part, in the first, the action, in the second the params
        command = command_line.split(' ', 1)
        packet = Packet()
        if command[0] in self.__command_list:
            packet.command_nb = self.__command_list[command[0]]
            packet.param = command[1]
            return packet
        else:
            # Todo : Display the list of available commands
            logging.error("Command not recognized")
            return None

    def __build_vlc_command(self, command) -> Packet:
        packet = Packet()
        packet.command_nb = Commands.VLC_COMMAND
        packet.param = command
        return packet

