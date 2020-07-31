from shared.cmd import *

def convert_int_stringbyte(value, max_length=16):
    if max_length < 1:
        max_length = 32
    value = str(value)

    if len(value) > max_length:
        return '9' * max_length
    fill_number = max_length - len(value)

    return ' ' * fill_number + value

def show_command(ip, port, type, size, command, message):
    print(f'{BLUE}[*][{command}] {BOLD}{ip}{BLUE}:{BOLD}{port}{BLUE}:{BOLD}{type}{BLUE}: {message}{RESET}') 

def show_notify(ip, port, type, message):
    print(f'{GREEN}[+] {BOLD}{ip}{GREEN}:{BOLD}{port}{GREEN}:{BOLD}{type} {GREEN}{message}{RESET}') 

def show_fail(ip, port, type, message):
    print(f'{RED}[-] {BOLD}{ip}{RED}:{BOLD}{port}{RED}:{BOLD}{type} {RED}{message}{RESET}') 
