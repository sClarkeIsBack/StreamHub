import os,xbmc

addon_id   = 'plugin.video.livehub'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))

def home():
	addDir('[COLOR red][B]BETA - Please Report All Problems To facebook.com/groups/streamh[/COLOR][/B]','url',0,icon,fanart,'')
	addDir('[COLOR white][B][/COLOR][/B]','url',0,icon,fanart,'')
	addDir('[COLOR white][B]UK Geo Locked[/COLOR][/B]','url',1000,icon,fanart,'')
	addDir('[COLOR white][B]Web Scrapers[/COLOR][/B]','url',2000,icon,fanart,'')
	addDir('[COLOR white][B]IPTV Scrapers[/COLOR][/B]','url',3000,icon,fanart,'')
	addDir('[COLOR white][B]Android API[/COLOR][/B]','url',4000,icon,fanart,'')
	
def play(url,name,pdialogue=None):
		from resources.modules import resolvers
		import xbmcgui
		
		url = url.strip()

		url = resolvers.resolve(url)
		if url == 'False':xbmcgui.Dialog().notification('A','This Link is Down, Try Another')
		if url.endswith('m3u8'):
			from resources.root import iptv
			iptv.listm3u(url)
		else:
				
			liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
			liz.setInfo(type='Video', infoLabels={'Title':name})
			liz.setProperty("IsPlayable","true")
			liz.setPath(url)

			if url.lower().startswith('plugin') and 'youtube' not in  url.lower():
				xbmc.executebuiltin('XBMC.PlayMedia('+url+')') 
				for i in range(8):
					xbmc.sleep(500) ##sleep for 10 seconds, half each time
					try:
						#print 'condi'
						if xbmc.getCondVisibility("Player.HasMedia") and xbmc.Player().isPlaying():
							return True
					except: pass
				print 'returning now'
				return False
			elif url.endswith('.ts'):
				playf4m(url,name)
				from resources.modules import  CustomPlayer
				import time

				player = CustomPlayer.MyXBMCPlayer()
				if (xbmc.Player().isPlaying() == 0):
					quit()
				try:
				   
						if player.urlplayed:
							print 'yes played'
							return
						if time.time()-beforestart>4: return False
					#xbmc.sleep(1000)
				except: pass

				print 'returning now'
				return False
			from resources.modules import  CustomPlayer
			import time

			player = CustomPlayer.MyXBMCPlayer()
			player.pdialogue=pdialogue
			start = time.time() 
			#xbmc.Player().play( liveLink,listitem)
			print 'going to play'
			import time
			beforestart=time.time()
			player.play( url, liz)
			if (xbmc.Player().isPlaying() == 0):
				quit()
			try:
				while player.is_active:
					xbmc.sleep(400)
				   
					if player.urlplayed:
						print 'yes played'
						return
					if time.time()-beforestart>4: return False
					#xbmc.sleep(1000)
			except: pass
			print 'not played',url
			xbmc.Player().stop()
			return
		
		
def playf4m(url, name):
                import urlparse,json
                if not any(i in url for i in ['.f4m', '.ts', '.m3u8']): raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if not ext: ext = url
                if not ext in ['f4m', 'ts', 'm3u8']: raise Exception()

                params = urlparse.parse_qs(url)

                try: proxy = params['proxy'][0]
                except: proxy = None

                try: proxy_use_chunks = json.loads(params['proxy_for_chunks'][0])
                except: proxy_use_chunks = True

                try: maxbitrate = int(params['maxbitrate'][0])
                except: maxbitrate = 0

                try: simpleDownloader = json.loads(params['simpledownloader'][0])
                except: simpleDownloader = False

                try: auth_string = params['auth'][0]
                except: auth_string = ''


                try:
                   streamtype = params['streamtype'][0]
                except:
                   if ext =='ts': streamtype = 'TSDOWNLOADER'
                   elif ext =='m3u8': streamtype = 'HLS'
                   else: streamtype = 'HDS'

                try: swf = params['swf'][0]
                except: swf = None

                from F4mProxy import f4mProxyHelper
                return f4mProxyHelper().playF4mLink(url, name, proxy, proxy_use_chunks, maxbitrate, simpleDownloader, auth_string, streamtype, False, swf)
		
def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
	

		
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
	import re
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r





def addDir(name,url,mode,iconimage,fanart,description):
	import xbmcgui,xbmcplugin,urllib,sys
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==87:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory


def OPEN_URL(url):
	import requests
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
	
	

	
	
	

	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)

import urllib

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
	home()

elif mode==1:
	from resources.root import ukgeo
	ukgeo.get(url)
	
	
elif mode==2:
	from resources.root import webscrapers
	webscrapers.get(url)
	
	
elif mode==3:
	from resources.root import iptv
	iptv.get(url)
	
elif mode==4:
	from resources.root import android
	android.get(url)
	
	
elif mode==50:
	from resources.root import iptv
	iptv.listm3u(url)
	

	
elif mode==10:
	play(url,name)
	


elif mode==1000:
	from resources.root import ukgeo
	ukgeo.cat()
	
elif mode==2000:
	from resources.root import webscrapers
	webscrapers.cat()

elif mode==3000:
	from resources.root import iptv
	iptv.cat()
	
elif mode==4000:
	from resources.root import android
	android.cat()
	
elif mode==9999:
	import xbmcgui,xbmcplugin
	from resources.modules import resolvers
	url = resolvers.resolve(url)
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels='')
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	

import xbmcplugin
xbmcplugin.endOfDirectory(int(sys.argv[1]))