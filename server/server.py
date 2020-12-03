from shared.cmd import *
from shared.utils import convert_int_stringbyte, show_command, show_notify, show_fail
from threading import Thread
import socket as skt



# ---- Server Class

class Server:
    def __init__(self, host, port, config):
        self.host = host
        self.port = port
        self.config = config

        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)    
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.config.stations_number)

        self.online = True
        self.clients = dict()
        self.listen()

    def listen(self):
        # try:
        while self.online:
            conn, addr = self.socket.accept()
            ip, port = addr
            self.clients[(ip, port)] = {
                'tcp' : ServerTCPConnection(self, conn, addr),
                'udp' : ServerUDPConnection(self, conn, addr),
                'station' : -1,
                'udpport' : -1,
            }
            self.clients[(ip, port)]['tcp'].run()
        # except:
        #     self.online = False
    
    def setUDPPort(self, ip, port, udpport):
        self.clients[(ip, port)]['udpport'] = udpport
    
    def setStation(self, ip, port, station):
        self.clients[(ip, port)]['station'] = station



# ---- TCP Connection Class

class ServerTCPConnection(Thread):



    # ---- Thread Methods

    def __init__(self, server, connection, address):
        self.server = server
        self.connection = connection
        self.ip, self.port = address
        
    def run(self):
        # Connected
        self.online = True
        self.handshake = False
        show_notify(self.ip, self.port, 'TCP', 'is connected.')

        # Get the First Command
        size = self.connection.recv(self.server.config.header_size) 
        if size:
            size = size.decode('utf-8')
            cmd, msg = self.__getCommand(size)
            if cmd is not None and msg is not None:
                if cmd == COMMAND_HELLO:
                    try:
                        udpport = int(msg)
                        self.server.setUDPPort(self.ip, self.port, udpport)
                        
                        # Send the Welcome response when UDPPort is Set (Handshake)
                        self.sendWelcome()
                        self.handshake = True
                    except:
                        self.online = False
                else:
                    self.sendInvalidCommand()
            else:
                self.online = False
        else:
            self.online = False
            
        # Waiting for set Station
        while self.online:
            size = self.connection.recv(self.server.config.header_size)
            if size:
                size = size.decode('utf-8')
                cmd, msg = self.__getCommand(size)
                if cmd and msg:
                    if cmd == COMMAND_SET_STATION:
                        try:
                            station = int(msg)
                            self.server.setStation(self.ip, self.port, station)
                        except:
                            self.online = False
                    else:
                        self.sendInvalidCommand()
       
       # Disconnected
        show_fail(self.ip, self.port, 'TCP', 'disconnected.')



    # ---- Response Methods

    def sendWelcome(self):
        message = convert_int_stringbyte(REPLY_WELCOME, self.server.config.command_byte_size)
        message += str(self.server.config.stations_number) 
        self.__send(message)
    
    def sendAnnounce(self, music):
        message = convert_int_stringbyte(REPLY_ANNOUNCE, self.server.config.command_byte_size)
        message += str(music)
        self.__send(message)

    def sendInvalidCommand(self):
        message = convert_int_stringbyte(REPLY_INVALID_COMMAND, self.server.config.command_byte_size)
        self.online = False
        self.__send(message)



    # ---- Private Methods

    def __send(self, message):
        message_size = len(message)
        header = convert_int_stringbyte(message_size, self.server.config.header_size)
        all_message = header + message
        self.connection.sendall(bytes(all_message, 'utf-8'))
    
    def __getCommand(self, size):
        cmd, msg = None, None
        if size.strip().isdigit():
            size = int(size)
            data = self.connection.recv(size)
            if data:
                data = data.decode('utf-8')
                cbs = self.server.config.command_byte_size
                cmd, msg = int(data[:cbs]), data[cbs:]
                show_command(self.ip, self.port, 'TCP', size, cmd, msg)
        return cmd, msg



class ServerUDPConnection:
    def __init__(self, server, connection, address):
        self.server = server
        self.connection = connection
        self.ip, self.port = address