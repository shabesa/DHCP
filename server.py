import socket
import random
import time


IP_LIMIT = 255

TIME_OUT = 5

HOST_IP = "0.0.0.0"
PORT = 1234

# echo-server.py


SERVER_ERROR = 500

ip_dict = {HOST_IP : [False, None],
           '0.0.0.1': [True, '05:10:52']} # [is_avaiable, time, is_active, MAC_ADDRESS] | Note: we did not implement the other aspects like checking device mac for simplicity

def ask():
    dict_len = len(ip_dict)
    for i in range(dict_len):
        ip = list(ip_dict.keys())
        print(ip[i])
        if ip_dict[ip[i]][0] == True:
            print(f"Offer {ip[i]}")
            ip_dict[ip[i]] = [False, time.time()]
            return ip[i]
    ip = list(ip_dict)[-1].split(".")
    print(ip)
    for i in range(3, -1, -1):
        if int(ip[i]) < IP_LIMIT:
            ip[i] = str(int(ip[i])+1)
            break
        else:
            ip[i] = "0"
    ip = ".".join(ip)
    ip_dict.update({ip: [True, time.time()]})
    print(f"Offer {ip}")
    return ip
            
def renew(userIP):
    if(userIP not in ip_dict.keys() or ip_dict[userIP][0] == False):
        print(SERVER_ERROR + " ERROR" + ": INVALID REQUEST")
    else:
        # check if device is correct LATER
        ip_dict.userIP[1] = time.strftime("%H:%M:%S")

def release(userIP):
    if(userIP not in ip_dict.keys() or ip_dict[userIP][0] == False):
        print(SERVER_ERROR + " ERROR" + ": INVALID REQUEST")
    else:
        ip_dict.userIP = [True, '']
        return "RELEASED " + str(userIP)

        
def status(userIP):
    if(userIP not in ip_dict.keys() or ip_dict[userIP][0] == True):
        print(userIP + " AVAILABLE")
        return userIP + " AVAILABLE"
    else:
        print(userIP + " ASSIGNED")
        return userIP + " ASSIGNED"


def net_comms(command, userDevice, conn, userIP = ""):
    match command:
        case "ASK":
            conn.send(bytes(ask(), "utf-8"))
        case "RENEW":
            conn.send(bytes(renew(userDevice, userIP), "utf-8"))
        case "RELEASE":
            conn.send(bytes(release(userIP), "utf-8"))
        case "STATUS":
            conn.send(bytes(status(userIP), "utf-8"))

def time_out():
    for ip in ip_dict:
        if ip != HOST_IP:
            if ip_dict[ip][0] == False:
                print(time.time())
                print (time.time() - float(ip_dict[ip][1]))
                if time.time() - float(ip_dict[ip][1]) > TIME_OUT:
                    ip_dict[ip] = [True, ""]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT))
        s.listen()
        conn, address = s.accept()
        with conn:
            print(f"Connected by {address}")
            while True:
                data = conn.recv(1024)
                data = data.decode("utf-8").split(" ")
                if len(data) > 0:
                    match data[0]:
                        case "ASK":
                            conn.send(ask().encode("utf-8"))
                        case "RENEW":
                            conn.send(renew(data[1]).encode("utf-8"))
                        case "RELEASE":
                            conn.send(release(data[1]).encode("utf-8"))
                        case "STATUS":
                            conn.send(status(data[1]).encode("utf-8"))
                        case _:
                            conn.send(bytes("INVALID REQUEST", "utf-8"))
                # conn.send(bytes("Welcome to the server!","utf-8"))


if __name__ == "__main__":
    main()