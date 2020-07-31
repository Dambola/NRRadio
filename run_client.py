from shared import cmd
from client.tcp import ClientTCP

def main():
    ClientTCP('localhost', 5000, 2500, 20, 1)

if __name__ == '__main__':
    main()
    