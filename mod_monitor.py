
#----------------------------------------------------------------------
#select a host for new vm
def selectHostIP(vmpool):
    """"""
    for key in vmpool.keys():
        if len(vmpool[key])<3:
            return key