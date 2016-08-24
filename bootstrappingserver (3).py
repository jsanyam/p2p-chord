import socket,pickle
import thread,threading
import hashlib
import os, sys
import path
import time

# Control Code

valid_password = 100
invalid_password = 104
valid_index = 105
invalid_index = 106
create_workspace = 102
join_workspace = 101
workspace_database = '150'
file_database = '160'
file_upload = '161'
file_download = '162'
checkout_ = '170'
getfile_='180'
upload = '190'
latest_upload = '200'
exit = 103
pad = 100
len_ws = 0
flag = 100
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("gmail.com",80))
# HOST = s.getsockname()[0]
# # print(s.getsockname()[0])
# s.close()

HOST = '192.168.43.131'#'192.168.43.148'
PORT = 1776
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))
print 'bootstrapping server started...'
s.listen(1)

fo = open("database.jpg", "rb")
workspace = fo.read()
fo.close()
if len(workspace) == 0:
    workspace = []
else:
    workspace = pickle.loads(workspace)

fo = open("database2.jpg", "rb")
users = fo.read()
fo.close()
if len(users) == 0:
    users = []
else:
    users = pickle.loads(users)

fo = open("database3.jpg", "rb")
filespace = fo.read()
fo.close()
if len(filespace) == 0:
    filespace = []
else:
    filespace = pickle.loads(filespace)

def return_port(d, ws):
    rport = (d+1)*5000
    #print rport
    for j in xrange(5000):
        print ws[d]['peers']
        flag = 0
        for k in xrange(len(ws[d]['peers'])):
            #print ws[j]['peers'][k]['port']
            if rport == int(ws[d]['peers'][k]['port']):
                #print rport
                flag = 1
        if flag == 0:
            return rport
        rport = rport + 1
        #print rport


def return_key(port, host):
    list = []
    list.append(port)
    list.append(host)
    lst = pickle.dumps(list)
    hash_object = hashlib.sha256("b'"+lst+"'")
    hex_digit1 = hash_object.hexdigest()
    y = int(str(hex_digit1), 16)
    key = y%(2**7)
    #print key
    return key

def create_ws(s, workspace):
    global flag
    msg = "Enter Workspace : "
    s.send(msg)
    while True:
        ws_name = s.recv(1024)
        if len(ws_name) < 4:
            msg = "Password too short\nEnter again : "
            s.send(msg)
        elif len(ws_name) > 30:
            msg = "Password too long\nEnter again : "
            s.send(msg)
        else:
            break
    msg = "Enter password : "
    s.send(msg)
    while True:
        ws_password = s.recv(1024)
        if len(ws_password) < 5:
            msg = "Password too short\nEnter again : "
            s.send(msg)
        elif len(ws_password) > 30:
            msg = "Password too long\nEnter again : "
            s.send(msg)
        else:
            break
    len_ws = len(workspace)
    workspace.append({'wsname': ws_name, 'wspassword': ws_password, 'peers': []})
    ip = s.recv(1024)
    if flag == valid_password:
        gport = return_port(len_ws, workspace)
        print 'port', gport
        path = "C:\Users\The Virgillos\Desktop\codes\es"+str(gport)
        os.mkdir( path, 0755)
        path = 'es'+str(gport)+'/root.txt'
        fo = open(path, "wb")
        fo.close()
        path = 'es'+str(gport)+'/version.txt'
        fo = open(path, "wb")
        fo.write('1')
        fo.close()
        key = int(return_key(gport, ip))
        print 'key', key
        workspace[len_ws]['peers'].append({'id': key, 'host': ip, 'port': gport})
        node = pickle.dumps(workspace[len_ws]['peers'][0])
        s.send(node)
        z = s.recv(1024)
        s.send(node)
        print pickle.loads(node)
        print workspace
        fo = open("database.jpg", "wb")
        ws = pickle.dumps(workspace)
        fo.write(ws)
        users.append({'host': ip, 'port': gport})
        fo = open("database2.jpg", "wb")
        us = pickle.dumps(users)
        fo.write(us)
        fo.close()
    else:
        msg = "password invalid"
        s.send(msg)


