from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import daemon,os,sys
from signal import SIGTERM
import time
import mod_vm

########################################################################
class RESTHandler(BaseHTTPRequestHandler):
    #----------------------------------------------------------------------
    def do_GET(self):
        """"""
        #get vm templates
        if self.path=="/templates":
            self.send_response(200)
            self.end_headers()
            ret_format=str(self.headers.getheader("format"))
            answer=""
            if ret_format!=None:
                answer=answer+ret_format
            answer=self.path+" "+answer
            self.wfile.write("<html>"+answer+"</html>")
            pass
        #get vm instance info
        elif self.path=="/instances":
            self.send_response(200)
            self.end_headers()
            self.wfile.write("vm instance info:")
        #answer="<html><pre>"+mod_vm.getConfig()+"</pre></html>"
        else:
            self.send_response(404)
            self.end_headers()
            answer=""
            
            self.wfile.write(self.path+str(self.headers.getparam("format")))
    #----------------------------------------------------------------------
    def do_POST(self):
        """"""
    #----------------------------------------------------------------------
    def do_PUT(self):
        """"""
    #----------------------------------------------------------------------
    def do_DELETE(self):
        """"""
        
    
        
#----------------------------------------------------------------------
def serverInit():
    """"""
    context=daemon.DaemonContext()
    with context:
        if os.path.exists("/var/run/rendervmd.pid"):
            try:
                pf=open("/var/run/rendervmd.pid","r")
                pid=int(pf.read().strip())
                pf.close()
                if pid!=None:
                    os.kill(pid,SIGTERM)
                    os.remove("/var/run/rendervmd.pid")
            except Exception:
                sys.stderr.write("error in vm daemon!")
        else:
            pf=open("/var/run/rendervmd.pid","w+")
            pid=int(os.getpid())
            pf.write(str(pid))
            pf.close()
            
            #start Http Service
            addr=('localhost',8001)
            server=HTTPServer(addr,RESTHandler)
            print "server is running..."
            server.serve_forever()
            context.__exit__()
            exit(0)
            
if __name__=='__main__':
    serverInit()