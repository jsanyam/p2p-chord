import csv
import os
import pickle
import socket
import threading
import thread
import time
import mehar1
import wx
from threading import Thread
import file

# 0 is to update predecessor
# 1 is to find successor
# 2 is closest_preceding_finger
# 3 is update_finger_table
# 4 is update_finger_table_leave
# 5 is leave function
# 6 is update_finger0
# 7 is get_predecessor
# 8 is  get_successor

import node1

k = 7 # this is 160 for sha1
MAX = 2 ** k


def decr(value, size):
    if size <= value:
        return value - size
    else:
        return MAX - (size - value)


def between(value, init, end):  # equals  x in (a,b)
    if init == end:
        return True
    elif init > end:
        shift = MAX - init
        init = 0
        end = (end + shift) % MAX
        value = (value + shift) % MAX
    return init < value < end


def Ebetween(value, init, end):  # equals  x in [a,b)
    if value == init:
        return True
    else:
        return between(value, init, end)


def betweenE(value, init, end):  # equals  x in (a,b]
    if value == end:
        return True
    else:
        return between(value, init, end)


class Node:
    def __init__(self, host, port, id):
        self.id = id  # argv[1]
        self.finger = {}
        self.start = {}  # stores nodes in the series id + 2**i
        self.host = host
        self.port = port
        self.boot_host = ''
        self.boot_port = 1776
        for i in range(k):
            self.start[i] = (self.id + (2 ** i)) % (2 ** k)
        with open("esoteric"+str(self.id)+".csv","a") as f:
            print "written"
        f.close()

    # myMethod = mehar.main
    # save predecessor also

    def filed(self, name,filepath):
                idee = self.id
                with open("esoteric"+str(idee)+".csv","a") as f:
                    print "file opened"
                    f.write(name+","+"H\n")
                    print "written"
                    f.close()
                    c = mehar1.Client(self.id, self, self.port)
                    f1=c.calid(name)
                    #print f1
                    xxx = self.suitable("a", self.id, f1, self.id, name,self.port,self.host)
                    #print xxx
                    c.run(xxx,self,filepath)
    def filed1(self, name,filepath):
            idee = self.id
            c = mehar1.Client(self.id, self, self.port)
            f1=c.calid(name)
            #print f1
            xxx = self.suitable("a", self.id, f1, self.id, name,self.port,self.host)
            #print xxx
            c.run(xxx,self,filepath)

    def suitable(self, sort, idee1, f1, idee, name, port, host):
                #print "helllllllllloooooo"

                glee=sort+"+"+"r"+"+"+str(self.id)+"+"+str(self.port)+"+"+str(idee)+"+"+name+"+"+str(port)+"+"+str(f1)+"+"+str(self.host)+"+"+str(host)
                print glee
                if (self.finger[0]["id"]-idee1)<0:
                    if (f1>=0 and f1<=self.finger[0]["id"]) or (f1>idee1 and f1<128):
                        result=self.finger[0]["id"]
                        glee=sort+"+"+"r"+"+"+str(result)+"+"+str(self.finger[0]["port"])+"+"+str(idee)+"+"+name+"+"+str(port)+"+"+str(f1)+"+"+str(self.finger[0]["host"])+"+"+str(host)
                    else:
                        min_dist=-1
                        node=idee1
                        if f1>idee1:
                            relv=f1-idee1
                        else:
                            relv=f1+128-idee1
                        for i in range(k):
                            if self.finger[i]["id"]>idee1:
                                d=self.finger[i]["id"]-idee1
                            else:
                                d=self.finger[i]["id"]+128-idee1
                            if d<relv:
                                if d>min_dist:
                                    min_dist=d
                                    node=self.finger[i]["id"]
                                    node1=self.finger[i]["port"]
                                    node2=self.finger[i]["host"]
                                print "s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee1)                                                      # bug
                                glee=sort+"+"+"s"+"+"+str(node)+"+"+str(node1)+"+"+str(f1)+"+"+str(idee)+"+"+name+"+"+str(port)+"+"+str(node2)+"+"+str(host)
                elif f1>idee1 and f1<=self.finger[0]["id"]:
                    result=self.finger[0]["id"]
                    glee=sort+"+"+"r"+"+"+str(result)+"+"+str(self.finger[0]["port"])+"+"+str(idee)+"+"+name+"+"+str(port)+"+"+str(f1)+"+"+str(self.finger[0]["host"])+"+"+str(host)  # changed
                else:
                    min_dist=-1
                    node=idee1
                    if f1>idee1:
                        relv=f1-idee1
                    else:
                        relv=f1+128-idee1
                    for i in range(k):
                        if self.finger[i]["id"]>idee1:
                            d=self.finger[i]["id"]-idee1
                        else:
                            d=self.finger[i]["id"]+128-idee1
                        if d<relv:
                            if d>min_dist:
                                min_dist=d
                                node=self.finger[i]["id"]
                                node1=self.finger[i]["port"]
                                node2=self.finger[i]["host"]
                            print "s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee1)
                            glee=sort+"+"+"s"+"+"+str(node)+"+"+str(node1)+"+"+str(f1)+"+"+str(idee)+"+"+name+"+"+str(port)+"+"+str(node2)+"+"+str(host)
                print glee
                return glee
    def download(self,fileName,filepath):
        c=mehar1.Client(self.id, self,self.port)
        c.run3(fileName,self,filepath)

    def handleclient(self, s):

                    idee = self.id
                    num = s.recv(1024)
                    print num
                    #print "catch"
                    #print num
                    if num=="$1":
                        out = open("esoteric"+str(idee)+".csv","rb")
                        data = csv.reader(out)
                        #data=[row for row in data]
                        data1 = [row for row in data]
                        print data1
                        listn = []
                        count = 0
                        for x in range(len(data1)):
                            if data1[count][1] == "NH":
                                s.send(pickle.dumps(data1[count]))
                                temp = s.recv(1024)
                            count += 1
                        # sending = pickle.dumps(listn)
                        # sending_len = len(sending)
                        # chunk_size = sending_len / 1024
                        # iter = 0
                        # for i in range(chunk_size-1):
                        #     s.send(sending[(iter * 1024):((iter+1) * 1024)])
                        #     print "hello"
                        #     # time.sleep(1)
                        #     temp = s.recv(1024)
                        #     iter += 1
                        # s.send(sending[(iter * 1024):(sending_len - 1)])
                        # temp = s.recv(1024)
                        time.sleep(1)
                        s.send("terminate")
                        temp = s.recv(1024)

                        #
                        #    data = pickle.loads(c.recv(8192))
                        #     time.sleep(1)
                        #     c.send("okk")
                        #     if data == "terminate":
                        #         break
                        #
                        #
                        # s.send(pickle.dumps(listn))
                    elif num == "$$":
                        #s.send(fingert[0])
                        out = open("esoteric"+str(idee)+".csv","rb")
                        data = csv.reader(out)
                        #data=[row for row in data]
                        data1 = [row for row in data]
                        print data1
                        listp = []
                        count = 0
                        for x in range(len(data1)):
                            print data1[count][1]
                            if data1[count][1] == "H":
                                listp.append(data1[count][0])
                            count += 1
                        print listp
                        s.send(pickle.dumps(listp))
                        if s.recv(200) == str(idee):
                            s.send("end")
                        else:
                            s.send(str(self.finger[0]["port"])+"+"+str(self.finger[0]["host"]))
                    else:
                        num1=num.split("+")
                        print "num1"
                        print num1
                        index2=-1
                        if num1[1]=="r":
                            print idee
                            if num1[0]=="a":
                                outx = open("esoteric"+str(idee)+".csv","rb")
                                datax = csv.reader(outx)
                                print "file opened"
                                data5 = [row for row in datax]
                                countx=0
                                info=''
                                for x in range(len(data5)):
                                    if data5[countx][0]==num1[5] and data5[countx][1]=="NH":
                                        index2=countx
                                        ilen=len(data5[countx])-1
                                        info=data5[x][0]
                                        for y in range(ilen):
                                            info=info+","+data5[x][y+1]
                                    countx=countx+1
                                if index2!=-1:
                                    with open("esoteric"+str(idee)+".csv", 'rb') as inp, open("zoned"+str(idee)+".csv", 'wb') as out1:
                                        writer = csv.writer(out1)
                                        for row in csv.reader(inp):
                                            if row[0] != num1[5] or row[1]=="H":
                                                writer.writerow(row)
                                    inp.close()
                                    out1.close()
                                    outx.close()
                                    with open("zoned"+str(idee)+".csv","a") as f:
                                        f.write(info+","+num1[6]+","+num1[4]+","+num1[9]+"\n")
                                        print "written"
                                    f.close()
                                    os.remove("esoteric"+str(idee)+".csv")
                                    print "removed"
                                    os.rename("zoned"+str(idee)+".csv","esoteric"+str(idee)+".csv")
                                    print "renamed"
                     
                                    print "file opened"
                                    '''data5 = [row for row in data]
                                        for x in range(len(data5)):
                                            if data1[x][0]==num1[5]:
                                                index2=x
                                                ilen=len(data1[x])
                                                for y in range(ilen):
                                                    info=info+data1[x][y]+","
                                                f.write(info+","+","
                                        if index2==0:'''
                                    s.send("mission accomplished")
                                else:
                                    with open("esoteric"+str(idee)+".csv","a") as f:
                                        f.write(num1[5]+","+"NH"+","+num1[7]+","+num1[6]+","+num1[4]+","+num1[9]+"\n")
                                        print "written"
                                    f.close()
                                    s.send("mission accomplished")
                            if num1[0]=="l":
                                
                                print "let's search for your file"
                                out=open("esoteric"+str(idee)+".csv","rb")
                                data=csv.reader(out)
                                #data=[row for row in data]
                                data1=[row for row in data]
                                y1=len(data1)
                                index=-1
                                index2=-1
                                index3=-1
                                count=0
                                for x1 in range(y1):
                                    if data1[count][0]==num1[5] and data1[count][1]=="NH":
                                        print data1[count][0]
                                        print data1[count][1]
                                        index2=count
                                        break
                                    count=count+1
                                print "<!------------------->"
                                print index
                                if index2==-1:
                                    print "such a file doesn't exist"
                                    '''elif data1[index][1]=="H":
                                    print "you'll find the file here"
                                    s.send("ready to share the file")
                                    filename = num1[5]
                                    f=open(filename,"rb")
                                    while True:
                                        l = f.read(1024)
                                        while l:
                                            s.send(l)
                                            print("data is being sent")
                                            l = f.read(1024)
                                            useless = s.recv(6)
                                            print useless
                                        print l
                                        if not l:
                                            print "heya"
                                            time.sleep(2)
                                            s.send("empty")
                                            useless = s.recv(6)
                                            print useless
                                            f.close()
                                            break
                                    print("sending done")
                                    s.send(filename)'''
                                elif data1[index2][1]=="NH":
                                    s.send("reached")
                                    s.recv(20)
                                    fileName=data1[index2][0]
                                    s.send(fileName)
                                    s.recv(50)
                                    nof=(len(data1[index2])-3)/3
                                    print nof
                                    arr=[]
                                    county=0
                                    print "++++++++++++++++++++++++++++++++++++++"
                                    for x in range(nof):
                                        print data1[index2]
                                        print data1[index2][5]
                                        print data1[index2][3]
                                        arr.append({"host":data1[index2][3+2+(county*3)], "port":data1[index2][3+(county*3)]})
                                        #arr.append({"port":data1[index2][3+(county*3)})
                                        #arr[county]["port"]=data1[index2][3+(county*3)]
                                        county=county+1
                                    #x="l+r+"+num1[4]+"+"+data1[index][3]+"+"+num1[2]+"+"+num1[5]+"+"+num1[6]+"+"+num1[7]+"+"+data1[index][5]
                                    #s.send(x)
                                    s.send(pickle.dumps(arr))
                                    out.close()
                                else:
                                    print "abbbb"

                        if num1[1]=="s":
                            x=self.suitable(num1[0],int(num1[2]),int(num1[4]),int(num1[5]),num1[6],num1[7],num1[9])
                            s.send(x)
                    s.close()
    def upload(self,fileName):
        c2 = mehar1.Client(self.id, self,self.port)
        lo=c2.calid(fileName)
        if int(self.id)==int(self.finger[0]["id"]):
            with open("esoteric"+str(self.id)+".csv","a") as f:
                print "file opened"
                f.write(fileName+","+"H\n")
                f.write(fileName+","+"NH"+","+str(lo)+","+str(self.port)+","+str(self.id)+","+str(self.host)+"\n")
                print "written"
                f.close()
        else:
            self.filed(fileName,"abc")
    def run(self):
            #     HOST = ''
            #     PORT = 12
            #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #     s.bind((HOST,PORT))
            #     print 'server 12 started...'
            #     s.listen(5)
            #     i = 0
                def handleclient3(a):
                    #print "handleclient"
                    if int(self.id)!=int(self.finger[0]["id"]):
                        c1=mehar1.Client(self.id,self,self.port)
                        c1.update(self.finger[0]["port"],self.id,self.finger[0]["id"],self.finger[0]["host"])
                def handleclient2():
                    #print "funnnnnnnnccccction calllllllll"
                    while True:
                        input=raw_input("1.commit\n2.clone a repository\n3.checkout\n")
                        if input=="1":
                            path=raw_input("enter the path of the directory")
                            file.paths(path,self.port,self)
                        if input=="2":
                            version=raw_input("Enter the version you want to download")
                            file.checkout(self.port,self,version)
                        if input=="3":
                            file.checkout(self.port,self)
                        #if input=="2":
                        #x = raw_input("1.look for a file\n2.just share\n")
                    #if x == "2":
                        #z = raw_input("enter the name of the file you want to share")
                        #self.filed(z)
                    #if x == "1":
                        #c = mehar.Client(self.id, self,self.port)
                        #c.run1(a)
                handleclient3(self.finger[0]["port"])
                handleclient2()
                # handleclient2(self.finger[0]["port"])
                # while True:
                #     conn, addr = s.accept()
                #     #i += 1
                #     print 'connected to ', addr
                #     thread.start_new_thread(handleclient, (conn,))

    def find_size(self, file_name):
        with open(str("gitstore/"+file_name), 'rb') as f:
            var = f.read()#.replace('\n', '')
            f.close()
            return len(var)

    def start_download(self, c, file_name, start, end):
        with open("gitstore/"+str(file_name), 'rb') as f:
            var = f.read()#.replace('\n', '')
            f.close()
            #var = pickle.load(f)
            print "file"
            #print var
            print start
            print end
            # print var[start: end + 1]
            return var[start: end + 1]
            #return c.recv(1024)


    def handlerFunction(self, c, addr):
        print "i am here"
        data = c.recv(1024)
        # print "reached"
        if data == 'file handling':
            c.send("ok")
            thread.start_new_thread(self.handleclient, (c,))
            #self.handleclient(c)

        else:
            received = pickle.loads(data)
            choice = received[1]
            if choice == 0:
                response = n.update_predecessor(received[0])
                c.send(response)
            elif choice == 1:
                response = n.find_successor(received[0])
                c.send(pickle.dumps(response))
            elif choice == 2:
                response = n.closest_preceding_finger(received[0])
                c.send(pickle.dumps(response))
            elif choice == 3:
                # response = \
                n.update_finger_table(received[0], received[2])
                # c.send(response)
            elif choice == 4:
                n.update_finger_table_leave(received[0], received[2], received[3])

            elif choice == 5:
                n.leave(received[0])

            elif choice == 6:
                response = n.update_finger0(received[0])
                c.send(response)

            elif choice == 7:
                response = n.get_predecessor()
                c.send(pickle.dumps(response))

            elif choice == 8:
                response = n.successor()
                c.send(pickle.dumps(response))

            elif choice == 9:
                response = n.find_size(received[2])
                c.send(str(response))
            elif choice == 10:
                response = "I am online"
                c.send(response)
            elif choice == 11:
                response = n.start_download(c, received[0], received[2], received[3])
                str_size = len(response)
                chunk = str_size / 1024
                iter = 0
                chunk = int(chunk)
                print str(str_size) + "chunk" + str(chunk)
                for i in range(chunk - 1):
                    # print i
                    c.send(response[i * 1024: (i+1) * 1024])
                    print response[i * 1024: (i+1) * 1024]
                    data = c.recv(1024)
                    iter += 1
                print iter
                c.send(response[iter * 1024:str_size])
                data = c.recv(1024)
                time.sleep(1)
                c.send("empty")
                data = c.recv(1024)
                #c.send(response)


            #print "Hello"
            # showFinger(n)
            c.close()


    def serve(self, n): # kuch gadbad hai
        # global server
        server = socket.socket()  # Create a socket object
        # print "hello"
        # print "***********************************************"
        # print (n.host,n.port)
        server.bind((n.host, n.port))  # Bind to the port
        server.listen(120)  # Now wait for client connection.
        while True:
            # showFinger(n)
            c, addr = server.accept()  # Establish connection with client.
            # print 'Got connection from', addr
            h, p = c.getpeername()
            # print str(h) + ":" + str(p)
            th = Thread(target =self.handlerFunction, args=(c, addr))
            th.start()

    def update_finger0(self, data):
        self.finger[0] = data
        return "finger0_ok"

    def get_successor_socket(self, n1):
        client = socket.socket()
        client.connect((n1["host"], n1["port"]))
        message = ["get_successor", 8]
        client.send(pickle.dumps(message))
        successor = pickle.loads(client.recv(1024))
        client.close()
        return successor

    def successor(self):
        return self.finger[0]

    def update_predecessor(self, predecessor):
        self.predecessor = predecessor
        return "up_prede_ok"

    def get_predecessor(self):
        return self.predecessor

    def closest_preceding_finger(self, id):
        #print "no"
        for i in range(k - 1, -1, -1):
            #print self.finger[i]["id"]
            #print id
            if between(self.finger[i]["id"], self.id, id):
                #print "yes"
                #print self.finger[i]["id"]
                #print self.id
                return self.finger[i]
        node = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(),
                #"predecessor": self.predecessor}
        return node

    def find_predecessor(self, id):
        if id == self.id:
            return self.predecessor
        n1 = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(), "predecessor": self.predecessor}
        # assuming a possible structure like (start,id,ip,port) n1.successor().id will be available to us locally
        #print "ohoo"
        #print self.predecessor["id"]
        #print n1["successor"]["id"]
        if self.id == n1["id"]:
            n1_successor = self.successor()
        else:
            n1_successor = self.get_successor_socket(n1)
        while not betweenE(id, n1["id"], n1_successor["id"]):#n1["successor"]["id"]):
            #print "wohoo"
            # print n1["successor"]["id"]
            #print "id"
            #print n1_successor["id"]
            if n1["id"] == self.id:
                n1 = self.closest_preceding_finger(id)  # sockets needed
            else:
                client = socket.socket()
                client.connect((n1["host"], n1["port"]))
                message = [id, 2]
                client.send(pickle.dumps(message))
                n1 = pickle.loads(client.recv(1024))
                client.close()
            if self.id == n1["id"]:
                n1_successor = self.successor()
            else:
                n1_successor = self.get_successor_socket(n1)
        #print n1["successor"]
        #print n1["successor"]["successor"]["id"]
        #print n1["successor"]["id"]
        #print n1["id"]
        return n1

    def find_successor(self, id):
        #print "fs"
        #print self.predecessor["id"]
        #print id
        #print self.id
        if betweenE(id, self.predecessor["id"], self.id):
            #print "123"
            node = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(),
                    # "predecessor": self.predecessor}
            return node
        n = self.find_predecessor(id)
        # ask n to find successor on self behalf and return it recursively to self.
        # n would be a different node in a network so ofc you need sockets
        #print "break"
        if self.id == n["id"]:
            return self.successor()
        return self.get_successor_socket(n) # n["successor"]

    def join(self, n1):
        if self.id == n1["id"]:
            for i in range(k):
                self.finger[i] = n1
            self.predecessor = n1
        else:
            self.init_finger_table(n1) #use locks and threads here
            self.update_others()
            # move keys from successor of self to self,whose successor is self.

    def init_finger_table(self, n1):
        # request n1 to get successor of self ,obviously socket are used as, different nodes
        # self.finger[0] = n1.find_successor(self.start[0]) #socket needed
        client = socket.socket()
        # print n1["host"]
        # print n1["port"]
        client.connect((n1["host"], n1["port"]))
        #node = {"id": self.start[0], "host": 0, "port": 0, "successor": 0, "predecessor": 0}
        id = self.start[0]
        message = [id, 1] #find_successor
        client.send(pickle.dumps(message))
        self.finger[0] = pickle.loads(client.recv(1024))
        client.close()
        # print "first"
        # print self.successor()
        # self.predecessor = self.successor()["predecessor"]  # socket needed may be  # can create problems
        client = socket.socket()
        client.connect((self.successor()["host"], self.successor()["port"]))
        # node = {"id": self.start[0], "host": 0, "port": 0, "successor": 0, "predecessor": 0}
        message = ["get_predecessor", 7] #find_successor
        client.send(pickle.dumps(message))
        self.predecessor = pickle.loads(client.recv(1024))
        client.close()
        # print "second"
        # self.successor().predecessor = self #socket needed
        client = socket.socket()
        client.connect((self.successor()["host"], self.successor()["port"]))
        node = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(),
                #"predecessor": self.predecessor}
        message = [node, 0]
        client.send(pickle.dumps(message))
        # s.send((self, 0)) # send request to successor server to update its predecessor
        response = client.recv(1024)  # what to do if response negative
        # print response
        # print self.successor()
        client.close()
        # print "third"
        # self.predecessor.finger[0] = self # socket needed why?
        client = socket.socket()
        client.connect((self.predecessor["host"], self.predecessor["port"]))
        node = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(),
                #"predecessor": self.predecessor}
        message = [node, 6]
        client.send(pickle.dumps(message))
        # s.send((self, 0))     # send request to successor server to update its predecessor
        response = client.recv(1024)  # what to do if response negative
        print response
        client.close()
        #print "fourth"
        for i in range(k - 1):
            if Ebetween(self.start[i+1], self.id, self.finger[i]["id"]):
                self.finger[i+1] = self.finger[i]
                #print "fifthi"
            else:
                # self.finger[i+1] = n1.find_successor(self.start[i+1]) # socket needed
                client = socket.socket()
                client.connect((n1["host"], n1["port"]))
                #node = {"id": self.start[i+1], "host": 0, "port": 0, "successor": 0, "predecessor": 0}
                id = self.start[i+1]
                message = [id, 1]
                client.send(pickle.dumps(message))
                self.finger[i + 1] = pickle.loads(client.recv(1024))
                client.close()
                #print "fifthii"
                # s.send(self.start[i+1], 1) # send request to n1 server
                # sel f.finger[i+1] = s.recv(1024)

    def update_others(self):
        #print self.successor()
        #print self.predecessor
        for i in range(k):
            prev = decr(self.id, 2 ** i)
            #print "prev"
            #print prev
            # showFinger(self)
            p = self.find_predecessor(prev)
            #print "p"
            #print p["id"]
            if self.id == p["id"]:
                p_successor = self.successor()
            else:
                p_successor = self.get_successor_socket(p)
            if prev == p_successor["id"]: # p["successor"]["id"]:  # find successor # if prev is a node itself
                p = p_successor
                # p.update_finger_table(self,i) # socket needed
            client = socket.socket()
            #print "uo"
            #print p["id"]
            #print p["port"]
            client.connect((p["host"], p["port"]))
            node = {"id": self.id, "host": self.host, "port": self.port}#, "successor": self.successor(),
                        #"predecessor": self.predecessor}
            message = [node, 3, i]
            client.send(pickle.dumps(message))
            #print "after connection"
            # s.send((self, i, 3))	# send request to server of next node by client of node
            #returned_value = client.recv(1024)
            #print returned_value

    def update_finger_table(self, s, i):
        #breaking_return = "up_fing_ok"
        #print "test"
        #print s["id"]
        #print i
        #print showFinger(self)
        if Ebetween(s["id"], self.id, self.finger[i]["id"]) and self.id != s["id"]:

            self.finger[i] = s
            p = self.predecessor
            # p.update_finger_table(s, i)  # socket needed
            client = socket.socket()
            #print "uft"
            #print p["id"]
            #print p["port"]
            client.connect((p["host"], p["port"]))
            message = [s, 3, i]
            client.send(pickle.dumps(message))
            #print "send problem"
            # s.send((s, i, 3))     # send request to server of next node by client of node
            #returned_value = client.recv(1024)
            #return returned_value
        # c.send(breaking_return)    # returned value by server of node
        #return breaking_return

    def exit(self):
        #print "exiting"
        # print self.successor().id
        #print self.id
        # self.successor().leave(self.id)
        client = socket.socket()
        client.connect((self.successor()["host"], self.successor()["port"]))
        id = self.id
        message = [id, 5]
        client.send(pickle.dumps(message))

    def leave(self, id):
        for i in range(k):
            prev = decr(id, 2**i)
            p = self.find_predecessor(prev)
            #print "p"
            # print p.id
            if self.id == p["id"]:
                p_successor = self.successor()
            else:
                p_successor = self.get_successor_socket(p)
            if prev == p_successor["id"]:
                p = p_successor
            #if prev == p.successor().id: #if prev is a node itself #socket needed
            #      p = p.successor()
            #print p.id
            # p.update_finger_table_leave(id, self, i) #socket needed
            client = socket.socket()
            client.connect((p["host"], p["port"]))
            node = {"id": self.id, "host": self.host, "port": self.port}
            message = [id, 4, node, i]
            client.send(pickle.dumps(message))

    def update_finger_table_leave(self, left_id, update_node, index):
        # print left_id, index
        # print self.finger[index].id
        if self.finger[index]["id"] == left_id and self.id != left_id:
            self.finger[index] = update_node
            #print "new finger"
            # print self.finger[index].id
            p = self.predecessor
            client = socket.socket()
            client.connect((p["host"], p["port"]))
            message = [left_id, 4, update_node, index]
            client.send(pickle.dumps(message))
            #p.update_finger_table_leave(left_id, update_node, index)

