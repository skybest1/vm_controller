import httplib
import urllib

if __name__=="__main__":
    param={}
    #vm instance id
    param["name"]="virtual machine name"
    param["length"]="123"
    body=urllib.urlencode(param)
    print body
    #
    httpconn=httplib.HTTPConnection("127.0.0.1:8001")
    url="/instance/new"
    headers={'User-Agent':"shoplug_platform/1.0","Connection":"close","Content-type":"application/x-www-form-urlencoded"}    
    httpconn.request("POST",url,body,headers)
    data=httpconn.getresponse()
    print data.read()