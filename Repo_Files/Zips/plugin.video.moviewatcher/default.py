import os,re,requests,string,sys,urllib,urllib2,urlresolver
import xbmc,xbmcaddon,xbmcgui,xbmcplugin


addon_id   = 'plugin.video.moviewatcher'
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

base_url   = 'http://moviewatcher.io'
search_url = 'http://moviewatcher.io/search?query='



def CAT():
	addDir('Most Popular',base_url+'/most-popular-movies',1,icon,fanart,'')
	addDir('New Movies',base_url+'/new-published-movies',1,icon,fanart,'')
	addDir('Genres',base_url,2,icon,fanart,'')
	addDir('Years',base_url,3,icon,fanart,'')
	addDir('Search',base_url,6,icon,fanart,'')
	addDir('TV Shows',base_url+'/tv-series',1,icon,fanart,'')
	
	
def INDEX(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<div class="one_movie-item">','							</div>')
	for a in all:
		name = regex_from_to(a,'alt="','"')
		url  = regex_from_to(a,'a href="','"')
		thumb= regex_from_to(a,'img src="','"')
		ratin= regex_from_to(a,'"IMDB Rating">','<')
		genre= regex_from_to(a,'<hr>','<hr>')
		desc = regex_from_to(a,'"movie-text">','<')
		if '<div class="movie-series">' in a:
			desc = 'tvshow'
		addDir(name,base_url+url,4,base_url+thumb,fanart,desc)
		
	try:
		np = regex_from_to(open,'<link rel="next" href="','"')
		if np =='':raise Exception()
		addDir('[COLOR red]NEXT PAGE>[/COLOR]',np,1,icon,fanart,'')
	except:
		pass
		
def GENRE(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'onclick="return false">GENRES</a>','</div>')
	all  = regex_get_all(part,'<li>','</li>')
	for a in all:
		url  = regex_from_to(a,'href="','"')
		name = regex_from_to(a,'">','<')
		addDir(name,base_url+url,1,icon,fanart,'')
		
def YEARS(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'onclick="return false">YEARS</a>','</div>')
	all  = regex_get_all(part,'<li>','</li>')
	for a in all:
		url  = regex_from_to(a,'href="','"')
		name = regex_from_to(a,'">','<')
		addDir(name,base_url+url,1,icon,fanart,'')
		

		
def LINKS(url,description):
	if base_url not in url:
		url = base_url+url
	open     = OPEN_URL(url)#
	if description == 'tvshow':
		all = regex_get_all(open,'<a class="episode_1 episode episode_series_link"','</a>')
		for a in all:
			url = regex_from_to(a,'href="','"')
			name= regex_from_to(a,'title="','"')
			season = regex_from_to(url,'/s','e')
			addDir(name +' - Season '+ season,base_url+url,4,icon,fanart,'')
	else:
		links    = regex_get_all(open,'<a class="full-torrent1" rel="nofollow">','</a>')
		for a in links:
			url  = regex_from_to(a,'<div onclick="','"')
			url  = base_url+str(url).replace("window.open('","").replace("')","")
			xbmc.log(str(url))
			name = regex_from_to(a,'Stream server: ','<')
			addDir(name,url,5,icon,fanart,'')
			xbmc.log(str(url))
		
def SEARCH():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Search Query') # optional
	kb.setHiddenInput(False) # optional
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		text = str(text).replace(' ','+')
		url  = search_url+text
		open = OPEN_URL(url)
		all  = regex_get_all(open,'<div class="one_movie-item">','							</div>')
		for a in all:
			name = regex_from_to(a,'alt="','"')
			url  = regex_from_to(a,'a href="','"')
			thumb= regex_from_to(a,'img src="','"')
			ratin= regex_from_to(a,'"IMDB Rating">','<')
			genre= regex_from_to(a,'<hr>','<hr>')
			desc = regex_from_to(a,'"movie-text">','<')
			if '<div class="movie-series">' in a:
				desc = 'tvshow'
			addDir(name,base_url+url,4,base_url+thumb,fanart,desc)
		
def RESOLVE(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = requests.get(url, headers=headers, verify=False,allow_redirects=True)
	link = link.url
	xbmc.log(str(link))
	link = urlresolver.HostedMediaFile(link).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title':description})
	liz.setProperty("IsPlayable","true")
	liz.setPath(str(link))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	

	
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==5:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r
	
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
	CAT()

elif mode==1:
	INDEX(url)
	
elif mode==2:
	GENRE(url)
	
elif mode==3:
	YEARS(url)
	
elif mode==4:
	LINKS(url,description)
	
elif mode==5:
	RESOLVE(url)
	
elif mode==6:
	SEARCH()
xbmcplugin.endOfDirectory(int(sys.argv[1]))