__author__ = 'SANCHIT'
import os, sys
# Path to be created
# c = '20000'
# path = "C:\Users\SANCHIT\PycharmProjects\untitled3\es"+str(c)
# os.mkdir( path, 0755 )
# verse = 1
# fo =open(path+'version.txt','wb')
# fo.write(str(verse))
# fo.close()

def paths():
    path="D:\\html";
    str=path.split("\\");
    print str[-1]
    print ""
    inp=""
    for root,dirs,files in os.walk(path):
        for file in files:
            inp+=root+"\\"+file+"\n"
    return inp

def make_file(filename, port):
    path = 'es'+port+'/'+filename+'.txt'
    fo = open(path, "wb")
    fo.close()

def update_folder(filename, version, filedata, port):
    flg = 0
    filedata1 = []
    filedata2 = []
    path = 'es'+port+'/'+filename+'.txt'
    fo = open(path, "rb")
    fdata = fo.read()
    fo.close()
    adata = filedata[0].split('\\',1)
    for i in xrange(len(filedata)):
        xdata = filedata[i].split('\\',1)
        if adata[0] == xdata[0] and len(xdata) == 1:
            try:
                xd = xdata[0].rsplit('.',1)
                fdata = fdata + '\n' +xd[0] + version + '.' + xd[1]
                filedata[i]=filedata[i].replace(xdata[0],'')
            except IndexError:
                xd = xdata[0].rsplit('.',1)
                fdata = xd[0] + version
                filedata[i]=filedata[i].replace(xdata[0],'')

        elif adata[0] == xdata[0] and len(xdata) > 1:
            xd = xdata[0]+'\\'
            filedata[i]=filedata[i].replace(xd,'')
            filename1 = xdata[0] +version+ '_folder'
            # print filename
            filedata2.append(filedata[i])
            flg = 1
        else:
            filedata1.append(filedata[i])
    if flg == 1:
        fdata = adata[0] + version + '_folder.txt\n' + fdata

    leng = len(filedata1)
    fo = open(path, "wb")
    fo.write(fdata)
    fo.close()
    if flg == 1:
        print filename
        make_file(filename1, port)
        make_folder(filename1, version, filedata2, port)
    while leng > 0:
        leng = update_folder(filename, version, filedata1, port)
    return leng

def make_folder(filename, version, filedata, port):
    flg = 0
    filedata1 = []
    filedata2 = []
    path = 'es'+port+'/'+filename+'.txt'
    adata = filedata[0].split('\\', 1)
    for i in xrange(len(filedata)):
        xdata = filedata[i].split('\\', 1)
        if adata[0] == xdata[0] and len(xdata) == 1:
            try:
                xd = xdata[0].rsplit('.',1)
                fdata = xd[0] + version + '.' + xd[1]
                filedata[i]=filedata[i].replace(xdata[0],'')
            except IndexError:
                xd = xdata[0].rsplit('.',1)
                fdata = xd[0] + version
                filedata[i]=filedata[i].replace(xdata[0],'')
        elif adata[0] == xdata[0] and len(xdata) > 1:
            xd = xdata[0]+'\\'
            filedata[i]=filedata[i].replace(xd,'')
            filename1 = xdata[0] + version + '_folder'
            filedata2.append(filedata[i])
            # print filename
            flg = 1
        else:
            filedata1.append(filedata[i])
    if flg == 1:
        fdata = adata[0] + version +'_folder.txt\n'
    fo = open(path, "wb")
    fo.write(fdata)
    fo.close()
    leng = len(filedata1)
    while leng > 0:
        leng = update_folder(filename, version, filedata1, port)
    # print root
    if flg == 1:
        print filename
        make_file(filename1, port)
        make_folder(filename1, version,filedata2, port)
        # print filedata

def make_root(root, version, port):
    path = 'es'+ port + '/' + 'root.txt'
    print path
    fo = open(path, "rb")
    fdata = fo.read()
    fo.close()
    print fdata
    fdata = fdata + '\n' + root + '.txt'
    fo = open(path, "wb")
    fo.write(fdata)
    fo.close()

def get_common_path():
    return rootcp


def maintain(c,x):
    print c
    print x
    fo =open("es"+c+"/"+"version.txt",'rb')
    version = fo.read()
    fo.close()

    verse = int(version) +1
    version = '_'+version

    fo =open('es'+c+'/version.txt','wb')
    fo.write(str(verse))
    fo.close()

    rootstr = x.split('\n')
    if not rootstr[-1]:
        rootstr.pop()
    commonpath = os.path.commonprefix(rootstr)
    print "Path is created"
    commonsplit = commonpath.split("\\")
    rootcp = commonsplit[-2]
    root = []
    rootadd = []
    for i in rootstr:
        try:
            i = i.split(rootcp+'\\',1)
            root.append(i[1])
            print root
        except IndexError:
            break
    rootcp = rootcp + version
    if version == '1':
        make_file('root', c)
    make_root(rootcp, version, c)
    make_file(rootcp, c)
    make_folder(rootcp,version,root,c)