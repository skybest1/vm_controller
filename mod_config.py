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
def getIPAddress(path,ips):
    """"""
    doc=xml.dom.minidom.parse(path+"/config/vm_config.xml")
    for node in doc.getElementsByTagName("hostip"):
        if node.hasChildNodes():
            ips.append(str(node.childNodes[0].nodeValue))
    return True

#----------------------------------------------------------------------
def getTemplate(path):
    """"""
    vmtemplate=open(path+"/template/Windows2k8.xml").read()
    return vmtemplate

if __name__=="__main__":
    ips=[]
    print ips
    getIPAddress(ips)
    print ips