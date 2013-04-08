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
        elif path=="/instances":
            self.send_response(200)
            self.end_headers()
            if params.has_key("UUID") and params.has_key("format"):
                req_UUID=params["UUID"][0]
                req_format=params["format"][0]
                #query vminfo
                query_result=mod_vm.queryVM(req_UUID,req_format)
                if query_result!=None:
                    if req_format=="json":
                        self.wfile.write(query_result)
                    else:
                        self.wfile.write("<html><pre>%s</pre></html>"%(query_result))
                else:
                    self.wfile.write("Query Fail!")
            else:
                self.wfile.write("Bad Request")
        else:
            self.send_error(404,"URL Error!")
            self.end_headers()
    #----------------------------------------------------------------------
    def do_POST(self):
        """"""
        #get path and params
        result=urlparse.urlparse(self.path)
        path=result.path
        
        #create new instance
        if path=="/instance/new":
            self.send_response(200)
            self.end_headers()
            #read and parse POST request body
            length=int(self.headers.getheader('content-length'))
            request_body=str(self.rfile.read(length))
            request_params=urlparse.parse_qs(request_body)
            #param:name template
            if request_params.has_key("name") and request_params.has_key("template"):
                ret_uuid=mod_vm.createVM(request_params["name"][0])
                if ret_uuid!=None:
                    self.wfile.write("VM Created...\nVM UUID:%s" %ret_uuid)
                else:
                    self.wfile.write("Cannot create VM...")
            else:
                self.wfile.write("Request Parameters Error!")
            
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