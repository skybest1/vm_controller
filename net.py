#from socket import *
import time

host=''
port=80
addr=(host,port)
conn=socket(AF_INET,SOCK_STREAM)
conn.bind(addr)
conn.listen(5)

while True:
    print "waiting for connection..."
    client,addr=conn.accept()
    print "receive package from", addr
    
    data=client.recv(2048)
    client.send("data:\n[%s] data\n %s" %(data,time.ctime()))
    print "send back!"
    client.close()
    
    #client.close()