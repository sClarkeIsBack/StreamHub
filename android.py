import xbmc,os

#############################EDITED#########################################

addon_id   = 'plugin.video.livehub'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

def cat():
	addDir('[COLOR white][B]Mobdro[/COLOR][/B]','mobdro',4,'http://apk.co/images/mobdro-2014-freemium.png',fanart,'')
	addDir('[COLOR white][B]Swift Streams[/COLOR][/B]','snappystreams',4,'https://image.winudf.com/v2/image/Y29tLnN3aWZ0LnN0cmVhbV9zcmNqdHBicg/icon.png?w=170&fakeurl=1&type=.png',fanart,'')

def get(url):
	if url == 'sourceetv':
		sourcetv()
	elif url == 'snappystreams':
		snappystreams()
	elif 'SnappyStreamz/api.php?cat_id=' in url:
		snappystreamschans(url)
	elif url == 'mobdro':
		mobdro()
	elif url == 'livetv':
		livetv()
		
		
def livetv():
	import re
	open = OPEN_URL('http://163.172.89.151:25461/get.php?username=iptvrestream.net&password=wC5Qtu9Zbl&type=m3u&output=ts')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir(name,url,10,icon,fanart,'')
		
		
def mobdro():
        import re
        file = xbmc.translatePath('special://home/addons/plugin.video.livehub/resources/')
        if os.path.exists(file):
            file = open(os.path.join(file, 'mobdrochans.txt'))
            data = file.read()
            file.close()
			
            all   = re.compile('\n([^:]+):(mpd://[^\n]+)').findall(data)
            for name,url in all:
				addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,'http://geekpeaksoftware.com/wp-content/uploads/2016/10/mobdro.png',fanart,'')
				

		
def snappystreams():
	import json,requests
	url = 'http://173.212.202.101/SnappyStreamz/api.php'
	
	headers = {'Authorization': 'Basic U25hcHB5OkBTbmFwcHlA',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['category_name']
		id   = a['cid']
		icon = a['category_image']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'http://173.212.202.101/SnappyStreamz/api.php?cat_id='+id,4,'http://swiftstreamz.com/SwiftStream/images/thumbs' + icon,fanart,'')
		
		
def snappystreamschans(url):
	import json,requests

	headers = {'Authorization': 'Basic U25hcHB5OkBTbmFwcHlA',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['channel_title']
		url  = a['channel_url']
		icon = a['channel_thumbnail']
		desc = a['channel_desc']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'snappystreams:'+url,10,'http://swiftstreamz.com/SwiftStream/images/thumbs/' + icon,fanart,desc)
		
######################################################################################################
		
		
		
def regex_from_to(text, from_string, to_string, excluding=True):
	import re,string
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	import re,string
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r



def OPEN_URL(url):
	import requests
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
logfile    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.livehub', 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	

		
		
def addDir(name,url,mode,iconimage,fanart,description):
	import xbmcgui,xbmcplugin,urllib,sys
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==102:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
