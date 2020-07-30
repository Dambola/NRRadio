from shared import cmd
from shared.utils import convert_int_stringbyte
from threading import Thread
import socket as skt

# def on_new_client(clientsocket,addr):
#     while True:
#         msg = clientsocket.recv(1024)
#         #do some checks and if msg == someWeirdSignal: break:
#         print addr, ' >> ', msg
#         msg = raw_input('SERVER >> ')
#         #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
#         clientsocket.send(msg)
#     clientsocket.close()

# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# port = 50000                # Reserve a port for your service.

# print 'Server started!'
# print 'Waiting for clients...'

# s.bind((host, port))        # Bind to the port
# s.listen(5)                 # Now wait for client connection.

# print 'Got connection from', addr
# while True:
#    c, addr = s.accept()     # Establish connection with client.
#    thread.start_new_thread(on_new_client,(c,addr))
#    #Note it's (addr,) not (addr) because second parameter is a tuple
#    #Edit: (c,addr)
#    #that's how you pass arguments to functions when creating new threads using thread module.
# s.close()

class Server:
    def __init__(self, host, port, max_connections):
        self.stations_number = stations_number
        self.header_size = header_size
        self.command_byte_size = command_byte_size
        self.max_connections = max_connections

        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)    
        self.socket.bind((self.host, self.port))
        self.socket.listen(max_connections)

        self.online = True
        self.clients = dict()
        self.listen()

    def listen(self):
        try:
            while self.online:
                conn, addr = self.socket.accept()
                self.clients[addr] = {
                    'tcp' : ServerTCPConnection(conn, addr, self.stations_number, self.header_size, self.command_byte_size)
                }
                self.clients[addr]['tcp'].start()
        except:
            self.online = False




class ServerTCPConnection(Thread):
    def __init__(self, connection, address, stations_number, header_size, command_byte_size):
        self.connection = connection
        self.address = address
        self.stations_number = stations_number
        self.header_size = header_size
        self.command_byte_size = command_byte_size
    
    def run(self):
        pass

    def sendWelcome(self):
        message = convert_int_stringbyte(cmd.REPLY_HELLO, self.command_byte_size)
        message += str(self.stations_number) 
        self.__send(message)
    
    def sendAnnounce(self, music):
        message = convert_int_stringbyte(cmd.REPLY_ANNOUNCE, self.command_byte_size)
        message += str(music)
        self.__send(message)

    def sendInvalidCommand(self, stationNumber):
        message = convert_int_stringbyte(cmd.REPLY_INVALID_COMMAND, self.command_byte_size)
        message += str(stationNumber) 
        self.__send(message)

    def __send(self, message):
        message_size = len(message)
        header = convert_int_stringbyte(message_size, self.header_size)
        all_message = header + message
        self.connection.sendall(bytes(all_message, 'utf-8'))

class ServerUDPConnection:
    pass