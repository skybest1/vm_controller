import urlparse
import libvirt
import json
#shutdownFlags(0) shutdown ASAP

conn=libvirt.open("qemu:///system")
#vm=conn.createLinux(mod_vm.config["Windows2k8"],0)
#print vm.UUIDString()
ss={"1":['1','2']}
print ss
del ss['1']
print ss