#!/usr/bin/python
#module:virtual machine controller based on libvirt
#author:Yuwenhao
#date:13-1-10

import libvirt
import os
import json

#"ip":['uuid1','uuid2']
vmpool={}
#"uuid":"host ip"
vmmap={}
#virtual machine state
vmstate=["none","Running","Blocked","Paused","ShutingDown","Shutoff","crashed","Suspended"]

config={}
fd=open("/home/achilles/docs/config/Windows2k8.xml","r")
lines=fd.readlines()
ss=""
for line in lines:
    ss=ss+line

config["Windows2k8"]=ss

#----------------------------------------------------------------------
#create vm on a host.
def createVM(name):
    """"""
    try:
        global vmmap,vmpool,config
        ip="127.0.0.1"
        param="qemu+ssh://root@"+ip+"/system"
        conn=libvirt.open(param)
        vm=conn.createLinux(config["Windows2k8"],0)
        #add to list
        vmmap[vm.UUIDString()]=ip
        if(vmpool.has_key(ip)):
            vmpool[ip].append(vm.UUIDString())
        else:
            vmpool[ip]=[]
            vmpool[ip].append(vm.UUIDString())
        conn.close()
        return vm.UUIDString()
    except Exception,e:
        print "cannot connect to %s" %(ip)
        return None

#----------------------------------------------------------------------
#shutdown a VM
def shutdownVM(uuid):
    """"""
    try:
        global vmmap,vmpool
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.shutdown()
        conn.close()
        return True
    except Exception,e:
        print "VM shutdown fail! %s" %e
        return False
#----------------------------------------------------------------------
#suspend an inactive domain(cut CPU I/O resource),process frozen but memory stay allocated
#vm state changed to 3(domain paused by user)
def suspendVM(uuid):
    try:
        global vmmap,vmpool
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        print vm.UUIDString()
        vm.suspend()
        return True
    except Exception,e:
        print "VM suspend fail! %s" %e
        return False

#----------------------------------------------------------------------
#resume a suspended domain,vm state changed to 1(running)
def resumeVM(uuid):
    """"""
    try:
        global vmmap,vmpool
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.resume()
        return True
    except Exception,e:
        print "VM resume fail! %s" %e
        return False
#----------------------------------------------------------------------
#
def rebootVM(uuid):
    """"""
    try:
        global vmmap,vmpool
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.reboot(0)
        return True
    except Exception,e:
        print "VM reboot fail!%s" %e
        return False
    
#----------------------------------------------------------------------
#
def destoryVM(uuid):
    """"""
    try:
        global vmmap,vmpool
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.destory()
        return True
    except Exception,e:
        print "VM destory fail!%s" %e
        return False
#----------------------------------------------------------------------
#
def queryVM(uuid,req_format):
    """"""
    ret_dict={}
    try:
        global vmmap,vmpool,vmstate
        url="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(url)
        vm=conn.lookupByUUIDString(uuid)
        ret_dict["info"]=vm.info()
        ret_dict["name"]=vm.name()
        ret_dict["UUID"]=uuid
        ret_dict["host"]={'name':conn.getHostname(),'ip':vmmap[uuid]}
        #return data
        if req_format=="json":
            return json.dumps(ret_dict)
        elif req_format=="text":
            ret=""
            ret=ret+"UUID       : "+ret_dict["UUID"]+"\n"
            ret=ret+"name       : "+ret_dict["name"]+"\n"
            ret=ret+"state      : "+vmstate[int(ret_dict["info"][0])]+"\n"
            ret=ret+"MaxMem     : "+str(ret_dict["info"][1])+"KB\n"
            ret=ret+"UsedMen    : "+str(ret_dict["info"][2])+"KB\n"
            ret=ret+"vCpu num   : "+str(ret_dict["info"][3])+"\n"
            ret=ret+"hostname   : "+ret_dict["host"]["name"]+"\n"
            ret=ret+"hostip     : "+ret_dict["host"]["ip"]+"\n\n"
            return ret
    except Exception,e:
        error="VM query fail!%s" %e
        return error
#----------------------------------------------------------------------
def getConfig():
    """"""
    ret=""
    for key in config.keys():
        ret=ret+"virtual machine template:"+key+"\n"+config[key]+"\n"
    return ret
        