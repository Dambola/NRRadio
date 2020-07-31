from shared import cmd
from server.server import Server

def main():
    Server('localhost', 5000, 200, 20, 1, 10)
    
if __name__ == '__main__':
    main()
    