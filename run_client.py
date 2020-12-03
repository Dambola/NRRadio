from shared import cmd
from client.tcp import ClientTCP
from argparse import ArgumentParser
from config import Config


def main():
    arg_parser = ArgumentParser(description='Running the NRRadio Client...')
    arg_parser.add_argument('IP', metavar='ip', type=str, help='Server Ip to connect...')
    arg_parser.add_argument('PORT', metavar='port', type=int, help='Server Port to connect...')
    arg_parser.add_argument('UDPPORT', metavar='udpport', type=int, help='UDP Port to the transmission...')
    args = arg_parser.parse_args()

    config = Config
    ClientTCP(args.IP, args.PORT, args.UDPPORT, config)



if __name__ == '__main__':
    main()
    