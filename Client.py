#from functools import singledispatch
import socket
from tkinter import*
import os
import json
from tkinter import ttk
def Sigin(SOCKET):
    root= Tk()
    root.geometry("400x300")
    root.title("Sign-In Client window")

    l3=Label(root,text="Login form",font=("Arial",35))
    l1= Label(root, text="Username")
    e1=Entry(root)
    e2=Entry(root)
    l2= Label(root, text="Password")
    l4=Label(root,text="")

    def clicked():
        username=e1.get()
        password=e2.get()
        SOCKET.send(username.encode("utf-8"))
        SOCKET.send(password.encode("utf-8"))
        global data
        data=SOCKET.recv(1024).decode("utf-8")
        root.destroy()

    bt=Button(root,text="Dang nhap",bg="blue",fg="white",command=clicked)
    bt1=Button(root,text="Thoat",bg="blue",fg="white",command=root.destroy)

    l3.grid(row=0,column=1)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)

    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    bt.grid(row=3,column=1)

    bt1.grid(row=5,column=1)
    l4.grid(row=4,column=1)
    root.mainloop()

def Register(SOCKET):
    root= Tk()
    root.geometry("400x300")
    root.title("Register Client window ")

    l1= Label(root, text="Username")
    e1=Entry(root)
    e2=Entry(root)
    l2= Label(root, text="Password")
    l3=Label(root,text="Register form",font=("Arial",35))

    def clicked():
        username=e1.get()
        password=e2.get()
        #l3.configure(text="Dang ky thanh cong")
        SOCKET.send(username.encode("utf-8"))
        SOCKET.send(password.encode("utf-8"))
        check=SOCKET.recv(1024).decode("utf-8")
        if check=="Da co tai khoan trung voi thong tin ban nhap":
            root.destroy()
            print("Da co tai khoan trung voi thong tin ban nhap")
        elif check=="Dang ky thanh cong":
            root.destroy()
            print("Dang ky thanh cong")

    bt=Button(root,text="Dang ky",bg="blue",fg="white",command=clicked)
    bt1=Button(root,text="Thoat",bg="blue",fg="white",command=root.destroy)

    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)

    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)

    bt.grid(row=3,column=1)
    bt1.grid(row=5,column=1)

    l3.grid(row=0,column=1)
    root.mainloop()
   
def chooseServer():
    global SERVER_ADDRESS
    SERVER_ADDRESS=input("Please choose server address ")
    global PORT
    PORT=int(input("Please choose port "))

def Menu(soc):
    while True:
        print("Menu:")
        print("0. Exit")
        print("1. Sign up")
        print("2. Register")
        choose=int((input("Nhap lua chon cua ban:")))
        soc.send(str(choose).encode())
        if choose==1:   
            Sigin(soc)  
            if(data=="Dang nhap thanh cong"):
                datavcb=int(soc.recv(4).decode())
                datactg=int(soc.recv(4).decode())
                datatcb=int(soc.recv(4).decode())
                databid=int(soc.recv(4).decode())
                datastb=int(soc.recv(4).decode())
                datasbv=int(soc.recv(3).decode())
                receivefilefromclient(soc,"vcb.json",datavcb)
                receivefilefromclient(soc,"ctg.json",datactg)
                receivefilefromclient(soc,"tcb.json",datatcb)
                receivefilefromclient(soc,"bid.json",databid)
                receivefilefromclient(soc,"stb.json",datastb)
                receivefilefromclient(soc,"sbv.json",datasbv)
                ManhinhChinh()
            else:
                print("Dang nhap that bai")
            break
        elif choose==2:
            Register(soc)
            break   
        elif choose==0:
            break

def receivefilefromclient(SOCKET,filenamejson,datasize):
    file=open(filenamejson,'wb')
    file_data=SOCKET.recv(datasize)
    file.write(file_data)
    file.close()

