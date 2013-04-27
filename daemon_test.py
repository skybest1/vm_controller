import os,sys
import libvirt
import mod_vm
import mod_config

mod_vm.mod_init()
conn=libvirt.open("qemu:///system")
vmconfig=mod_config.setName(mod_vm.config["Windows2k8"],"testname hello")
print vmconfig
dom=conn.createLinux(vmconfig,0)