# (ip_address, port, id, successor, predecessor)


def showFinger(node):
    print 'Finger table of node ' + str(node.id)
    print 'start:node'
    for i in range(k):
        print str(node.start[i]) + ' : ' + str(node.finger[i]["id"])
    print '-----------'
    

class windowClass(wx.Frame):
    def __init__(self,*args,**kwargs):
        print "bskjhkqehblhblt"
        super(windowClass,self).__init__(*args,**kwargs)

        #self.basicGUI()

    def basicGUI(self,S):
        '''print "dakbhklgligb"
        panel=wx.Panel(self)
        menuBar=wx.MenuBar()
        fileButton=wx.Menu()
        editButton=wx.Menu()
        exitItem=fileButton.Append(wx.ID_EXIT,'Exit','status msg...')
        #exitItem.SetBitmap(wx.Bitmap("gfvgfj.png"))
        fileButton.AppendItem(exitItem)

        menuBar.Append(fileButton,'File')
        menuBar.Append(editButton,'Edit')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU,self.Quit,exitItem)'''
        while True:
            chooseOneBox=wx.SingleChoiceDialog(None,'Please select one option from below',
                                               'choice',['add a new file','download a file'])
            option=[]
            if chooseOneBox.ShowModal()==wx.ID_OK:
                option=chooseOneBox.GetStringSelection()
            if chooseOneBox.ShowModal()==wx.ID_CANCEL:
                break

            if option=="add a new file":
                nameBox=wx.TextEntryDialog(None,'Please enter the name of file you wish to add','welcome')
                if nameBox.ShowModal()==wx.ID_OK:
                    fileName=nameBox.GetValue()
                    '''s=socket.socket()
                    host='192.168.43.148'
                    port=1776
                    s.connect((host,port))
                    s.send('161')
                    if s.recv(100)=="ok":
                        s.send(fileName)
                    s.close()'''
                    #fileName=nameBox.GetValue()
                    #S=Node(a,b,c)
                    c2 = mehar1.Client(S.id, S,S.port)
                    lo=c2.calid(fileName)
                    if int(S.id)==int(S.finger[0]["id"]):
                        with open("esoteric"+str(S.id)+".csv","a") as f:
                            print "file opened"
                            f.write(fileName+","+"H\n")
                            f.write(fileName+","+"NH"+","+str(S.id)+","+str(S.port)+","+str(lo)+","+str(S.host)+"\n")
                            print "written"
                        f.close()
                    else:
                        S.filed(fileName)
            if option=="download a file":
                #nameBox1=wx.TextEntryDialog(None,'Please enter the name of file you wish to download','welcome')
                #if nameBox1.ShowModal()==wx.ID_OK:
                    #fileName1=nameBox1.GetValue()
                '''s=socket.socket()
                host='192.168.43.148'
                port=1776
                s.connect((host,port))
                s.send('162')
                fs = s.recv(1024)
                listp=fs.split("_")'''
                '''j = 0
                for i in listn:
                    listp[j] = i['filename']
                    j = j
                print listp'''    
                #s.close()
                '''app=wx.App()
                w=mehar1.windowClass2(None)
                w.basicGUI(listp,self,S)
                #w.basicGUI(listp,self,S)
                app.MainLoop()'''

                #c.run1(S.finger[0]["port"],S.finger[0]["host"])

            #wx.TextCtrl(panel,pos=(3,10),size=(150,50))
            #aweText=wx.StaticText(panel, -1, "Awesome Text" , (3,3))
            #aweText.setForegroundColor('#67cddc')
            #aweText.setForegroundColor('black')
        

        #self.SetTitle('Epic Window')

        #self.Show(True)

    def Quit(self,e):
        self.Close()

