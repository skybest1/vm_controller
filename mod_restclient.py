#!/usr/bin/env python
#coding:utf-8
# Author: Yuwenhao--<skybest1_zju@163.com>
# Purpose: virtual machine controller based on libvirt
# Created: 2013年01月13日

import httplib
import urllib
import hashlib
import json

#----------------------------------------------------------------------
#return access-token of a request.private key is needed.
def accessToken(params,private_key):
    """"""
    data=""
    keys=params.keys()
    keys.sort()
    for key in keys:
        data=data+key
        data=data+str(params[key])
    data=data+private_key
    hash_new=hashlib.sha1()
    hash_new.update(data)
    hash_value=hash_new.hexdigest()
    return hash_value

#----------------------------------------------------------------------
def createVM_rest():
    """"""
    
    pass


#----------------------------------------------------------------------
def shutdownVM_rest():
    """"""
    pass

#----------------------------------------------------------------------
def suspendVM_rest():
    """"""
    pass

#----------------------------------------------------------------------
def queryVM():
    """"""
    
