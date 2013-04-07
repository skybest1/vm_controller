import urlparse
import urllib
url="length=123&name=virtual+machine+name"

print urlparse.parse_qs("length=123&name=virtual+machine+name",True)