if __name__ == "__main__":
    # ri = raw_input("Choice")
    #
    # if ri == "1":
    #     n = Node(socket.gethostname(), 8009, 8)  # , argv[1], argv[2])
    #     node = {"id": n.id, "host": n.host, "port": n.port}  # , "successor": 0, "predecessor": 0}
    #     # node["successor"] = node
    #     # node["predecessor"] = node
    #     host = n.host  # '0.0.0.0' ## Get local machine name
    #     port = n.port  # Reserve a port for your service.
    #     print host
    #     server = socket.socket()  # Create a socket object
    #     server.bind((host, port))  # Bind to the port
    #     server.listen(10)  # Now wait for client connection.
    #     t = threading.Thread(target=n.serve, args=())
    #     #t.daemon = True
    #     t.start()
    #     n.join(node)
    #     showFinger(n)
    #
    # elif ri == "0":
    #     n = Node(socket.gethostname(), 8010, 1)  # , argv[1], argv[2])
    #     node = {"id": 8, "host": socket.gethostname(), "port": 8009} # , "successor": 0, "predecessor": 0}
    #     # node["successor"] = node
    #     # node["predecessor"] = node
    #     host = n.host  # '0.0.0.0' ## Get local machine name
    #     port = n.port  # Reserve a port for your service.
    #     print host
    #     server = socket.socket()  # Create a socket object
    #     server.bind((host, port))  # Bind to the port
    #     server.listen(10)  # Now wait for client connection.
    #     t = threading.Thread(target=n.serve, args=())
    #     #t.daemon = True
    #     t.start()
    #     n.join(node)
    #     #print "after join"
    #     showFinger(n)
    #
    # else:
    #     n = Node(socket.gethostname(), 8011, 98)  # , argv[1], argv[2])
    #     node = {"id": 8, "host": socket.gethostname(), "port": 8009} # , "successor": 0, "predecessor": 0}
    #     # node["successor"] = node
    #     # node["predecessor"] = node
    #     host = n.host  # '0.0.0.0' ## Get local machine name
    #     port = n.port  # Reserve a port for your service.
    #     print host
    #     server = socket.socket()  # Create a socket object
    #     server.bind((host, port))  # Bind to the port
    #     server.listen(10)  # Now wait for client connection.
    #     t = threading.Thread(target=n.serve, args=())
    #     #t.daemon = True
    #     t.start()
    #     n.join(node)
    #     #print "after join"
    #     showFinger(n)
    result = node1.main()
    n = Node(result[1]["host"], result[1]["port"], result[1]["id"])
    t = threading.Thread(target=n.serve, args=(n,))  #call it via function
    t.start()
    #n.serve(n)
    n.join(result[0])
    showFinger(n)
    print "Exiting"
    exit_status = raw_input("Want to exit")
    if exit_status == 'Yes':
                '''PORT = self.successor()["port"]
                #print PORT
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = self.successor()["host"]
                try:
                        c.connect((host, PORT))
                except socket.gaierror:
                        print "sorry but you were unable to connect"
                #c.connect((host,PORT))
                c.send("file handling")
                print c.recv(1024)
                c.send("$1")
                data = pickle.loads(c.recv(1024))
                count = 0
                with open("esoteric"+self.id+".csv","a") as f:
                        print "file opened"
                        count=0
                        for x in range(len(data)):
                                if data[count][1]=="NH":
                                        f.write(data[count][0]+","+data[count][1]+","+data[count][2]+","+data[count][3]+","+data[count][4]+","+data[count][5]+"\n")
                                        print "written"
                                count=count+1
                        f.close()
                c.close()'''
                n.exit()
    else:
        showFinger(n)
        n.run()
        # print"finisheddddd"
        # s.run()

# 0 is to update predecessor
# 1 is to find successor
# 2 is closest_preceding_finger
# 3 is update_finger_table
# 4 is return value
# 5 is join function
# 6 is update_finger0
# 7 is get_predecessor
# 8 is  get_successor