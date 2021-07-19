import socket
import json
import requests
import threading
import os
import time
import tkinter as tk
from tkinter import Canvas, filedialog, Text
clients = []


def getInfo():
    global HOST_NAME
    HOST_NAME = socket.gethostname()
    global HOST_ADDRESS
    HOST_ADDRESS = socket.gethostbyname(HOST_NAME)
    print(HOST_NAME)
    print(HOST_ADDRESS)


def choosePort():
    global PORT
    PORT = int(input("Please choose a port that will be used for connection: "))


def Register(username, password):
    try:
        file = open('UserPass.txt', 'a')
        file.writelines(username+","+password+'\n')
    except Exception as e:
        print('client left')
    finally:
        file.close()


def GuiFileDataCacBankChoClientKhiTracuu(ClientConnection, NgayThangData):
    datavcb = GetsizeData("./17072021/vcb.json")
    lenvcb = DodaiChuoiso(datavcb)
    ClientConnection.send(lenvcb.encode())
    ClientConnection.send(datavcb.encode())

    datactg = GetsizeData("./"+NgayThangData+"/ctg.json")
    lenctg = DodaiChuoiso(datactg)
    ClientConnection.send(lenctg.encode())
    ClientConnection.send(datactg.encode())

    datatcb = GetsizeData("./"+NgayThangData+"/tcb.json")
    lentcb = DodaiChuoiso(datatcb)
    ClientConnection.send(lentcb.encode())
    ClientConnection.send(datatcb.encode())

    databid = GetsizeData("./"+NgayThangData+"/bid.json")
    lenbid = DodaiChuoiso(databid)
    ClientConnection.send(lenbid.encode())
    ClientConnection.send(databid.encode())

    datastb = GetsizeData("./"+NgayThangData+"/stb.json")
    lenstb = DodaiChuoiso(datastb)
    ClientConnection.send(lenstb.encode())
    ClientConnection.send(datastb.encode())

    SendFileExchangeToClient(ClientConnection, "./" +
                             NgayThangData+"/vcb.json", int(datavcb))
    SendFileExchangeToClient(ClientConnection, "./" +
                             NgayThangData+"/ctg.json", int(datactg))
    SendFileExchangeToClient(ClientConnection, "./" +
                             NgayThangData+"/tcb.json", int(datatcb))
    SendFileExchangeToClient(ClientConnection, "./" +
                             NgayThangData+"/bid.json", int(databid))
    SendFileExchangeToClient(ClientConnection, "./" +
                             NgayThangData+"/stb.json", int(datastb))


def GuiFileDataNgayMoiChoClientHomNay(ClientConnection):
    datavcb = GetsizeData("vcb.json")
    lenvcb = DodaiChuoiso(datavcb)
    ClientConnection.send(lenvcb.encode())
    ClientConnection.send(datavcb.encode())

    datactg = GetsizeData("ctg.json")
    lenctg = DodaiChuoiso(datactg)
    ClientConnection.send(lenctg.encode())
    ClientConnection.send(datactg.encode())

    datatcb = GetsizeData("tcb.json")
    lentcb = DodaiChuoiso(datatcb)
    ClientConnection.send(lentcb.encode())
    ClientConnection.send(datatcb.encode())

    databid = GetsizeData("bid.json")
    lenbid = DodaiChuoiso(databid)
    ClientConnection.send(lenbid.encode())
    ClientConnection.send(databid.encode())

    datastb = GetsizeData("stb.json")
    lenstb = DodaiChuoiso(datastb)
    ClientConnection.send(lenstb.encode())
    ClientConnection.send(datastb.encode())

    SendFileExchangeToClient(ClientConnection, "vcb.json", int(datavcb))
    SendFileExchangeToClient(ClientConnection, "ctg.json", int(datactg))
    SendFileExchangeToClient(ClientConnection, "tcb.json", int(datatcb))
    SendFileExchangeToClient(ClientConnection, "bid.json", int(databid))
    SendFileExchangeToClient(ClientConnection, "stb.json", int(datastb))


