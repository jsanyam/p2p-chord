import socket,pickle,csv
import thread,threading
import select
import time
import hashlib
def main():
    class Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
            def filed(self,name):
                with open("esoteric"+str(idee)+".csv","a") as f:
                    print "file opened"
                    f.write(name+","+"H\n")
                    print "written"
                    f.close()
                    c = Client()
                    f1=c.calid(name)
                    print f1
                    xxx=self.suitable("a",idee,f1,idee,name)
                    print xxx
                    c.run(xxx)
                
            def suitable(self,sort,idee1,f1,idee,name):
                print "helllllllllloooooo"
                glee=sort+"+"+"r"+"+"+str(idee1)+"+"+str(idee)+"+"+name
                print glee
                if (fingert[0]-idee1)<0:
                    if (f1>=0 and f1<=fingert[0]) or (f1>idee1 and f1<128):
                        result=fingert[0]
                        glee=sort+"+"+"r"+"+"+str(result)+"+"+str(idee)+"+"+name
                    else:                
                        min_dist=-1
                        node=idee1
                        if f1>idee1:
                            relv=f1-idee1
                        else:
                            relv=f1+128-idee1
                        for x in fingert:
                            if x>idee1:
                                d=x-idee1
                            else:
                                d=x+128-idee1
                            if d<relv:
                                if d>min_dist:
                                    min_dist=d
                                    node=x
                                #print "s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee1)
                                glee=sort+"+"+"s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee)+"+"+name
                elif f1>idee1 and f1<=fingert[0]:
                    result=fingert[0]
                    glee=sort+"+"+"r"+"+"+str(result)+"+"+str(idee)+"+"+name
                else:
                    min_dist=-1
                    node=idee1
                    if f1>idee1:
                        relv=f1-idee1
                    else:
                        relv=f1+128-idee1
                    for x in fingert:
                        if x>idee1:
                            d=x-idee1
                        else:
                            d=x+128-idee1
                        if d<relv:
                            if d>min_dist:
                                min_dist=d
                                node=x
                            #print "s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee1)
                            glee=sort+"+"+"s"+"+"+str(node)+"+"+str(f1)+"+"+str(idee)+"+"+name
                print glee
                return glee
            def run(self,ro):
                HOST = ''
                PORT = 12
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                print 'server 12 started...'
                s.listen(5)
                i = 0
                if ro==1:
                    z=raw_input("enter the name of the file you want to share")
                    self.filed(z)
                def handleclient(s):
                    num = s.recv(1024)
                    if num=="$$":
                        #s.send(fingert[0])
                        out=open("esoteric"+str(idee)+".csv","rb")
                        data=csv.reader(out)
                        #data=[row for row in data]
                        data1=[row for row in data]
                        listp=[]
                        count=0
                        for x in range(len(data1)):
                            if data1[count][1]=="H":
                                listp.append(data1[count][0])
                                count=count+1
                        s.send(pickle.dumps(listp))
                        if s.recv(200)==str(idee):
                            s.send("end")
                        else:
                            s.send(str(fingert[0]))
                    else:                
                        num1=num.split("+")
                        if num1[1]=="r":
                            print idee
                            if num1[0]=="a":
                                print "we'll add your file"
                                with open("esoteric"+str(idee)+".csv","a") as f:
                                    print "file opened"
                                    f.write(num1[4]+","+"NH"+","+num1[3]+"\n")
                                    print "written"
                                f.close()
                                s.send("mission accomplished")
                            if num1[0]=="l":
                                print "let's search for your file"
                                out=open("esoteric"+str(idee)+".csv","rb")
                                data=csv.reader(out)
                                #data=[row for row in data]
                                data1=[row for row in data]
                                y1=len(data1)-1
                                index=-1
                                count=0
                                for x1 in range(y1):
                                    if data1[count][0]==num1[4]:
                                        print data1[count][0]
                                        print data1[count][1]
                                        index=count
                                        break
                                    count=count+1
                                print "<!------------------->"
                                print index
                                if index==-1:
                                    print "such a file doesn't exist"
                                if data1[index][1]=="H":
                                    print "you'll find the file here"
                                    s.send("ready to share the file")
                                    filename=num1[4]
                                    f=open(filename,"rb")
                                    l=f.read(1024)
                                    while(l):
                                        s.send(l)
                                        print("data is being sent")
                                        l=f.read(1024)
                                    f.close()
                                    print("sending done")
                                if data1[index][1]=="NH":
                                    x="l+r+"+data1[y1][2]+"+"+num1[3]+"+"+num1[4]
                                    s.send(x)
                                    out.close()
                    
                        if num1[1]=="s":
                            x=self.suitable(num1[0],int(num1[2]),int(num1[3]),int(num1[4]),num1[5])
                            s.send(x)
                        

                while True:
                    conn,addr=s.accept()
                    i=i+1
                    print 'connected to ',addr
                    thread.start_new_thread(handleclient,(conn,))


    class Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
            def calid(self,x):
                hash_object1 = hashlib.sha256("b'"+x+"'")
                hex_dig1 = hash_object1.hexdigest()
                ym=int(str(hex_dig1),16)
                idee1=ym%(2**7)
                print idee1
                return idee1
            def run1(self,data):
                while True:
                    PORT = int(data)
                    #print PORT
                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host = socket.gethostname()
                    c.connect((host, PORT))
                    c.send("$$")
                    data=pickle.loads(c.recv(1024))
                    count=0
                    for x in range(len(data)):
                        print data[count]
                        count=count+1
                    c.send(str(idee))
                    data=c.recv(100)
                    if data=="end":
                        break
                    while True:
                        menu = "Enter the name of the file"
                        d = raw_input(menu)
                        #c = Client()
                        f1=self.calid(d)
                        #s=Server()
                        req_node=s.suitable("l",idee,f1,idee,d)
                        c.run(req_node)
                            
                                   
                    
                
            def run(self,data):
                while True:
                    data1=data.split("+")
                    PORT = int(data1[2])
                    print PORT
                    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host = socket.gethostname()
                    c.connect((host, PORT))
                    c.send(data)
                    data=c.recv(1024)
                    print data
                    if data=="mission accomplished":
                        break
                    if data=="ready to share the file":
                        filename=raw_input("please enter the new name of the file")
                        with open(filename,"a") as f:
                            print "file opened"
                            while True:
                                print "receiving data"
                                data=c.recv(7)
                                print data
                                f.write(data)
                                if not data:
                                    break
                                
                        f.close()
                        print "file has been transferred"

    idee=12
    fingert=[37,37,37,37,37,45,85]
    x=raw_input("1.share new files\n2.look for a file\n3.just share\n")
    if x=="1":
        s=Server()
        s.run(1)
        
    elif x=='2':
        s=Server()
        c=Client()
        c.run1(fingert[0])
                
            
        '''while True:
            menu = "Enter the name of the file"
            d = raw_input(menu)
            #c = Client()
            f1=c.calid(d)
            #s=Server()
            req_node=s.suitable("l",idee,f1,idee,d)
            c.run(req_node)'''
    if x=="3":
        s=Server()
        s.run(0)
    
if __name__ == "__main__":
    main()               
    
    
            

