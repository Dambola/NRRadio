from shared.cmd import *
from shared.utils import convert_int_stringbyte, show_command, show_notify, show_fail
import socket as skt

class ClientTCP:
    def __init__(self, host, port, udp_port, config):
        self.host = host
        self.port = port
        self.udp_port = udp_port
        self.config = config
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)    
        self.socket.connect((self.host, self.port))
        self.run()
    
    def run(self):
        # Connect
        self.online = True
        self.handshake = False
        show_notify(self.host, self.port, 'TCP', 'is connected.')
        
        # Send the First Command
        try:
            self.sendHello()
        except:
            self.online = False
        
        # Get the Welcome response (Handshake)
        size = self.socket.recv(self.config.header_size) 
        if size:
            size = size.decode('utf-8')
            cmd, msg = self.__getCommand(size)
            if cmd is not None and msg is not None:
                if cmd == REPLY_WELCOME:
                    self.handshake = True
                    stations_number = int(msg)
                    show_command(self.host, self.port, 'TCP', size, cmd, f'The number of Stations is {stations_number}.')
                else:
                    self.online = False
            else:
                self.online = False
        else:
            self.online = False

        # Sending the Station to set
        while self.online:
            try:
                cmd = input('Set station: ')
                if cmd.lower() in ('q','quit','exit'):
                    self.online = False
                else:
                    self.sendSetStation(int(cmd))
            except:
                pass
        
        # Disconnected
        show_fail(self.host, self.port, 'TCP', 'disconnected.')

    def sendHello(self):
        message = convert_int_stringbyte(COMMAND_HELLO, self.config.command_byte_size)
        message += str(self.udp_port) 
        self.__send(message)
    
    def sendSetStation(self, stationNumber):
        message = convert_int_stringbyte(COMMAND_SET_STATION, self.config.command_byte_size)
        message += str(stationNumber) 
        self.__send(message)

    def __send(self, message):
        message_size = len(message)
        header = convert_int_stringbyte(message_size, self.config.header_size)
        all_message = header + message
        self.socket.sendall(bytes(all_message, 'utf-8'))

    def __getCommand(self, size):
        cmd, msg = None, None
        if size.strip().isdigit():
            size = int(size)
            data = self.socket.recv(size)
            if data:
                data = data.decode('utf-8')
                cbs = self.config.command_byte_size
                cmd, msg = int(data[:cbs]), data[cbs:]
                show_command(self.host, self.port, 'TCP', size, cmd, msg)
        return cmd, msg