def join_ws(s,workspace):
    flag = 100
    ws = pickle.dumps(workspace)
    s.send(ws)
    pqrs = s.recv(1024)
    msg = "Enter your choice : "
    s.send(msg)
    len_ws = int(s.recv(8))
    if len_ws >= len(workspace):
        s.send(str(invalid_index))
        return invalid_index
    else:
        s.send(str(valid_index))
        msg = "Enter password : "
        s.send(msg)
        pswd = s.recv(30)
        print workspace[len_ws]['wspassword']
        if pswd != workspace[len_ws]['wspassword']:
            flag = 101
        ip = s.recv(1024)
        if flag == valid_password:
            s.send('100')
            flg = 0
            print users
            for i in users:
                print i['host']
                if ip == i['host']:
                    flg = 1
                    gport = i['port']
                    break
            if flg == 0:
                gport = return_port(len_ws, workspace)
                print 'port', gport
            key = int(return_key(gport, ip))
            print 'key', key
            workspace[len_ws]['peers'].append({'id': key, 'host': ip, 'port': gport})
            node = pickle.dumps(workspace[len_ws]['peers'][0])
            s.send(node)
            z = s.recv(1024)
            len_p = len(workspace[len_ws]['peers']) - 1
            node = pickle.dumps(workspace[len_ws]['peers'][len_p])
            s.send(node)
            print workspace
            fo = open("database.jpg", "wb")
            ws = pickle.dumps(workspace)
            fo.write(ws)
            fo.close()
            return valid_password
        else:
            s.send('101')
            msg = "password invalid"
            s.send(msg)
            return invalid_password

def get_version1(s, version, gport):
    path = 'es'+gport+'/root.txt'
    #print path
    fo = open(path, 'rb')
    rootstr = fo.read()
    fo.close()
    path = 'es'+gport+'/version.txt'
    fo = open(path, 'rb')
    length = fo.read()
    fo.close()
    version = int(version)
    if version != 0:
        version = int(length) - version - 1
    rootstr = rootstr.split('\n')
    path = 'es'+gport+'/'+rootstr[len(rootstr)-1-version]
    #print path
    fo =open(path, 'rb')
    filedata = fo.read()
    fo.close()
    return filedata

def get_name1(s, version, gport):
    path = 'es'+gport+'/root.txt'
    print path
    fo = open(path, 'rb')
    rootstr = fo.read()
    fo.close()
    path = 'es'+gport+'/version.txt'
    print path
    fo = open(path, 'rb')
    length = fo.read()
    fo.close()
    rootstr = rootstr.split('\n')
    version = int(version)
    if version != 0:
        version = int(length) - version -1
    filename = rootstr[len(rootstr)-1-version]
    return filename

def get_version2(s, version, gport):
    path = 'es'+gport+'/'+version
    fo =open(path, 'rb')
    filedata = fo.read()
    fo.close()
    return filedata

def get_name2(s, version, gport):
    path = 'es'+gport+'/root.txt'
    fo = open(path, 'rb')
    rootstr = fo.read()
    fo.close()
    #print rootstr
    rootstr = rootstr.split('\n')
    #print rootstr
    filename = 'es'+gport+version
    return filename

def getfile(s):
    gport = s.recv(10)
    gport = int(gport)/5000
    gport = gport*5000
    msg = 'Port recieved '
    s.send(msg)
    print gport
    version = s.recv(1024)
    # filename = get_name2(s, version, gport)
    # s.send(filename)
    # print filename
    filedata = get_version2(s, version, str(gport))
    leng = len(filedata)
    leng = str(leng)
    print leng
    s.send(leng)
    print s.recv(1024)
    print filedata
    s.send(filedata)

