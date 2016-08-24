import socket,pickle
import thread,threading
import select
import time

# Control Code

valid_password = 100
invalid_password = 104
create_workspace = 102
join_workspace = 101
exit_workspace = 103
valid_index = 105
invalid_index = 106
pad = 100
empty_workspace = 110
not_empty_workspace = 111


def main():

    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1

            def join_ws(self, c, host):
                ws = c.recv(10000)
                # print ws
                workspace = pickle.loads(str(ws))
                j = 0
                for i in workspace:
                    print 'Press %d for %s' % (j, i['wsname'])
                    j += 1
                # print workspace
                c.send("now choice")
                d = raw_input(c.recv(1024))
                c.send(d)
                check = int(c.recv(1024))
                if check == invalid_index:
                    c.close()
                    return []
                d = raw_input(c.recv(1024))
                c.send(d)
                c.send('192.168.43.148')
                pswd = int(c.recv(8))
                if pswd == valid_password:
                    node = c.recv(1024)
                    node = pickle.loads(node)
                    print "head node details : ", node
                    c.send("head")
                    head = node
                    node = c.recv(1024)
                    node = pickle.loads(node)
                    print "new node details : ", node
                    new = node
                    c.close()
                    return [head, new]
                else:
                    print c.recv(1024)
                    #c.close()
                    return []

            def create_ws(self, c, host):
                # print "abc"
                d = raw_input(c.recv(1024))
                # print d
                c.send(d)
                d = raw_input(c.recv(1024))
                while True:
                    c.send(d)
                    if len(d) < 5:
                        d = raw_input(c.recv(1024))
                    elif len(d) > 30:
                        d = raw_input(c.recv(1024))
                    else:
                        break
                c.send('192.168.43.148')
                node = c.recv(2048)
                node = pickle.loads(node)
                print "head node details : ", node
                print "head node details : ", node
                head = node
                c.send("head")
                node = c.recv(2048)
                node = pickle.loads(node)
                print "new node details : ", node
                new = node
                c.close()
                return [head, new]

            def run(self):
                PORT = 1776
                c = socket.socket()
                host = '192.168.43.131' #'192.168.43.222'
                c.connect((host, PORT))
                c.send('150')
                #print c.recv(2048)
                while True:
                        num = raw_input(c.recv(2048))
                        c.send(num)
                        num = int(num) + pad
                        #print c.recv(2048)
                        #print num
                        if num == exit_workspace:
                            c.close()
                            exit()

                        elif num == create_workspace:
                            result = self.create_ws(c, host)
                            c.close()
                            return result

                        elif num == join_workspace:
                            empty_check = c.recv(1024)
                            #print empty_check
                            if empty_check == '0':
                                msg = c.recv(1024)
                                print msg
                            else:
                                result = self.join_ws(c, host)
                                if len(result) == 0:
                                    abcd = c.recv(1024)
                                else:
                                    c.close()
                                    return result

                        else:
                            msg = c.recv(1024)
                            print "Error\tInavlid input : %s\n%s\n"%(num,msg)

    # Prompt, object instantiation, and threads start here.

    c = Chat_Client()
    result = c.run()
    return result

# if __name__ == "__main__":
#     print main()