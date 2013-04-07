#!/usr/bin/python
#module:virtual machine controller based on libvirt
#author:Yuwenhao
#date:13-1-10

import libvirt
import os

#"ip":connection object,connections should keep alive
connectionpool={}
#"ip":['uuid1','uuid2']
vmpool={}
#"uuid":"host ip"
vmmap={}

config={}
fd=open("/home/achilles/docs/config/Windows2k8.xml","r")
lines=fd.readlines()
ss=""
for line in lines:
    ss=ss+line

config["Windows2k8"]=ss

#----------------------------------------------------------------------
#create vm on a host,with given xml-based configuration.
def createVM(ip,xmlconfig):
    """"""
    if connectionpool.has_key(ip):
        conn=connectionpool[ip]
        if conn.isAlive():
            vm=conn.createLinux(xmlconfig,0)
            #add to list
            vmmap[vm.UUIDString()]=ip
            if(vmpool.has_key(ip)):
                vmpool[ip].append(vm.UUIDString())
            else:
                vmpool[ip]=[]
                vmpool[ip].append(vm.UUIDString())
            return vm.UUIDString()
        else:
            conn=libvirt.open(conn.getURI())
            vm=conn.createLinux(xmlconfig,0)
            connectionpool[ip]=conn
            #add to list
            vmmap[vm.UUIDString()]=ip
            if(vmpool.has_key(ip)):
                vmpool[ip].append(vm.UUIDString())
            else:
                vmpool[ip]=[]
                vmpool[ip].append(vm.UUIDString())
            return vm.UUIDString()
    else:
        try:
            param="qemu+ssh://root@"+ip+"/system"
            conn=libvirt.open(param)
            vm=conn.createLinux(xmlconfig,0)            
            #conn.setKeepAlive(5,5)
            connectionpool[ip]=conn
            #add to list
            vmmap[vm.UUIDString()]=ip
            if(vmpool.has_key(ip)):
                vmpool[ip].append(vm.UUIDString())
            else:
                vmpool[ip]=[]
                vmpool[ip].append(vm.UUIDString())
            return vm.UUIDString()
        except Exception,e:
            print "cannot connect to %s" %(ip)
            return None

#----------------------------------------------------------------------
#shutdown a VM
def shutdownVM(uuid):
    """"""
    try:
        conn=connectionpool[vmmap[uuid]]
        vm=conn.lookupByUUIDString(uuid)
        vm.shutdown()
        return True
    except Exception,e:
        print "VM shutdown fail! %e" %e
#----------------------------------------------------------------------
#suspend an inactive domain(cut CPU I/O resource),process frozen but memory stay allocated
#vm state changed to 3(domain paused by user)
def suspendVM(uuid):
    """"""
    try:
        conn=connectionpool[vmmap[uuid]]
        vm=conn.lookupByUUIDString(uuid)
        vm.suspend()
        return True
    except Exception,e:
        print "VM suspend fail! %s" %e

#----------------------------------------------------------------------
#resume a suspended domain,vm state changed to 1(running)
def resumeVM():
    """"""
    try:
        conn=connectionpool[vmmap[uuid]]
        vm=conn.lookupByUUIDString(uuid)
        vm.resume()
        return True
    except Exception,e:
        print "VM resume fail! %s" %e
    
#----------------------------------------------------------------------
#
def rebootVM():
    """"""
    try:
        conn=connectionpool[vmmap[uuid]]
        vm=conn.lookupByUUIDString(uuid)
        vm.reboot(0)
        return True
    except Exception,e:
        print "VM reboot fail!%s" %e
    
#----------------------------------------------------------------------
#
def destoryVM():
    """"""
    try:
        conn=connectionpool[vmmap[uuid]]
        vm=conn.lookupByUUIDString(uuid)
        vm.destory()
        return True
    except Exception,e:
        print "VM reboot fail!%s" %e
        
#----------------------------------------------------------------------
#
def queryVM(uuid):
    """"""
    
#----------------------------------------------------------------------
def getConfig():
    """"""
    ret=""
    for key in config.keys():
        ret=ret+"virtual machine template:"+key+"\n"+config[key]+"\n"
    return ret
        