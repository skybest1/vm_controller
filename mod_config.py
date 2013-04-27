import xml.dom.minidom
import os
#----------------------------------------------------------------------
def setName(xmlcofig,name):
    """"""
    doc=xml.dom.minidom.parseString(xmlcofig)
    for node in doc.getElementsByTagName("name"):
        if node.hasChildNodes():
            node.childNodes[0].nodeValue=name
    return str(doc.toxml())
#----------------------------------------------------------------------
#get cluster host ip address
def getIPAddress():
    """"""
    ips=[]
    doc=xml.dom.minidom.parse(os.getcwd()+"/config/vm_config.xml")
    for node in doc.getElementsByTagName("hostip"):
        if node.hasChildNodes():
            ips.append(str(node.childNodes[0].nodeValue))
    return ips

#----------------------------------------------------------------------
def getTemplate():
    """"""
    vmtemplate=open(os.getcwd()+"/template/Windows2k8.xml").read()
    ret={}
    ret['Windows2k8']=vmtemplate
    return ret

if __name__=="__main__":
    log=open(os.getcwd()+"/errorlog.log","a+")
    log.write("hello world!\n")