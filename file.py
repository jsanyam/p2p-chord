checkout_ ='170'
getfile_ = '180'
upload='190'
latest_upload='200'
host = '192.168.43.131'
port=1776
from sets import Set
from shutil import copyfile
import os
import socket


def paths(path, assigned_port,S):
    set_file=Set()
    set_name=Set()
    #path="C:\\nltk_data\\chunkers";
    c=socket.socket()
    c.connect((host,port))
    c.send(latest_upload)
    print c.recv(1024)
    c.send(str(assigned_port))#port
    version=c.recv(1024)
    print version
    inp=""
    for root,dirs,files in os.walk(path):
        for file in files:
            src=root+"\\"+ str(file)

            splitarr=file.split(".")
            if len(splitarr)==1:
                mem=splitarr[0]+"_"+str(version)
            else:
                mem=splitarr[0]+"_"+str(version)+"."+splitarr[1]

            if mem in set_name: continue
            src=src.replace("\\\\","\\")
            inp+=src+"\n"
            set_name.add(mem)
            copyfile(src,"gitstore"+'/'+mem)
            set_file.add("gitstore"+'/'+mem)
            print inp
            #print root+"\\"+splitarr[0]+"_"+str(version)+"."+splitarr[1]

    for file in set_file:
        print file
        fileName=file.split("/")[-1]
        S.upload(fileName)

    print inp
    c.send(inp)
    print "Successfully commited"

def make_directory(path):
    os.mkdir( path, 0755 );

def head_download(assigned_port,v):

    c=socket.socket()
    c.connect((host,port))
    c.send(checkout_)
    print c.recv(1024)
    c.send(str(assigned_port))
    print c.recv(1024)
    c.send(str(v))
    filename=c.recv(1024)
    print filename
    print filename+"))))"
    filename=filename.strip("_folder.txt")
    c.send("file name recieved")
    print filename+"))))"
    leng=int(c.recv(1024))

    c.send('ok')
    st=c.recv(leng)
    c.send("ok")
    c.close()
    print filename
    fo=open(filename+"_","wb")
    fo.write(st)
    fo.close()

    return filename

def checkout(assigned_port,s,v=0):
    filename=head_download(assigned_port,v)
    make_directory(filename)
    path=filename+"/"
    download_recursive(filename+"_",path,assigned_port,s)




def get_file(filename,assigned_port):
    c=socket.socket()
    c.connect((host,port))
    c.send(getfile_)
    print c.recv(1024)
    c.send(str(assigned_port))
    print c.recv(1024)
    c.send(filename)


    filename=filename[:-13]

    leng=int(c.recv(1024))
    c.send('ok')
    st=c.recv(leng)


    c.close()
    fo=open(filename,"wb")
    fo.write(st)
    fo.close()



def download_at_this(path,file,s):
    print file+"###"
    print "searching"+file
    s.download(file,path+file)
    copyfile(path+file,"gitstore"+'/'+file)
    #file = open(path+file,'w')
    #file.close()

def download_recursive(filename,path,assigned_port,s):


    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        print line+"()()()()()"
        if not line : continue
        if(line[-1]=="\n"):line=line[:-1]
        print line+"--"
        if line.endswith("_folder.txt"):
            print path+"____"
            print "making "+(path+line)

            make_directory(path+line[:-13])
            print("send recur "+line)
            get_file(line,assigned_port)

            folder_name=line
            print folder_name+"<>"
            folder_name=folder_name[:-13]
            print folder_name+"<><>"
            download_recursive(folder_name,path+folder_name+"/",assigned_port,s)
        else:
            print "path now "+path
            download_at_this(path,line,s)

#checkout()