def XulyNhuCauClient(ClientConnection):
    try:
        temp = ClientConnection.recv(1024).decode()
        choose = int(temp)
        if choose == 1:
            username = ClientConnection.recv(1024).decode()
            password = ClientConnection.recv(1024).decode()
            if(Docfile(username, password) == 1):
                ClientConnection.send("Dang nhap thanh cong".encode("utf-8"))

                datavcb = GetsizeData("vcb.json")
                lenvcb = DodaiChuoiso(datavcb)
                ClientConnection.send(lenvcb.encode())
                ClientConnection.send(datavcb.encode())

                datactg = GetsizeData("ctg.json")
                lenctg = DodaiChuoiso(datactg)
                ClientConnection.send(lenctg.encode())
                ClientConnection.send(datactg.encode())

                datatcb = GetsizeData("tcb.json")
                lentcb = DodaiChuoiso(datatcb)
                ClientConnection.send(lentcb.encode())
                ClientConnection.send(datatcb.encode())

                databid = GetsizeData("bid.json")
                lenbid = DodaiChuoiso(databid)
                ClientConnection.send(lenbid.encode())
                ClientConnection.send(databid.encode())

                datastb = GetsizeData("stb.json")
                lenstb = DodaiChuoiso(datastb)
                ClientConnection.send(lenstb.encode())
                ClientConnection.send(datastb.encode())

                datasbv = GetsizeData("sbv.json")
                lensbv = DodaiChuoiso(datasbv)
                ClientConnection.send(lensbv.encode())
                ClientConnection.send(datasbv.encode())

                SendFileExchangeToClient(
                    ClientConnection, "vcb.json", int(datavcb))
                SendFileExchangeToClient(
                    ClientConnection, "ctg.json", int(datactg))
                SendFileExchangeToClient(
                    ClientConnection, "tcb.json", int(datatcb))
                SendFileExchangeToClient(
                    ClientConnection, "bid.json", int(databid))
                SendFileExchangeToClient(
                    ClientConnection, "stb.json", int(datastb))
                SendFileExchangeToClient(
                    ClientConnection, "sbv.json", int(datasbv))

                while True:
                    # Lỗi ở đây bởi vì mình chỉ bấm Tra cứu có 1 lần
                    CheckTracuu = ClientConnection.recv(1024).decode()
                    if(CheckTracuu == "Tracuu"):
                        while True:
                            KiemTraDataSeGui = ClientConnection.recv(
                                1024).decode()
                            if(KiemTraDataSeGui == "17072021"):
                                GuiFileDataCacBankChoClientKhiTracuu(
                                    ClientConnection, "17072021")
                            elif(KiemTraDataSeGui == "18072021"):
                                GuiFileDataCacBankChoClientKhiTracuu(
                                    ClientConnection, "18072021")
                            elif(KiemTraDataSeGui == "19072021"):
                                GuiFileDataCacBankChoClientKhiTracuu(
                                    ClientConnection, "19072021")
                            elif(KiemTraDataSeGui == "Today"):
                                GuiFileDataNgayMoiChoClientHomNay(
                                    ClientConnection)
                            elif(KiemTraDataSeGui == "Thoat"):
                                break
                        continue
                    elif(CheckTracuu == 'Thoat'):
                        break
                    else:
                        break
            else:
                ClientConnection.send(
                    "Ban nhap sai tai khoan hoac mat khau".encode())
        elif choose == 2:
            username = ClientConnection.recv(1024).decode()
            password = ClientConnection.recv(1024).decode()
            if(Docfile(username, password) == 1):
                ClientConnection.send(
                    "Da co tai khoan trung voi thong tin ban nhap".encode())
            else:
                Register(username, password)
                ClientConnection.send("Dang ky thanh cong".encode())
    except:
        print('client left')


