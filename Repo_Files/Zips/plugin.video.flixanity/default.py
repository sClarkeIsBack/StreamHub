import re,os,xbmc,urllib

from resources.modules import client

addon_id   = 'plugin.video.flixanity'

base_url   = 'https://flixanity.online'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))


def home():
	addDir('Movies',base_url+'/movies',1,icon,fanart,'')
	addDir('Tv Shows',base_url+'/tv-shows',3,icon,fanart,'')
	addDir('New Movies',base_url+'/new-movies',2,icon,fanart,'')
	addDir('New Episodes',base_url+'/new-episodes',2,icon,fanart,'')
	

		  
def movies():
	addDir('Trending',base_url+'/movies/trending',2,icon,fanart,'')
	addDir('Popular',base_url+'/movies/popular',2,icon,fanart,'')
	addDir('Release Date',base_url+'/movies/release-date',2,icon,fanart,'')
	addDir('Most Watched',base_url+'/movies/most-watched',2,icon,fanart,'')
	addDir('IMDB Rating',base_url+'/movies/imdb-rating',2,icon,fanart,'')
	addDir('Highest Grossing',base_url+'/movies/highest-grossing',2,icon,fanart,'')
	addDir('In Theaters',base_url+'/movies/in-theaters',2,icon,fanart,'')
	addDir('Genres','movies',6,icon,fanart,'')
	
def shows():
	addDir('Trending',base_url+'/tv-shows/trending',2,icon,fanart,'')
	addDir('Popular',base_url+'/tv-shows/popular',2,icon,fanart,'')
	addDir('Most Watched',base_url+'/tv-shows/most-watched',2,icon,fanart,'')
	addDir('IMDB Rating',base_url+'/tv-shows/imdb-rating',2,icon,fanart,'')
	addDir('Genres','tv',6,icon,fanart,'')
	
	
def index(url):
	if 'movies' in url:
		mode = '10'
	else:
		mode = '4'
	open = client.request(url)
	all  = regex_get_all(open,'<section class="cardBox.+?flip">','</section>')
	for a in all:
		name = regex_from_to(a,'alt="','"')
		if 'span class' in name:
			n  = regex_from_to(a,'href=".+?">','<')
			ep = regex_from_to(a,'<p>','</p>')
			name = n + ' ' + ep
			icon = regex_from_to(a,'src="','"')
			url  = regex_from_to(a,'href="','"')
			mode = '10'
		else:
			url  = regex_from_to(a,'href="','"')
			icon = regex_from_to(a,'img src="','"')
		addDir(name,urllib.quote_plus(url),mode,icon,fanart,'')
	try:
		np = re.compile('<a href="(.+?)" class="next-page-button">').findall(open)
		for url in np:
			addDir('[COLOR lime][B]Next Page >[/COLOR][/B]',url,2,icon,fanart,'')
	except:
		pass
		
	
def genres(url):
	if 'movies' in url:
		url = base_url+'/movies/'
	else:
		url = base_url+'/tv-shows/'
		
	open = client.request(url)
	
	part = regex_from_to(open,'Genres:','</select>')
	
	regex   = re.compile('<option value="(.+?)">(.+?)<').findall(part)
	for url,name in regex:
		if not 'All Movies' in name:
			if not 'All TV Shows' in name:
				addDir(name,url,2,icon,fanart,'')
				
		
def season(url):
	open = client.request(url)
	
	part = regex_from_to(open,'<b>Seasons:</b>','</div>')
	
	regex= re.compile('href="(.+?)".+?">(.+?)<').findall(part)
	for url,name in regex:
		addDir('Season %s'%name,url,5,icon,fanart,'')
		
		
def episodes(url):
	open = client.request(url)
	
	all  = regex_get_all(open,'<h5 class="episode-title">','</span>')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'data-img="','"')
		addDir(name,url,10,icon,fanart,'')
		
		
def getLinks(url):
            import re,json,time,base64,urlparse,urllib
			
            headers = {}
            r = client.request(url, headers=headers, output='extended', timeout='10')

            cookie = r[4] ; headers = r[3] ; result = r[0]

            try:
                r = re.findall('(https:.*?redirector.*?)[\'\"]', result)
                for i in r:
                    try:
						addDir('Direct',urllib.quote_plus(i),100,icon,fanart,'')
                    except:
                        pass
            except:
                pass

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url


            u = '/ajax/jne.php'
            u = urlparse.urljoin(base_url, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            c = client.request(u, post=post, headers=headers, XHR=True, output='cookie', error=True)

            headers['Cookie'] = cookie + '; ' + c

            r  = client.request(u, post=post, headers=headers, XHR=True)
            re = re.compile('type":"(.+?)".+?embed":".+?http(.+?)"\\ ',re.DOTALL|re.MULTILINE).findall(r)
            for name,url in re:
				url = 'http'+(url).replace('\/','/').replace('\\','')
				addDir(name,urllib.quote_plus(url),100,icon,fanart,'')
		  
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
	if mode==100:
		liz.setProperty("IsPlayable","true")
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
	movies()
	
elif mode==2:
	index(url)

elif mode==3:
	shows()
	
elif mode==4:
	season(url)
	
elif mode==5:
	episodes(url)
	
elif mode==6:
	genres(url)
	
elif mode==10:
	getLinks(url)
	
elif mode==100:
	import xbmcgui,xbmcplugin,urlresolver
	try:
		host = urlresolver.HostedMediaFile(url)
		if host:
			url = urlresolver.resolve(url)
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		liz.setInfo(type='Video', infoLabels='')
		liz.setProperty("IsPlayable","true")
		liz.setPath(url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	except:
		pass

import xbmcplugin
xbmcplugin.endOfDirectory(int(sys.argv[1]))