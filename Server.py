import socket
import json
from tkinter.constants import SE
import requests
import threading
import os

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


def XulyNhuCauClient(ClientConnection):
    try:
        temp = ClientConnection.recv(1024).decode()
        choose = int(temp)
        if choose == 1:
            username = ClientConnection.recv(1024).decode()
            password = ClientConnection.recv(1024).decode()
            if(Docfile(username, password) == 1):
                ClientConnection.send("Dang nhap thanh cong".encode("utf-8"))

                datavcb=GetsizeData("vcb.json")
                lenvcb=DodaiChuoiso(datavcb)
                ClientConnection.send(lenvcb.encode())
                ClientConnection.send(datavcb.encode())

                datactg=GetsizeData("ctg.json")
                lenctg=DodaiChuoiso(datactg)
                ClientConnection.send(lenctg.encode())
                ClientConnection.send(datactg.encode())

                datatcb=GetsizeData("tcb.json")
                lentcb=DodaiChuoiso(datatcb)
                ClientConnection.send(lentcb.encode())
                ClientConnection.send(datatcb.encode())
                
                databid=GetsizeData("bid.json")
                lenbid=DodaiChuoiso(databid)
                ClientConnection.send(lenbid.encode())
                ClientConnection.send(databid.encode())
                
                datastb=GetsizeData("stb.json")
                lenstb=DodaiChuoiso(datastb)
                ClientConnection.send(lenstb.encode())
                ClientConnection.send(datastb.encode())

                datasbv=GetsizeData("sbv.json")
                lensbv=DodaiChuoiso(datasbv)
                ClientConnection.send(lensbv.encode())
                ClientConnection.send(datasbv.encode())

                SendFileExchangeToClient(ClientConnection,"vcb.json",int(datavcb))
                SendFileExchangeToClient(ClientConnection,"ctg.json",int(datactg))
                SendFileExchangeToClient(ClientConnection,"tcb.json",int(datatcb))
                SendFileExchangeToClient(ClientConnection,"bid.json",int(databid))
                SendFileExchangeToClient(ClientConnection,"stb.json",int(datastb))
                SendFileExchangeToClient(ClientConnection,"sbv.json",int(datasbv))  
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
    temp=len(str(chuoiso))
    temptwo=str(temp)
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


def SendFileExchangeToClient(SOCKET,filenamejson,datasize):
    file = open(filenamejson, 'rb')
    file_data = file.read(datasize)
    SOCKET.send(file_data)
    print("Data has been transmitted successfully")
    file.close()

def GetsizeData(filename):
    file_size=os.path.getsize(filename)
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

if(__name__ == "__main__"):
    get_exchange_rate("ctg")
    get_exchange_rate("vcb")
    get_exchange_rate("tcb")
    get_exchange_rate("bid")
    get_exchange_rate("stb")
    get_exchange_rate("sbv")
    getInfo()
    choosePort()
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    soc.bind((HOST_ADDRESS, PORT))
    soc.listen()
    while True:
        try:
            ClientConnection, ClientAddress = soc.accept()
            print("Connect to Client: ", ClientAddress)
            content = "Server say hello Client"
            ClientConnection.send(content.encode())

            thread = threading.Thread(target=worker, args=(ClientConnection,))
            thread.start()
        except Exception as e:
            print('client left')
