import socket,pickle,csv
import thread,threading
import select
import time
import hashlib
import road4
#import node
import wx
class Client(threading.Thread):

        def __init__(self, idee, s,port):
            threading.Thread.__init__(self)
            self.host = None
            self.sock = None
            self.running = 1
            self.idee = idee
            self.s = s
            self.port=port

        def calid(self, x):
            hash_object1 = hashlib.sha256("b'"+x+"'")
            hex_dig1 = hash_object1.hexdigest()
            ym=int(str(hex_dig1),16)
            idee1=ym%(2**7)
            print idee1
            return idee1
        def yess(self,f1,id,succ):
                f1=int(f1)
                succ=int(succ)
                id=int(id)
                if f1<succ:
                        ds=succ-f1
                else:
                        ds=succ+128-f1
                if f1<id:
                        dm=id-f1
                else:
                        dm=id+128-f1
                if dm<ds:
                        return True
                else:
                        return False
        def update(self,port,idee,succid,hostt):
                PORT = int(port)
                print PORT
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = hostt
                try:
                        c.connect((host, PORT))
                except socket.gaierror:
                        print "sorry but you were unable to connect"
                #c.connect((host,PORT))
                c.send("file handling")
                print c.recv(1024)
                c.send("$1")
                temp = ''
                data=[]
                while True:
                    end = c.recv(1024)
                    if end == "terminate":
                        #print "yoyo"
                        break
                    data.append(pickle.loads(end))
                    # time.sleep(1)
                    c.send("okk")
                count = 0
                with open("esoteric"+str(idee)+".csv","a") as f:
                        print "file opened"
                        count=0
                        for x in range(len(data)):
                                if self.yess(data[count][2],idee,succid):
                                        info=data[count][0]
                                        for y in range(len(data[count])-1):
                                                info=info+","+data[count][y+1]
                                        f.write(info+"\n")
                                        #print "written"
                                count=count+1
                        f.close()
                c.close()

        def run1(self, port,hostt,S):
            listp=[]    
            while True:    
                PORT = int(port)
                #print PORT
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = hostt
                #print "port"
                #print PORT
                try:
                        c.connect((host, PORT))
                except socket.gaierror:
                        print "sorry but you were unable to connect"
                c.send("file handling")
                print c.recv(1024)
                c.send("$$")
                data = pickle.loads(c.recv(1024))
                count = 0
                for x in range(len(data)):
                    print data[count]
                    listp.append(data[count])
                    count += 1
                c.send(str(self.idee))
                data1=c.recv(100)
                if data1=="end":
                        break
                else:
                        data2=data1.split("+")
                        port=data2[0]
                        hostt=data2[1]
                c.close()
            #print "listttttpppp"
            #print listp
            app=wx.App()
            w=windowClass2(None)
            w.basicGUI(listp,self,S)
            app.MainLoop()

        def run3(self, d, S, filepath):
            #while True:
                #menu = "Enter the name of the file"
                #d = raw_input(menu)
                f1 = self.calid(d)
                req_node = self.s.suitable("l", self.idee, f1, self.idee, d,self.port,self.s.host)
                self.run(req_node,S,filepath)

        def fille(self, filename, c, S):
            with open(filename, "wb") as f:
                print "file opened"
                while True:
                    print "receiving data"
                    time.sleep(2)
                    data = c.recv(1024)
                    print "woohooooo"
                    c.send("ok")
                    print data
                    time.sleep(2)
                    if data == "empty":
                        break
                    f.write(data)
            f.close()
            print "file has been transferred"
            fileName=c.recv(50)
            with open("esoteric"+str(S.id)+".csv","a") as f:
                    print "file opened"
                    f.write(fileName+","+"H\n")
                            #f.write(fileName+","+"NH"+","+str(S.id)+","+str(S.port)+","+str(lo)+","+str(S.host)+"\n")
                    print "written"
            f.close()
            S.filed1(fileName)

        def run(self, data, S,filepath):
            arr=[]
            fileName=''
            while True:
                data1 = data.split("+")
                PORT = int(data1[3])
                print PORT
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = data1[8]
                #c.connect((host, PORT))
                try:
                    print "error"
                    print host
                    print PORT
                    c.connect((host, PORT))
                except socket.gaierror:
                    print "sorry but you were unable to connect"
                print "i am connected to:"+str(PORT)
                c.send("file handling")
                print c.recv(1024)
                c.send(data)
                data = c.recv(1024)
                print data
                if data=="mission accomplished":
                    c.close()    
                    break
                if data=="reached":
                    c.send("send filename")
                    fileName=c.recv(50)
                    c.send("send list")
                    arr=pickle.loads(c.recv(1024))
                    road4.function(arr, fileName, S,filepath)
                    c.close()
                    break
            #print "arrrrrrrrrrrrrrrrr"
            #print arr
            #print "filenameeeeeeeeeeeeeee"
            #print fileName

            #road3.function(arr,fileName)
                    
                    #app=wx.App()
                    #w=windowClass2(None)
                    #w.basicGUI2(self,c,S)
                    #app.MainLoop()      
                    #filename=raw_input("please enter the new name of the file")


class windowClass2(wx.Frame):
    def __init__(self, *args, **kwargs):
        print "bskjhkqehblhblt"
        super(windowClass2, self).__init__(*args, **kwargs)

        #self.basicGUI()
    def basicGUI2(self, C, c,S):
        nameBox=wx.TextEntryDialog(None,'Please enter the new name of file you wish to add','welcome')
        fileName=''
        if nameBox.ShowModal()==wx.ID_OK:
            fileName=nameBox.GetValue()
        C.fille(fileName,c,S)

    def basicGUI(self,listp,C,S):
        print "dakbhklgligb"
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

        self.Bind(wx.EVT_MENU,self.Quit,exitItem)

        chooseOneBox=wx.SingleChoiceDialog(None,'Please select one option from below',
                                           'choice',listp)
        option=[]
        if chooseOneBox.ShowModal()==wx.ID_OK:
            option=chooseOneBox.GetStringSelection()
            C.run3(option,S)
        '''if option=="add a new file":
            nameBox=wx.TextEntryDialog(None,'Please enter the name of file you wish to add','welcome')
            if nameBox.ShowModal()==wx.ID_OK:
                fileName=nameBox.GetValue()
                #S=Node(a,b,c)
                S.filed(fileName)
        if option=="download a file":
            nameBox1=wx.TextEntryDialog(None,'Please enter the name of file you wish to download','welcome')
            if nameBox1.ShowModal()==wx.ID_OK:
                fileName1=nameBox1.GetValue()
                c=mehar.Client(self.id, self,self.port)
                c.run1(fingert[0])'''

            #wx.TextCtrl(panel,pos=(3,10),size=(150,50))
            #aweText=wx.StaticText(panel, -1, "Awesome Text" , (3,3))
            #aweText.setForegroundColor('#67cddc')
            #aweText.setForegroundColor('black')
        

        self.SetTitle('Epic Window')

        self.Show(True)
    def Quit(self,e):
        self.Close()
    #idee = 12
    #finger = [37, 37, 37, 37, 37, 45, 85]
    #s = Server()
    #s.run()

#if __name__ == "__main__":
#    main()