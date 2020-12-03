from shared import cmd
from server.server import Server
from config import Config
from argparse import ArgumentParser



def main():
    arg_parser = ArgumentParser(description='Running the NRRadio Server...')
    arg_parser.add_argument('IP', metavar='ip', type=str, help='Hosting Ip to the Server...')
    arg_parser.add_argument('PORT', metavar='port', type=int, help='Hosting Port to the Server...')
    args = arg_parser.parse_args()

    config = Config
    server = Server(args.IP, args.PORT, config)



if __name__ == '__main__':
    main()
    