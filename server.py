import socket
import requests
import json

HOST, PORT = '127.0.0.1', 8080


def create_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.bind((host, port))
    print('Socket is listening..')
    s.listen(5)
    return s


def MoveHomePage(Server, Client, Request):
    if "GET /index.html HTTP/1.1" in Request:
        SendFileIndex(Client)
        # Server.close()
        return True


def SendFileIndex(Client):
    f = open("index.html", "rb")
    L = f.read()
    header = f"""HTTP/1.1 200 OK
Content-Length: {len(L)}

"""
    print("-----------------HTTP respone  Index.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def send_main_page(Client):
    f = open("main.html", "rb")
    L = f.read()
    header = f"""HTTP/1.1 301 Moved Permanently
Content-Length: {len(L)}

"""
    print("-----------------HTTP respone  main.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def CheckPass(Request):
    if "POST / HTTP/1.1" not in Request:
        return False
    if "Username=admin&Password=admin" in Request:
        return True
    else:
        return False
def get_exchange_rate():
    r = requests.get(
        'https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate')
    j = r.json()
    key = j['results']
    head = {'Authorization': 'Bearer ' + key}

    rs = [None] * 7
    temps = [None] * 7
    rs[6] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/sbv",
                         headers=head)
    rs[1] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/vcb",
                         headers=head)
    rs[2] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/ctg",
                         headers=head)
    rs[3] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/tcb",
                         headers=head)
    rs[4] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/bid",
                         headers=head)
    rs[5] = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/stb",
                         headers=head)
    for i in range(1, 7):
        temps[i] = rs[i].json()
        temps[i] = temps[i]['results']
        # Serializing json
        json_object = json.dumps(temps[i], indent=4)

        # Writing to sample.json

        with open(f"./data/temp{i}.json", "w") as outfile:
            outfile.write(json_object)





if __name__ == "__main__":

    while True:
        try:
            s = create_server(HOST, PORT)
            connection, address = s.accept()
            request = connection.recv(1024).decode('utf-8')
            # print(request)



            MoveHomePage(s, connection, request)
            if (CheckPass(request)):
                print("welcome")
                send_main_page(connection)
            else:
                print('sai pass')
            s.close()

        except:
            print("cant connect")
            break
