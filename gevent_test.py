import gevent
import os
import sys
#----------------------------------------------------------------------
def hehe(i):
    """"""
    for t in range(3):
        global xx
        print "thread %d :" %i,
        print "xx:%d" %xx,
        xx=xx+1
        print "->%d" %xx
        gevent.sleep(0)

if __name__=="__main__":
    print "hello world!"
    print len(sys.argv)
    print sys.argv[0]