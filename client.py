import socket
import time


PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), PORT))

# msg = s.recv(1024)
# print(msg.decode('utf-8'))

while True:
    print("MENU:\n")
    print("'ASK' To Generate IP_ADDRESS\n")
    print("'RENEW' IP_ADDRESS\n")
    print("'RELEASE'  IP_ADDRESS\n")
    print("'STATUS'  IP_ADDRESS\n")
    print("====================")
    command = input("\nEnter a command: ")
    s.send(bytes(command, 'utf-8'))
    msg = s.recv(1024)
    print(" ======= SERVER SAYS =======")
    print(msg.decode('utf-8'))
    print(" =======        =======")
    time.sleep(1)