def DodaiChuoiso(chuoiso):
    temp = len(str(chuoiso))
    temptwo = str(temp)
    return temptwo


def createserver():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    soc.bind((HOST_ADDRESS, PORT))
    soc.listen(5)

    while True:
        try:
            ClientConnection, ClientAddress = soc.accept()
            print("Connect to Client: ", ClientAddress)
            content = "Server say hello Client"
            ClientConnection.send(content.encode())
            XulyNhuCauClient(ClientConnection)
            while True:
                Check = ClientConnection.recv(1024).decode()

                if(Check == "Y"):
                    XulyNhuCauClient(ClientConnection)
                elif(Check == "N"):
                    ClientConnection.close()
                    print('client left ')
        except Exception as e:
            print('client left ')


def get_exchange_rate(filenamejson):
    r = requests.get(
        'https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate')
    j = r.json()
    key = j['results']
    head = {'Authorization': 'Bearer ' + key}
    rr = requests.get(
        f"https://vapi.vnappmob.com/api/v2/exchange_rate/"+filenamejson, headers=head)
    exchange_rate = rr.json()
    exchange_rate = exchange_rate['results']

    # Serializing json
    json_object = json.dumps(exchange_rate, indent=4)

    # Writing to sbv.json
    with open(filenamejson+".json", "w") as outfile:
        outfile.write(json_object)


def SendFileExchangeToClient(SOCKET, filenamejson, datasize):
    file = open(filenamejson, 'rb')
    file_data = file.read(datasize)
    SOCKET.send(file_data)
    file.close()


def GetsizeData(filename):
    file_size = os.path.getsize(filename)
    return str(file_size)


def Docfile(username, password):
    try:
        file = open('UserPass.txt', 'r')
        for line in file:
            data = line.strip()
            if username+","+password == data:
                return 1
        return 0
    finally:
        file.close()


def worker(ClientConnection):

    XulyNhuCauClient(ClientConnection)

    while True:
        try:
            Check = ClientConnection.recv(1024).decode()

            if(Check == "Y"):
                XulyNhuCauClient(ClientConnection)
            elif(Check == "N"):
                ClientConnection.close()
                print('client left ')
        except Exception as e:
            break


def getExRate():
    get_exchange_rate("ctg")
    get_exchange_rate("vcb")
    get_exchange_rate("tcb")
    get_exchange_rate("bid")
    get_exchange_rate("stb")
    get_exchange_rate("sbv")


def updateEX():
    start = time.time()
    while True:
        # print(time.time() - start)
        if((time.time() - start) > 1800):
            getExRate()
            start = time.time()


def kill_clients(clients):
    for client in clients:
        client.close()


def run_app():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    soc.bind((HOST_ADDRESS, PORT))
    soc.listen()
    while True:

        try:
            ClientConnection, ClientAddress = soc.accept()
            print("Connect to Client: ", ClientAddress)
            content = "Server say hello Client"
            ClientConnection.send(content.encode())
            clients.append(ClientConnection)

            thread = threading.Thread(target=worker, args=(ClientConnection,))
            thread.start()

        except Exception as e:
            print('client left')


def MENU():
    root = tk.Tk()
    Canvas = tk.Canvas(root, height=400, width=400, bg='RoyalBlue4')
    Canvas.pack()
    korosai = tk.Button(root, text="CLOSE CONNECTIONS", font='Times 15',
                        bg="RoyalBlue4", fg="white", command=lambda: kill_clients(clients))
    korosai.pack()
    root.mainloop()


if(__name__ == "__main__"):

    getExRate()
    getInfo()
    choosePort()
    threadApp = threading.Thread(target=run_app)
    threadApp.start()
    threadTime = threading.Thread(target=updateEX)
    threadTime.start()
    threadMenu = threading.Thread(target=MENU)
    threadMenu.start()
