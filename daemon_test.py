import urlparse
import urllib2


result=urlparse.urlparse("http://www.baidu.com/s?tn=baiduhome_pg&ie=utf-8&bs=python+if+else&f=8&rsv_bp=1&rsv_spt=1&wd=python+else+if&rsv_sug3=13&rsv_sug=0&rsv_sug1=8&rsv_sug4=607&inputT=2700")
params=urlparse.parse_qs(result.query,True)
print params['wd']