def HienManHinhExchangeRate(filenamejson):
    myjsonfile=open(filenamejson,'r')
    
    jsondata=myjsonfile.read()
    
    obj=json.loads(jsondata)
    list=obj
    listtemp=[]
    index=0
    for key in list[0].keys():
        listtemp.insert(index,key)
        index=index+1
    root=Tk()
    root.title('Exchange Rate')
    root.geometry("500x500")
    my_tree = ttk.Treeview(root)
 
    my_tree['columns'] = (listtemp[1:len(listtemp)])
    my_tree.column("#0",width=120,minwidth=25)
    my_tree.column(listtemp[1],anchor=CENTER,width=120)

    for i in range(2,len(listtemp)):
        my_tree.column(listtemp[i],anchor=W,width=120)

    my_tree.heading("#0",text=listtemp[0],anchor=W)
    my_tree.heading(listtemp[1],text=listtemp[1],anchor=CENTER)
    for i in range(2,len(listtemp)):
        my_tree.heading(listtemp[i],text=listtemp[i],anchor=W)
    
    for i in range(len(list)):  
        if(len(listtemp)==3):
            my_tree.insert(parent='',index='end',iid=i,text=list[i].get(listtemp[0]),values=(list[i].get(listtemp[1]),list[i].get(listtemp[2])))
        elif(len(listtemp)==4):
            my_tree.insert(parent='',index='end',iid=i,text=list[i].get(listtemp[0]),values=(list[i].get(listtemp[1]),list[i].get(listtemp[2]),list[i].get(listtemp[3]))) 
    my_tree.pack(pady=20)

    root.mainloop()
def ManhinhChinh():
    root = Tk()

    def bankCTG():
        HienManHinhExchangeRate("ctg.json")
    def bankVCB():
        HienManHinhExchangeRate("vcb.json")
    def bankTCB():
        HienManHinhExchangeRate("tcb.json")
    def bankBIDV():
        HienManHinhExchangeRate("bid.json")
    def bankSTB():
        HienManHinhExchangeRate("stb.json")
    def bankSBV():
        HienManHinhExchangeRate("sbv.json")    
    root.geometry("500x500")
    l1=Label(root,text="EXCHANGE RATE OF 6 BANKS",fg="black",bg="LightYellow2",font=("Arial",20))
    btVCB=Button(root,text="Bank Vietcombank (VCB)",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankVCB)
    btCTG=Button(root,text="Bank Vietinbank (CTG)",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankCTG)
    btTCB=Button(root,text="Bank Techcombank (TCB)",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankTCB)
    btBIDV=Button(root,text="Bank BIDV",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankBIDV)
    btSTB=Button(root,text="Bank Sacombank (STB)",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankSTB)
    btSBV=Button(root,text="Bank SBV",font=("Arial",15),bg="RoyalBlue4",fg="white",width=23,command=bankSBV)
    btExit=Button(root,text="Dang Xuat",font=("Arial",10),bg="RoyalBlue4",fg="white",width=10,command=root.destroy)
    l2=Label(root,text="")
    l1.grid(row=0,column=1)
    btVCB.grid(row=1,column=1)
    btCTG.grid(row=2,column=1)
    btTCB.grid(row=3,column=1)
    btBIDV.grid(row=4,column=1)
    btSTB.grid(row=5,column=1)
    btSBV.grid(row=6,column=1)
    l2.grid(row=7,column=1)
    btExit.grid(row=10,column=1)
    root.mainloop()
def createClient():
    soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    soc.connect((SERVER_ADDRESS,PORT))
    IsConnect=soc.recv(1024).decode()
    print(IsConnect)
    Menu(soc)
    while True:
        Tieptuc=input(("Do you wanna continute ? Y/N "))
        soc.send(Tieptuc.encode())
        if(Tieptuc=="Y"):
            os.system("cls")
            Menu(soc)
        elif(Tieptuc=="N"):
            break
    soc.close()

if(__name__=="__main__"):
    chooseServer()
    createClient()


