import os,re,requests,string,sys,urllib,urllib2,urlresolver
import xbmc,xbmcaddon,xbmcgui,xbmcplugin


addon_id   = 'plugin.video.kohi'
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

base_url   = 'http://kohimovie.info'
search_url = 'http://kohimovie.info/search?q='
link_info  = 'http://webapp.bobbyhd.com/player.php?alias='



def CAT():
	addDir('Most Popular',base_url+'/popular',1,icon,fanart,'')
	addDir('Trending',base_url+'/trending',1,icon,fanart,'')
	addDir('Genres',base_url,3,icon,fanart,'')
	addDir('By Year',base_url,4,icon,fanart,'')
	addDir('Search',base_url,5,icon,fanart,'')
	addDir('Episodes',base_url+'/tvshows',1,icon,fanart,'')
	
def INDEX(url):
	open = OPEN_URL(url)
	all_vids = regex_get_all(open,'<article id="','</article>')
	for a in all_vids:
		name = regex_from_to(a,'alt="','"')
		url  = regex_from_to(a,'watch/movie-online-','"')
		if url == "":
			url = regex_from_to(a,'watch/tvshow-online-','"')
		thumb= regex_from_to(a,'src="','"')
		qual = regex_from_to(a,'25px;">','<')
		rat  = regex_from_to(a,'<span class="icon-star2"></span>','	')
		rat  = str(rat).replace('0','')
		addDir(name+'  [COLOR red]%s[/COLOR]  [B]%s[/B]'%(qual,rat),url,2,thumb,fanart,'')
	try:
		part = regex_from_to(open,"<div class='resppages'>","<span")
		np = regex_from_to(part,'<a href="','"')
		addDir('[COLOR red]NEXT PAGE>[/COLOR]',np,1,icon,fanart,'')
	except:
		pass

	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(500)")
		
def GENRES(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'"li-text">Genres</span>','<div class="clearfix">')
	all  = regex_get_all(part,'<li>','</li>')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'a href="','"')
		addDir(name,url,1,icon,fanart,'')
		
def YEARS(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'<ul class="year scrolling">','<div class="sidemenu">')
	all  = regex_get_all(part,'<li>','</li>')
	for a in all:
		name = regex_from_to(a,'">','<')
		url  = regex_from_to(a,'a href="','"')
		addDir(name,url,1,icon,fanart,'')
		
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
		all_vids = regex_get_all(open,'<article id="','</article>')
		for a in all_vids:
			name = regex_from_to(a,'alt="','"')
			url  = regex_from_to(a,'watch/movie-online-','"')
			thumb= regex_from_to(a,'src="','"')
			qual = regex_from_to(a,'25px;">','<')
			addDir(name+'  [COLOR red]%s[/COLOR]'%qual,url,2,thumb,fanart,'')
			xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			xbmc.executebuiltin("Container.SetViewMode(500)")
		
def RESOLVE(url):
	url = link_info+url
	open = OPEN_URLH(url)
	link = re.compile("changevideo\(\'(.+?)\'\)").findall(open)
	link = str(link).replace("['","").replace("']","")
	play = CHECKLINK(link)
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(play)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def CHECKLINK(link):
	if 'ganoolmovies' in link:
		open = OPEN_URL(link)
		link = regex_from_to(open,'file: "','"')
	elif 'openload' in link:
		link = urlresolver.resolve(link)
	elif 'google' in link:
		link = urlresolver.resolve(link)
	return link
	

	
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==2:
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
	
def OPEN_URLH(url):
	headers={'Host':'webapp.bobbyhd.com',
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
					'Accept-Language':'en-gb',
					'Accept-Encoding':'gzip, deflate',
					'Connection':'keep-alive'}

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
	RESOLVE(url)
	
elif mode==3:
	GENRES(url)
	
elif mode==4:
	YEARS(url)
	
elif mode==5:
	SEARCH()
xbmcplugin.endOfDirectory(int(sys.argv[1]))