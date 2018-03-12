import socket
import threading
import os
import time

UDP_PORT = 5005
users = []
MESSAGE = ""
open_ch = ""
event = threading.Event()
event.set()
ans = threading.Event()
flage=0

def notification():
    print("UDP target port:", UDP_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    i = 0
    while i < 4:
        sock.sendto(MESSAGE.encode(), ('<broadcast>', UDP_PORT))
        time.sleep(0.5)
        i = i+1


def Receiving():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', UDP_PORT))
    while True:
        event.wait()
        print("1")
        data, addr = sock.recvfrom(1024)
        if data.decode().find("@#") != -1:
            writeback = data.decode().split("@#")
            flag = 0
            for item in users:
                if item == data.decode():
                    flag = 1
            if flag != 1:
                users.append(data.decode())
                print(writeback[0], "gdohndoh")
                chat = open("chat"+writeback[1]+".txt", "a")
                chat.close()
                if data.decode() != MESSAGE:
                    sock.sendto(MESSAGE.encode(), (writeback[0], UDP_PORT))
        elif data.decode().find("|") != -1:
            writeback = data.decode().split("|")
            print("received message:", data.decode())
            chat = open("chat"+writeback[0]+".txt", "a")
            chat.write("\n"+data.decode())
            chat.close()


def Sending(Actual_chat):
    while True:
        # ans.wait()
        Node = input()
        print(Node)
        print(open_ch)
        print(Actual_chat)
        # ans.wait()
        if Node == "back to menu":
            global flage
            flage=1
            break
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            i = 0
            while i < len(users):
                IP = users[i].split("@#")
                if Actual_chat == IP[1]:
                    print("SEDG")
                    event.clear()
                    a = (message+"|"+Node).encode()
                    sock.sendto(a, (IP[0], UDP_PORT))
                    chat = open("chat"+IP[1]+".txt", "a")
                    chat.write("\n"+a.decode())
                    chat.close()
                    ans.clear()
                    event.set()
                i += 1


def chat_update():
    print("open chat with")
    open_ch = input()
    ans.set()
    e = threading.Thread(target=Sending, args=(open_ch,))
    e.start()
    while True:
        if flage==1:
            os.system('CLS')
            break
        else:
            os.system('CLS')
            file = open("chat"+open_ch+".txt", "r")
            for line in file:
                print(line)
                #print(1)
            file.close()
            time.sleep(3)


def menu():
    while True:
        os.system('CLS')
        for item in users:
            print(item)
        chat_update()
        global flage
        flage=0



print("Please choose login")
#IPaddr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(
#    ("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
IPaddr=s.getsockname()[0]
s.close()
message = input()
MESSAGE = IPaddr+"@#"+message
users.append(MESSAGE)
chat = open("chat"+message+".txt", "a")
chat.close()
c = threading.Thread(target=Receiving)
c.start()
notification()

menu()

#d = threading.Thread(target=chat_update)
# d.start()

"""while True:
    for item in users:
        print(item)
        time.sleep(3)
    os.system('CLS')"""