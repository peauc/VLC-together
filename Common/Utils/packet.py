import Common.Network.Protobuff.Generated.packet_pb2 as packet_pb2


def create_packet(command: packet_pb2.defaultPacket.Commands, param: str) -> packet_pb2.defaultPacket:
    packet = packet_pb2.defaultPacket()
    packet.command = command
    packet.param = param
    return packet
