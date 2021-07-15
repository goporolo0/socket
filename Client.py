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
                receivefilefromclient(soc)
                HienManHinhExchangeRate()
            else:
                print("Dang nhap that bai")
            break
        elif choose==2:
            Register(soc)
            break   
        elif choose==0:
            break

def receivefilefromclient(SOCKET):
    file=open("sbv.json",'wb')
    file_data=SOCKET.recv(1024)
    file.write(file_data)
    file.close()

def HienManHinhExchangeRate():
    myjsonfile=open('sbv.json','r')
    
    jsondata=myjsonfile.read()
    
    obj=json.loads(jsondata)
    list=obj
    
    root=Tk()
    root.title('Exchange Rate')
    root.geometry("500x500")
    my_tree = ttk.Treeview(root)

    my_tree['columns'] = ("Currency","Sell")

    my_tree.column("#0",width=120,minwidth=25)
    my_tree.column("Currency",anchor=CENTER,width=120)
    my_tree.column("Sell",anchor=W,width=120)

    my_tree.heading("#0",text="Buy",anchor=W)
    my_tree.heading("Currency",text="Currency",anchor=CENTER)
    my_tree.heading("Sell",text="Sell",anchor=W)

    for i in range(len(list)):
        # for key in list[0].keys(): print (key)
       
        my_tree.insert(parent='',index='end',iid=i,text=list[i].get("buy"),values=(list[i].get("currency"),list[i].get("sell")))
    # for i in range(len(list)):
    #         for j in range(len(list[0])):
    #             my_tree.insert
                  
                # self.e = Entry(root, width=20, fg='blue',
                #                font=('Arial',16,'bold'))
                  
                # self.e.grid(row=i, column=j)
                # self.e.insert(END, lst[i][j])
          
    my_tree.pack(pady=20)

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


