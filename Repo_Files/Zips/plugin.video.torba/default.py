import os,re,sys,json,string,urllib,requests,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

from resources.modules import client,trailer



addon_id   = 'plugin.video.torba'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

base_url   = 'https://torba.se'

def CAT():
	addDir('[COLOR white][B][CAPITALIZE]Movies[/B][/CAPITALIZE][/COLOR]','url',1,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Tv Series[/B][/CAPITALIZE][/COLOR]','url',2,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Search[/B][/CAPITALIZE][/COLOR]','url',99,icon,fanart,'')
	
	
def MOVIECAT():
	addDir('[COLOR white][B][CAPITALIZE]Recently Added[/B][/CAPITALIZE][/COLOR]',base_url+'/search',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Favourite[/B][/CAPITALIZE][/COLOR]',base_url+'/search?order=favorites',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Popular[/B][/CAPITALIZE][/COLOR]',base_url+'/search?order=views',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Collections[/B][/CAPITALIZE][/COLOR]','url',10,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Rated[/B][/CAPITALIZE][/COLOR]',base_url+'/search?order=rating',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Country[/B][/CAPITALIZE][/COLOR]',base_url+'/search',12,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Genres[/B][/CAPITALIZE][/COLOR]',base_url+'/search',8,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Qaulity[/B][/CAPITALIZE][/COLOR]',base_url+'/search',13,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Year[/B][/CAPITALIZE][/COLOR]',base_url+'/search',11,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Search[/B][/CAPITALIZE][/COLOR]',base_url+'/search?title=%s&order=views',9,icon,fanart,'')
	
def TVCAT():
	addDir('[COLOR white][B][CAPITALIZE]Recently Added[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=recent',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Followed[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=followed',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Popular[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=views',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Rated[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=rating',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Country[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search',12,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Qaulity[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search',13,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Genres[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search',8,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Latest[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=year',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Year[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search',11,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]A-Z[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?order=name',4,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Search[/B][/CAPITALIZE][/COLOR]',base_url+'/series/search?title=%s&order=views',9,icon,fanart,'')
	
def COLLECTIONSCAT():
	addDir('[COLOR white][B][CAPITALIZE]Aliens[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/aliens',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Assassins[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/about-contract-killers-and-assassins',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Best of 2015[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/best-of-2015',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Best of 2016[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/best-of-2016-in-hd',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Comics[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/comics',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Descent into Madness[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/about-descent-into-madness',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Distopian[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/distopian-films',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Horrors You Will Never Wacth Again[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/disturbing-horror-movies-you-will-never-watch-again',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Human Experiments[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/about-human-experiments',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Master Peices[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/cinematic-masterpieces',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Most Extreme[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/most-extreme',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Paris[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/paris',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Psychological Thrillers[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/psychological-thrillers',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Relax & Enjoy[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/just-relax-and-enjoy',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Sci-fi[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/sci-fi',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Soul Crashing[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/soul-crashing',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Super Hero[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/superheores',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Super Natural[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/supernatural',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Survival[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/survival',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]The Future[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/future',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Vampires[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/vampires',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Visually Stunning[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/visually-stunning',3,icon,fanart,'')
	addDir('[COLOR white][B][CAPITALIZE]Worst Movies of 2016[/B][/CAPITALIZE][/COLOR]',base_url+'/collection/worst-movies-of-2016',3,icon,fanart,'')
	
	
	

def INDEX(url):
	try:
		open = OPEN_URL(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	all  = regex_get_all(open,'<div class="films-item-image">','div class="films-item-image-block">')
	for a in all:
		name = regex_from_to(a,'films-item-title"><span>','</span>').replace('&#039;',"'")
		url  = regex_from_to(a,'a href="','"')
		icon = regex_from_to(a,'img src="','"')
		addDir('[COLOR white][B][CAPITALIZE]%s[/B][/CAPITALIZE][/COLOR]'%name,base_url+url,7,base_url+icon,fanart,'')
	try:
		np = regex_from_to(open,'<li class="next"><a href="','"').replace('&amp;','&')
		addDir('[COLOR yellow][B][CAPITALIZE]NEXT PAGE >[/B][/CAPITALIZE][/COLOR]',urllib.quote_plus(base_url+np),3,icon,fanart,'')
	except:
		pass
		
		
def TVINDEX(url):
	try:
		open = OPEN_URL(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	all  = regex_get_all(open,'div class="tv-show">','<div class="clearfix">')
	for a in all:
		url  = regex_from_to(a,'<a href="','"')
		fanart = regex_from_to(a,'background-image:','"').replace('url(',base_url).replace(')','')
		name = regex_from_to(a,'<span class="tv-show-title">','</span>')
		name = regex_from_to(name,'">','<').replace('&#039;',"'")
		addDir('[COLOR white][B][CAPITALIZE]%s[/B][/CAPITALIZE][/COLOR]'%name,base_url+url,5,fanart,fanart,regex_from_to(name,'^','[0-9]').replace('(',''))
	try:
		np = regex_from_to(open,'<li class="next"><a href="','"').replace('&amp;','&')
		addDir('[COLOR lime]NEXT PAGE >[/B][/CAPITALIZE][/COLOR]'%name,urllib.quote_plus(base_url+np),3,icon,fanart,'')
	except:
		pass
		
def TVSEASONS(url,description):
	try:
		open = OPEN_URL(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	part  = regex_from_to(open,'<div class="season-change">','</div>')
	all  = regex_get_all(part,'a href','</li>')
	for a in all:
		url  = regex_from_to(a,'="','"')
		name = regex_from_to(a,'">','<').replace('&#039;',"'")
		name = '%s | %s'%(description,name)
		addDir('[COLOR white][B][CAPITALIZE]%s[/B][/CAPITALIZE][/COLOR]'%name,base_url+url,6,base_url+icon,fanart,name)
		
def TVEPISODES(url,description):
	try:
		open = OPEN_URL(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	part = regex_from_to(open,'</a>    </div>','</html>')
	all  = regex_get_all(part,'<li class="episode-item"','</div></li>')
	for a in all:
		name = regex_from_to(a,'title">','<').replace('&#039;',"'")
		name = '%s | %s'%(description,name)
		url = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		addDir('[COLOR white][B][CAPITALIZE]%s[/B][/CAPITALIZE][/COLOR]'%name,base_url+url,7,icon,fanart,'')
		
		
def GENRE(url):
	if '/series/' in url:
		mode = '4'
		temp = '%s/series/search?order=views&genre=%s'
	else:
		mode = '3'
		temp = '%s/search?order=views&genre=%s'
	open = OPEN_URL(url)
	part = regex_from_to(open,'<div id="dropdown-id-genre"','<div id="dropdown-id-year"')
	all  = regex_get_all(part,'<li class="dropdown-item">','</a></li>')
	for a in all:
		name = regex_from_to(a,'dropdown-id-genre">','<').replace('&#039;',"'")
		url  = regex_from_to(a,'data-text="','"')
		url  = temp%(base_url,url)
		if not 'All genres' in name:
			if not 'N/A' in name:
				if not '</a>' in name:
					addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus(url),mode,icon,fanart,'')
		
		
def YEAR(url):
	if '/series/' in url:
		mode = '4'
		temp = base_url+'/series/search?order=views&year='
	else:
		mode = '3'
		temp = base_url+'/search?order=views&year='
	open = OPEN_URL(url)
	part = regex_from_to(open,'dropdown-id-year">All years</a>','</li></ul>')
	all  = regex_get_all(part,'<a data','</a>')
	for a in all:
		name = regex_from_to(a,'year">','<')
		url  = regex_from_to(a,'text="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus(temp+url),mode,icon,fanart,'')
		
		
def COUNTRY(url):
	if '/series/' in url:
		mode = '4'
		temp = base_url+'/series/search?order=views&country[]='
	else:
		mode = '3'
		temp = base_url+'/search?order=views&country[]='
	open = OPEN_URL(url)
	part = regex_from_to(open,'<div class="filters-inner">','<div class="filters-inner">')
	all  = regex_get_all(part,'class="filter-input"','label')
	for a in all:
		name = regex_from_to(a,'"> ','<')
		url  = regex_from_to(a,'value="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus(temp+url),mode,icon,fanart,'')
		
def QUALITYS(url):
	if '/series/' in url:
		mode = '4'
		temp = base_url+'/series/search?order=views&quality[]='
	else:
		mode = '3'
		temp = base_url+'/search?order=views&quality[]='
	open = OPEN_URL(url)
	part = regex_from_to(open,'name="quality"','<a class="header-filter-sorting-toggle">')
	all  = regex_get_all(part,'class="filter-input"','label')
	for a in all:
		name = regex_from_to(a,'"> ','<')
		url  = regex_from_to(a,'value="','"')
		if not '480 p' in name:
			addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus(temp+url),mode,icon,fanart,'')

def RESOLVE(url):
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	try:
		open = client.request(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	
	id   = regex_from_to(open,'href="https://streamtorrent.tv/view/','"')
	url  = 'https://streamtorrent.tv/api/torrent/%s.json' % id
	urls  = []
	quals = []
	
	try:
		r = OPEN_URL(url)
	except:
		xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/B][/CAPITALIZE][/COLOR]','Oops the connection timed out, Try Again')
		return
	r = json.loads(r)
	
	r = [i for i in r['files'] if 'streams' in i and len(i['streams']) > 0][0]
	r = [{'height': i['height'], 'stream_id': r['_id'], 'vid_id': url} for i in r['streams']]

	links = []
	links += [{'quality': '1080p', 'url': urllib.urlencode(i)} for i in r if int(i['height']) >= 1080]
	links += [{'quality': '720p', 'url': urllib.urlencode(i)} for i in r if 720 <= int(i['height']) < 1080]
	links += [{'quality': '360p', 'url': urllib.urlencode(i)} for i in r if int(i['height']) <= 720]
	links = links[:3]
	for i in links:
		if xbmcaddon.Addon().getSetting('quality') in i['quality']:
			url = i['url']
		else:
			if '1080p' in i['quality']:
				url  = i['url']
				qual = '1080p'
			elif '720p' in i['quality'] and not '1080p' in i['quality']:
				url = i['url']
				qual = '720p'
			else:
				url = i['url']


	

	query = urlparse.parse_qs(url)
	query = dict([(key, query[key][0]) if query[key] else (key, '') for key in query])
	auth = 'https://streamtorrent.tv/api/torrent/%s/%s.m3u8' % (query['vid_id'], query['stream_id'])
	auth = str(auth).replace('/https://streamtorrent.tv/api/torrent','').replace('.json/','/')

	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title':description})
	liz.setProperty("IsPlayable","true")
	liz.setPath(auth)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def SEARCH(url):
	kb = xbmc.Keyboard ('', 'Please Enter Your Query', False)
	kb.doModal()
	if (kb.isConfirmed()):
		query = kb.getText()
		query = str(query).replace(' ','+')
		u   = url%query
		
		open  = OPEN_URL(u)
		if '/series/' in url:
		
		
			all  = regex_get_all(open,'div class="tv-show">','<div class="clearfix">')
			if not all ==[]:
				for a in all:
					url  = regex_from_to(a,'<a href="','"')
					icon = regex_from_to(a,'image:url(','"')
					name = regex_from_to(a,'<span class="tv-show-title">','</span>').replace('&#039;',"'")
					name = regex_from_to(name,'">','<')
					addDir('[COLOR white]%s[/COLOR]'%name,base_url+url,5,base_url+icon,fanart,'')
			else:
				xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/COLOR]','Oops TV Show Not Found')
				
		else:
			all   = regex_get_all(open,'<div class="films-item-image">','</a></li>')
			if not all==[]:
				for a in all:
					name = regex_from_to(a,'title"><span>','<').replace('&#039;',"'")
					url  = regex_from_to(a,'a href="','"')
					icon = regex_from_to(a,'img src="','"')
					addDir('[COLOR white]%s[/COLOR]'%name,base_url+url,7,base_url+icon,fanart,'')
			else:
				xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/COLOR]','Oops TV Show Not Found')
				
def HOMESEARCH():
	d  = xbmcgui.Dialog().select('What Do You Want To Search?',['Movies','TV Shows'])
	kb = xbmc.Keyboard ('', 'Please Enter Your Query', False)
	kb.doModal()
	if (kb.isConfirmed()):
		query = kb.getText()
		query = str(query).replace(' ','+')
		if not d == 0:
			u   = base_url+'/series/search?title=%s&order=views'%query
		
			open  = OPEN_URL(u)
		
			all  = regex_get_all(open,'div class="tv-show">','<div class="clearfix">')
			if not all ==[]:
				for a in all:
					url  = regex_from_to(a,'<a href="','"')
					icon = regex_from_to(a,'image:url(','"')
					name = regex_from_to(a,'<span class="tv-show-title">','</span>').replace('&#039;',"'")
					name = regex_from_to(name,'">','<')
					addDir('[COLOR white]%s[/COLOR]'%name,base_url+url,5,base_url+icon,fanart,'')
			else:
				xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/COLOR]','Oops TV Show Not Found')
				return
		else:
			u   = base_url+'/search?title=%s&order=views'%query
		
			open  = OPEN_URL(u)
			all   = regex_get_all(open,'<div class="films-item-image">','</a></li>')
			if not all ==[]:
				for a in all:
					name = regex_from_to(a,'title"><span>','<').replace('&#039;',"'")
					url  = regex_from_to(a,'a href="','"')
					icon = regex_from_to(a,'img src="','"')
					addDir('[COLOR white]%s[/COLOR]'%name,base_url+url,7,base_url+icon,fanart,'')
			else:
				xbmcgui.Dialog().notification('[COLOR white][B][CAPITALIZE]TORBA[/B][/CAPITALIZE][/COLOR]','Oops Movie Not Found')
				return
		

		
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

	
def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = requests.session().get(url, headers=headers, verify=False,allow_redirects=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
	
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==7:
		liz.setProperty("IsPlayable","true")
		cm = []
		cm.append(('Play Trailer','XBMC.RunPlugin(plugin://plugin.video.torba/?mode=100&url='+str(name)+')'))
		liz.addContextMenuItems(cm,replaceItems=False)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory

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
#	get_auth()
	CAT()
elif mode==1:
	MOVIECAT()
elif mode==2:
	TVCAT()
elif mode==3:
	INDEX(url)
elif mode==4:
	TVINDEX(url)
elif mode==5:
	TVSEASONS(url,description)
elif mode==6:
	TVEPISODES(url,description)
elif mode==7:
	RESOLVE(url)
elif mode==8:
	GENRE(url)
elif mode==9:
	SEARCH(url)
elif mode==10:
	COLLECTIONSCAT()
elif mode==11:
	YEAR(url)
elif mode==12:
	COUNTRY(url)
elif mode==13:
	QUALITYS(url)
	
elif mode==99:
	HOMESEARCH()
elif mode==100:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	trailer.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))