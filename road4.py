import pickle
import socket
from threading import Thread

parts = {}
threads = []
# file_name = '007.gif'


def check_online(ip, port, file_name):
    try:
        client = socket.socket()
        print "socket"
        client.connect((ip, port))
        message = ["online", 10, file_name]
        client.send(pickle.dumps(message))
        print client.recv(1024)
        client.close()
        return 1

    except Exception as e:
        print e
        return 0


def request_file(client, message, iter):
    temp2 = ''
    client.send(pickle.dumps(message))
    while True:
        temp = client.recv(1024)    # receive upto not complete
        client.send("received")
        if temp == "empty":
            break
        print "previous"
        print temp
        print "reached"
        temp2 += temp
        #print temp2
    print "received chunk"
    parts[iter] = temp2


def function(list, file_name, S,filepath):
    count = 0
    print list
    for dictionary in list:
        print dictionary
        ip=dictionary['host']
        port=int(dictionary['port'])
        print port
        dictionary["online"] = check_online(ip, port, file_name)
        if dictionary["online"] == 1:
            count += 1
        print "woh"
        print dictionary

    print count

    for dictionary in list:
        if dictionary["online"] == 1:
            client = socket.socket()
            client.connect((dictionary['host'], int(dictionary['port'])))
            message = ["file_size", 9, file_name]
            client.send(pickle.dumps(message))
            size = client.recv(1024)
            client.close()
            chunk_size = int(int(size) / count)
            last_chunk_size = int(size) - (chunk_size * (count - 1))
            break

    iter = -1
    for dictionary in list:
        if dictionary["online"] == 1:
            iter += 1
            client = socket.socket()
            client.connect((dictionary['host'], int(dictionary['port'])))
            if iter == int(size) - 1:
                message = [file_name, 11, chunk_size * iter, int(size) - 1]
            else:
                message = [file_name, 11, chunk_size * iter, (chunk_size*(iter+1))-1]
            t=Thread(target=request_file, args=(client, message, iter))
            t.start()
            threads.append(t)

    for i in threads:
        i.join()

    print "end"
    result = ''
    for i in range(count):
        #print parts[i]
        result += parts[i]
    print result
    with open(filepath, 'wb') as f:
        f.write(result)
        f.close()
        S.filed(file_name,filepath)
# if __name__ == '__main__':
    # list = [{'host': '192.168.254.1', 'port': 5000}, {'host': '192.168.254.1', 'port': 5050}, {'host': '192.168.254.1', 'port': 5100}]
    # print list
    # for dictionary in list:
    #    print dictionary
    # function(list)

        # node = {"id": self.id, "host": self.host, "port": self.port}
        # message = [id, 4, node, i]
        # client.send(pickle.dumps(message))
