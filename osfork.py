import time,os,sys

pid=os.fork()
#in the father process
if pid>0:
    fd=open("/tmp/daemon.log","a")
    fd.write("father %s leave at %s \n" %(os.getppid(),time.ctime()))
    fd.flush()
    fd.close()
    os._exit(0)

#in the child process
fd=open("/tmp/daemon.log","a+")
fd.write("child %d begin at %s \n" %(pid,time.ctime()))
fd.flush()
for i in range(3):
    fd.write("deamon log %s \n" %time.ctime())
    fd.flush()
    time.sleep(5)
fd.close()

