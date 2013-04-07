#!/usr/bin/python
import libvirt
import os
import sys
import time

conn = libvirt.open('qemu+ssh://root@127.0.0.1/system')
f1=open("/home/achilles/docs/config/Windows2k8.xml")
lines=f1.readlines()
xmlconfig=""
for line in lines:
    xmlconfig=xmlconfig+line
print "Connection Complete!"
#create virtual machine
dom=conn.createLinux(xmlconfig,0)
for dom in conn.listAllDomains(0):
    print dom.getCPUStats(1,0)
#print "VM Created! %s" %dom.UUIDString()
print conn.getInfo()


