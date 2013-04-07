from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import daemon,os,sys
from signal import SIGTERM
import time
import mod_vm
import urlparse

########################################################################
class RESTHandler(BaseHTTPRequestHandler):
    #----------------------------------------------------------------------
    def do_GET(self):
        """"""
        #get path and params
        result=urlparse.urlparse(self.path)
        path=result.path
        params=urlparse.parse_qs(result.query,True)
        
        #get vm templates
        if path=="/templates":
            self.send_response(200)
            self.end_headers()
            answer=mod_vm.getConfig().replace('<',"&lt;").replace('>',"&gt;")
            self.wfile.write("<html><pre>"+answer+"</pre></html>")
            
        #get vm instance info
        elif self.path=="/instances":
            self.send_response(200)
            self.end_headers()
            self.wfile.write("vm instance info:")
            
        else:
            self.send_error(404,"URL Error!")
            self.end_headers()
    #----------------------------------------------------------------------
    def do_POST(self):
        """"""
        #get path and params
        result=urlparse.urlparse(self.path)
        path=result.path
        #new instance
        if path=="/instance/new":
            self.send_response(200)
            self.end_headers()
            length=int(self.headers.getheader('content-length'))
            request_body=str(self.rfile.read(length))
            
            self.wfile.write()
            
        elif path=="/instance/start":
            pass
        elif path=="/instance/stop":
            pass
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