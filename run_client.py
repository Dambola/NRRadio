from shared import cmd
from client.tcp import ClientTCP

def start_client():
    print(cmd.BOLD + ' WELCOME TO' + cmd.GREEN + ' NRRadio' + cmd.BOLD + '...' + cmd.RESET)

def main():
    start_client()

if __name__ == '__main__':
    main()
    ClientTCP('localhost', 5000, 2500, 20, 3)