#!/usr/bin/python
#module:virtual machine controller based on libvirt
#author:Yuwenhao
#date:13-1-10

import libvirt
import os
import json
import time
import mod_config
import mod_monitor
#"ip":['uuid1','uuid2']
vmpool={}
#"uuid":"host ip"
vmmap={}
#virtual machine state
vmstate=["none","Running","Blocked","Paused","ShutingDown","Shutoff","crashed","Suspended"]
#name:xml config
config={}
#module information
mod_info={}
#error log:cannnot use mod_log=open(...) here!!!
mod_log=1

#----------------------------------------------------------------------
#module init
def mod_init():
    """"""
    try:
        global config,mod_log,vmpool
        mod_log=open("/home/achilles/workspace/PythonTest/log/modlog.log","a+")
        mod_info["time"]=time.ctime()
        mod_info["PID"]=str(os.getpid())
        config["Windows2k8"]=mod_config.getTemplate()
        
        ip_list=[]
        mod_config.getIPAddress(ip_list)
        #add host
        for ip in ip_list:
            vmpool[ip]=[]
        mod_log.write(time.ctime()+" Info "+"module init OK!\n")
        mod_log.flush()
    except Exception, e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
#----------------------------------------------------------------------
#get the running info of the module
def queryModInfo():
    try:
        ret=""
        ret=ret+"server start from "+mod_info["time"]+"...\n"
        ret=ret+"PID: "+mod_info["PID"]+"\n"
        ret=ret+"Virtual Machine number:"+str(len(vmmap.keys()))+"\n"
        ret=ret+"Host     <====>   VM\n\n"
        for key in vmpool.keys():
            ret=ret+key+"<====>  "+str(vmpool[key])+"\n"
        return ret
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return "query info error!%s" %e
#----------------------------------------------------------------------
#create vm on a host.
def createVM(name):
    """"""
    try:
        global vmmap,vmpool,config,mod_log
        #should select a host ip!
        ip=mod_monitor.selectHostIP(vmpool)
        #ip="127.0.0.1"
        param="qemu+ssh://root@"+ip+"/system"
        conn=libvirt.open(param)
        vmconfig=mod_config.setName(config['Windows2k8'],name)
        vm=conn.createLinux(vmconfig,0)
        #add to list
        vmmap[vm.UUIDString()]=ip
        if(vmpool.has_key(ip)):
            vmpool[ip].append(vm.UUIDString())
        else:
            vmpool[ip]=[]
            vmpool[ip].append(vm.UUIDString())
        conn.close()
        #log
        mod_log.write(time.ctime()+" Info "+"create vm on host:"+ip+"\n")
        mod_log.flush()
        return vm.UUIDString()
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return None

#----------------------------------------------------------------------
#shutdown a VM
def shutdownVM(uuid):
    """"""
    try:
        global vmmap,vmpool,mod_log
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.shutdownFlags(0)
        host_ip=vmmap[uuid]
        del vmmap[uuid]
        vmpool[host_ip].remove(uuid)
        conn.close()
        mod_log.write(time.ctime()+" Info "+"vm:"+uuid+" shut down...\n")
        mod_log.flush()
        return 1
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return 0
#----------------------------------------------------------------------
#suspend an inactive domain(cut CPU I/O resource),process frozen but memory stay allocated
#vm state changed to 3(domain paused by user)
def suspendVM(uuid):
    try:
        global vmmap,vmpool,mod_log
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        print vm.UUIDString()
        vm.suspend()
        conn.close()
        mod_log.write(time.ctime()+" Info "+"vm:"+uuid+" paused...\n")
        mod_log.flush()
        return 1
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return 0

#----------------------------------------------------------------------
#resume a suspended domain,vm state changed to 1(running)
def resumeVM(uuid):
    """"""
    try:
        global vmmap,vmpool,mod_log
        param="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(param)
        vm=conn.lookupByUUIDString(uuid)
        vm.resume()
        conn.close()
        mod_log.write(time.ctime()+" Info "+"vm:"+uuid+" resumed...\n")
        mod_log.flush()
        return 1
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return 0
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
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
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
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return False
#----------------------------------------------------------------------
#
def queryVM(uuid,req_format):
    """"""
    ret_dict={}
    try:
        global vmmap,vmpool,vmstate,mod_log
        url="qemu+ssh://root@"+vmmap[uuid]+"/system"
        conn=libvirt.open(url)
        vm=conn.lookupByUUIDString(uuid)
        ret_dict["info"]=vm.info()
        ret_dict["name"]=vm.name()
        ret_dict["UUID"]=uuid
        ret_dict["host"]={'name':conn.getHostname(),'ip':vmmap[uuid],'type':conn.getType()}
        #return data
        if req_format=="json":
            return json.dumps(ret_dict)
        elif req_format=="text":
            ret=""
            ret=ret+"UUID       : "+ret_dict["UUID"]+"\n"
            ret=ret+"name       : "+ret_dict["name"]+"\n"
            ret=ret+"state      : "+vmstate[int(ret_dict["info"][0])]+"\n"
            ret=ret+"MaxMem     : "+str(ret_dict["info"][1])+"KB\n"
            ret=ret+"UsedMem    : "+str(ret_dict["info"][2])+"KB\n"
            ret=ret+"vCpu num   : "+str(ret_dict["info"][3])+"\n"
            ret=ret+"Hostname   : "+ret_dict["host"]["name"]+"\n"
            ret=ret+"Hostip     : "+ret_dict["host"]["ip"]+"\n"
            ret=ret+"Driver     : "+ret_dict["host"]["type"]+"\n"
            return ret
    except Exception,e:
        mod_log.write(time.ctime()+" Error "+e+"\n")
        mod_log.flush()
        return error
#----------------------------------------------------------------------
def getConfig():
    """"""
    ret=""
    for key in config.keys():
        ret=ret+"virtual machine template:"+key+"\n"+config[key]+"\n"
    return ret
        