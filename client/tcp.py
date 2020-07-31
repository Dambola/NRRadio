from shared import cmd
from shared.utils import convert_int_stringbyte
import socket as skt

class ClientTCP:
    def __init__(self, host, port, udp_port, header_size, command_byte_size):
        self.host = host
        self.port = port
        self.udp_port = udp_port
        self.header_size = header_size
        self.command_byte_size = command_byte_size
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)    
        self.socket.connect((self.host, self.port))
        self.online = True

        self.listen()
    
    def listen(self):
        while self.online:
            cmd = input('>>> ').split()
            self.__process(cmd)

    def sendHello(self):
        message = convert_int_stringbyte(cmd.COMMAND_HELLO, self.command_byte_size)
        message += str(self.udp_port) 
        self.__send(message)
    
    def sendSetStation(self, stationNumber):
        message = convert_int_stringbyte(cmd.COMMAND_SET_STATION, self.command_byte_size)
        message += str(stationNumber) 
        self.__send(message)

    def __send(self, message):
        message_size = len(message)
        header = convert_int_stringbyte(message_size, self.header_size)
        all_message = header + message
        self.socket.sendall(bytes(all_message, 'utf-8'))

    def __process(self, cmd):
        if len(cmd) == 2 and cmd[0] == 'setstation':
            if cmd[1].isdigit():
                station = int(cmd[1])
                self.sendSetStation(station)
        
        elif len(cmd) == 1 and cmd[0].lower() in ('q','quit','exit'):
            self.online = False