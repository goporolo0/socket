import socket
import json
import requests
import threading


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
        print(e)
    finally:
        file.close()


def XulyNhuCauClient(ClientConnection):
    temp = ClientConnection.recv(1024).decode()
    choose = int(temp)
    if choose == 1:
        username = ClientConnection.recv(1024).decode()
        password = ClientConnection.recv(1024).decode()
        if(Docfile(username, password) == 1):
            ClientConnection.send("Dang nhap thanh cong".encode("utf-8"))
            # thread = threading.Thread(target=SendFileExchangeToClient, args=(ClientConnection,))
            # thread.start()
            SendFileExchangeToClient(ClientConnection)  # gửi 1 đống text
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
            print(e)


def get_exchange_rate():
    r = requests.get(
        'https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate')
    j = r.json()
    key = j['results']
    head = {'Authorization': 'Bearer ' + key}
    rr = requests.get(
        f"https://vapi.vnappmob.com/api/v2/exchange_rate/sbv", headers=head)
    exchange_rate = rr.json()
    exchange_rate = exchange_rate['results']

    # Serializing json
    json_object = json.dumps(exchange_rate, indent=4)

    # Writing to sbv.json
    with open("sbv.json", "w") as outfile:
        outfile.write(json_object)


def SendFileExchangeToClient(SOCKET):
    file = open('sbv.json', 'rb')
    file_data = file.read(1024)
    SOCKET.send(file_data)
    print("Data has been transmitted successfully")
    file.close()


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


if(__name__ == "__main__"):
    get_exchange_rate()
    getInfo()
    choosePort()
    createserver()