def checkout(s):
    gport = s.recv(10)
    gport = int(gport)/5000
    gport = gport*5000
    msg = 'Port recieved '
    print gport
    s.send(msg)
    version = s.recv(1024)
    print version
    gport = str(gport)
    filename = get_name1(s, version, gport)
    print filename
    s.send(filename)
    print s.recv(1024)
    filedata = get_version1(s, version, gport)
    print filedata
    leng = len(filedata)
    leng = str(leng)
    s.send(leng)
    s.recv(1024)
    s.send(filedata)
    print s.recv(1024)


    # str = s.recv(1024)

def handleclient(s):
    while True:
        check = s.recv(1024)
        if check == workspace_database:
            menu = "Press 1 to join existing workspace \nPress 2 to create new workspace\nPress 3 to exit\nEnter your choice : "
            s.send(menu)
            num = int(s.recv(1024))
            num += pad
            print num
            if num == exit:
                break

            elif num == create_workspace:
                create_ws(s, workspace)
                break

            elif num == join_workspace:
                ln = len(workspace)
                s.send(str(ln))
                #print ln
                if ln != 0:
                    check = join_ws(s, workspace)
                    if check == invalid_index:
                        msg = "invalid choice\n"
                        s.send(msg)
                    else:
                        if check == invalid_password:
                            msg = "invalid password"
                            s.send(msg)
                        else:
                            break
                else:
                    msg = "No workspace available\n"
                    s.send(msg)

            else:
                msg = "Enter valid choice"
                s.send(msg)
                #print 'password invalid'
        # elif check == file_upload:
        #     s.send('bok')
        #     filename = s.recv(1024)
        #     flg = 0
        #     for i in filespace:
        #         if filename == i['filename']:
        #             flg = 1
        #             break
        #     if flg == 0:
        #         filespace.append({'filename': filename})
        #         fo = open("database3.jpg", "wb")
        #         fs = pickle.dumps(filespace)
        #         fo.write(fs)
        #         fo.close()
        # else:
        #     print filespace
        #     fs = 'filename'
        #     for i in filespace:
        #         fs = fs+'_'+i['filename']
        #     print fs
        #     s.send(fs)
        elif check == file_upload:
            s.send('bok')
            filename = s.recv(1024)
            s.send('port')
            gport = int(s.recv(1024))
            gport = gport/5000
            gport = gport*5000
            flg = 0
            fo = open('es'+str(gport)+'/'+'databse.png','rb')
            fs = fo.read()
            fo.close()
            filespace = pickle.loads(fs)
            for i in filespace:
                print i['filename']
                if filename == i['filename']:
                    flg = 1
                    break
            if flg == 0:
                filespace.append({'filename': filename})
                fo = open('es'+str(gport)+'/'+'databse.png', "wb")
                fs = pickle.dumps(filespace)
                fo.write(fs)
                fo.close()

        elif check == checkout_:
            s.send('bok')
            checkout(s)
        elif check == getfile_:
            s.send('bok')
            getfile(s)
        elif check == upload:
            s.send('ohk')
            pathp = s.recv(1024)
            path.maintain(str(gport),pathp)

        elif check == latest_upload:
            s.send('ohk')
            gport = int(s.recv(1024))/5000
            gport = gport * 5000
            setpath = 'es'+str(gport)+'/'+'version.txt'
            fo = open(setpath,'rb')
            version = fo.read()
            fo.close()
            s.send(version)
            pathp = s.recv(1024)
            print pathp
            print gport
            path.maintain(str(gport), pathp)
        elif check == file_download:
            s.send('bok')
            gport = int(s.recv(1024))
            gport = gport/5000
            gport = gport * 5000
            fo = open('es'+str(gport)+'/'+'databse.png','rb')
            fs = fo.read()
            fo.close()
            filespace = pickle.load(fs)
            fs = 'filename'
            for i in filespace:
                fs = fs+'_'+i['filename']
            print fs
            s.send(fs)
        else:
            break

while True:
    conn,addr=s.accept()
    print 'connected to ',addr
    thread.start_new_thread(handleclient,(conn,))
    # handleclient(conn)
