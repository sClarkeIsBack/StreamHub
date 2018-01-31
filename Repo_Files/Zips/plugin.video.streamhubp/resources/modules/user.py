import base64 as b
import xbmcaddon

id   = b.b64decode('cGx1Z2luLnZpZGVvLnN0cmVhbWh1YnA=')

name = b.b64decode('W0NPTE9SIGZmZmYwMDAwXVtCXVN0cmVhbUh1YlsvQ09MT1JdW0NPTE9SIGdvbGRdIFByZW1pdW1bL0NPTE9SXVsvQl0=')

port = b.b64decode('ODA=')

def host():
	if xbmcaddon.Addon().getSetting('direct') == 'true':
		url = b.b64decode('aHR0cDovL3N0cmVhbWh1YnByZW1pdW0uY28udWs=')
	else:
		url = b.b64decode('aHR0cDovL2RpcmVjdC5zdHJlYW1odWJwcmVtaXVtLmNvLnVr')
	return url