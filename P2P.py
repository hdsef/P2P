import socket
import threading
import os
import time

UDP_PORT = 5005
users = []
LogIp = ""
open_ch = ""
event = threading.Event()
event.set()
flage = 0

def notification():                             #BROADCAST оповещение сети о новом пользователе
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    i = 0
    while i < 4:
        sock.sendto(LogIp.encode(), ('<broadcast>', UDP_PORT))
        time.sleep(0.5)
        i = i + 1


def Receiving():                                #Получение UDP пакетов, пополнение списка участников,
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', UDP_PORT))
    while True:
        event.wait()
        data, addr = sock.recvfrom(1024)
        if data.decode().find("@#") != -1:
            writeback = data.decode().split("@#")
            flag = 0
            for item in users:
                if item == data.decode():
                    flag = 1
            if flag != 1:
                users.append(data.decode())
                chat = open("chat" + writeback[1] + ".txt", "a")
                chat.close()
                if data.decode() != LogIp:
                    sock.sendto(LogIp.encode(), (writeback[0], UDP_PORT))
        elif data.decode().find("|") != -1:
            writeback = data.decode().split("|")
            chat = open("chat" + writeback[0] + ".txt", "a")
            chat.write("\n" + data.decode())
            chat.close()


def Sending(Actual_chat):                   #Отправка сообщений
    while True:
        message = input()
        if message == "back to menu":
            global flage
            flage = 1
            break
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            i = 0
            while i < len(users):
                IP = users[i].split("@#")
                if Actual_chat == IP[1]:
                    event.clear()
                    a = (login + "|" + message).encode()
                    sock.sendto(a, (IP[0], UDP_PORT))
                    chat = open("chat" + IP[1] + ".txt", "a")
                    chat.write("\n" + a.decode())
                    chat.close()
                    event.set()
                i += 1


def chat_update():                                            #Обновление открытого чата
    print("open chat with")
    open_ch = input()
    e = threading.Thread(target=Sending, args=(open_ch,))
    e.start()
    while True:
        if flage == 1:
            os.system('CLS')
            break
        else:
            os.system('CLS')
            file = open("chat" + open_ch + ".txt", "r")
            for line in file:
                print(line)
            file.close()
            time.sleep(3)


def menu():                      #Основной цикл содержащий список участников, для                                 
    while True:                   #обновления нужно открыть любой чат и вернутся назад                        
        os.system('CLS')            #(Чтобы вернуться введите в открытом чате "back to menu")  
        for item in users:
            print(item)
        chat_update()
        global flage
        flage = 0


#IPaddr = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if
#not ip.startswith("127.")] or [[(s.connect(
#    ("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
#    [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP
#    found"])[0]
print("Please choose login")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
IPaddr = s.getsockname()[0]  #устанавливаем локальный IP машины
s.close()

login = input()        #login
LogIp = IPaddr + "@#" + login       #
users.append(LogIp)
chat = open("chat" + login + ".txt", "a")
chat.close()

c = threading.Thread(target=Receiving)
c.start()

notification()

menu()
