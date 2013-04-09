from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import daemon,os,sys
from signal import SIGTERM
import time
import mod_vm
import urlparse
import json

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
        #get system running info
        elif path=="/info":
            self.send_response(200)
            self.end_headers()
            answer=mod_vm.queryModInfo()
            self.wfile.write("<html><pre>%s</pre></html>" %(answer))
            
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
        #get path and request body
        result=urlparse.urlparse(self.path)
        path=result.path
        length=int(self.headers.getheader('content-length'))
        request_body=str(self.rfile.read(length))
        request_params=urlparse.parse_qs(request_body)        
        
        #create new instance
        if path=="/instance/new":
            self.send_response(200)
            self.end_headers()
            #param:name template
            if request_params.has_key("name") and request_params.has_key("template"):
                ret_uuid=mod_vm.createVM(request_params["name"][0])
                if ret_uuid!=None:
                    ret_answer={"code":"1","UUID":ret_uuid}
                    self.wfile.write(json.dumps(ret_answer))
                else:
                    ret_answer={"code":"0"}
                    self.wfile.write(json.dumps(ret_answer))
            else:
                self.wfile.write("Request Parameters Error!")
        #suspend a vm
        elif path=="/instance/pause":
            self.send_response(200)
            self.end_headers()
            #param :uuid
            if request_params.has_key("UUID"):
                req_uuid=request_params["UUID"][0]
                ret=mod_vm.suspendVM(req_uuid)
                if ret==1:
                    ret_answer={"code":"1"}
                    self.wfile.write(json.dumps(ret_answer))
                else:
                    ret_answer={"code":"0"}
                    self.wfile.write(json.dumps(ret_answer))
        #resume a suspended vm
        elif path=="/instance/resume":
            self.send_response(200)
            self.end_headers()
            #param :uuid
            if request_params.has_key("UUID"):
                req_uuid=request_params["UUID"][0]
                ret=mod_vm.resumeVM(req_uuid)
                if ret==1:
                    ret_answer={"code":"1"}
                    self.wfile.write(json.dumps(ret_answer))
                else:
                    ret_answer={"code":"0"}
                    self.wfile.write(json.dumps(ret_answer))
        #shut down a vm
        elif path=="/instance/shutdown":
            self.send_response(200)
            self.end_headers()
            #param :uuid
            if request_params.has_key("UUID"):
                req_uuid=request_params["UUID"][0]
                ret=mod_vm.shutdownVM(req_uuid)
                if ret==1:
                    ret_answer={"code":"1"}
                    self.wfile.write(json.dumps(ret_answer))
                else:
                    ret_answer={"code":"0"}
                    self.wfile.write(json.dumps(ret_answer))
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write("URL error...")
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
            mod_vm.mod_init()
            addr=('localhost',8001)
            server=HTTPServer(addr,RESTHandler)
            print "server is running..."
            server.serve_forever()
            context.__exit__()
            exit(0)
            
if __name__=='__main__':
    serverInit()