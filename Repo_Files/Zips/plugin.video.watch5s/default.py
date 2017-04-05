import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,hashlib,os,random,re,string,sys,urllib,urlresolver
from resources.modules import tools,client
from metahandler import metahandlers



KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])

if not str(KODIV).startswith('17'):
	xbmcgui.Dialog().ok('Attention',"The Website used in this Addon is SSL Encrypted.","Only Kodi 17 and above supports SSL Encryption.","Please update your System before using this Addon.")
	sys.exit()
	
	
	
	
addon_id   = 'plugin.video.watch5s'
addon_name = 'Watch 5s'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

base_url   = 'http://watch5s.to'
play_link  = 'http://play.watch5s.to/grabber-api/episode/%s?token=%s'





def MOVIES():
	addDir('Top IMDB Movies',base_url+'/top-imdb/movies/',1,icon,fanart,'')
	addDir('Recently Added',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=all'),1,icon,fanart,'')
	addDir('Most Favorite',base_url+urllib.quote_plus('/filter/?sort=favorite&type=movie&quality=all&year=all'),1,icon,fanart,'')
	addDir('Most Viewed',base_url+urllib.quote_plus('/filter/?sort=view&type=movie&quality=all&year=all'),1,icon,fanart,'')
	addDir('Most Rated',base_url+urllib.quote_plus('/filter/?sort=rating&type=movie&quality=all&year=all'),1,icon,fanart,'')
	addDir('In Cinema',base_url+'/cinema/',1,icon,fanart,'')
	addDir('Country',base_url+'/filter',8,icon,fanart,'')
	addDir('Genres','url',3,icon,fanart,'')
	addDir('Years','url',5,icon,fanart,'')
	addDir('A-Z',base_url+'/library/',1,icon,fanart,'')
	addDir('Search','url',4,icon,fanart,'')
	addDir('Settings','url',9,icon,fanart,'')
	
	
def GENRES():
	addDir('Action',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=21&year=all'),1,icon,fanart,'')
	addDir('Adventure',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=22&year=all'),1,icon,fanart,'')
	addDir('Animation',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=23&year=all'),1,icon,fanart,'')
	addDir('Biography',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=41&year=all'),1,icon,fanart,'')
	addDir('Comedy',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=19&year=all'),1,icon,fanart,'')
	addDir('Crime',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=20&year=all'),1,icon,fanart,'')
	addDir('Documentary',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=24&year=all'),1,icon,fanart,'')
	addDir('Drama',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=39&year=all'),1,icon,fanart,'')
	addDir('Family',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=25&year=all'),1,icon,fanart,'')
	addDir('Fantasy',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=26&year=all'),1,icon,fanart,'')
	addDir('History',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=27&year=all'),1,icon,fanart,'')
	addDir('Horror',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=28&year=all'),1,icon,fanart,'')
	addDir('Kids',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=29&year=all'),1,icon,fanart,'')
	addDir('Music',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=30&year=all'),1,icon,fanart,'')
	addDir('Mystery',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=31&year=all'),1,icon,fanart,'')
	addDir('News',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=32&year=all'),1,icon,fanart,'')
	addDir('Romance',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=33&year=all'),1,icon,fanart,'')
	addDir('Sci-Fi',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=38&year=all'),1,icon,fanart,'')
	addDir('Sport',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres%5B%5D=34&year=all'),1,icon,fanart,'')
	addDir('Thriller',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=35&year=all'),1,icon,fanart,'')
	addDir('War',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=36&year=all'),1,icon,fanart,'')
	addDir('Western',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&genres[]=37&year=all'),1,icon,fanart,'')

	
def YEARS():
	addDir('2017',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2017'),1,icon,fanart,'')
	addDir('2016',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2016'),1,icon,fanart,'')
	addDir('2015',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=20l5'),1,icon,fanart,'')
	addDir('2014',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2014'),1,icon,fanart,'')
	addDir('2013',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2013'),1,icon,fanart,'')
	addDir('2012',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2012'),1,icon,fanart,'')
	addDir('2011',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2011'),1,icon,fanart,'')
	addDir('2010',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2010'),1,icon,fanart,'')
	addDir('2009',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2009'),1,icon,fanart,'')
	addDir('2008',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2008'),1,icon,fanart,'')
	addDir('2007',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2007'),1,icon,fanart,'')
	addDir('2006',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2006'),1,icon,fanart,'')
	addDir('2005',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2005'),1,icon,fanart,'')
	addDir('2004',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2004'),1,icon,fanart,'')
	addDir('2003',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2003'),1,icon,fanart,'')
	addDir('2002',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2002'),1,icon,fanart,'')
	addDir('2001',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2001'),1,icon,fanart,'')
	addDir('2000',base_url+urllib.quote_plus('/filter/?sort=latest&type=movie&quality=all&year=2000'),1,icon,fanart,'')
	

def INDEX(url):
	if xbmcaddon.Addon().getSetting('autoplay')=='true':
		mode = 7
	else:
		mode = 6
	xbmc.log(str(url))
	open = client.request(url)
	if '/library/' in url:
		all  = tools.regex_get_all(open,'<tr class="mlnew">','</tr>')
		for a in all:
			name  = tools.regex_from_to(a,'title="','"')
			if not 'Season' in name or 'Episode' in name:
				url   = tools.regex_from_to(a,'<a href="','"')
				icon  = tools.regex_from_to(a,'img src="','"')
				qual  = tools.regex_from_to(a,'"mlnh-3">',"<")
				if xbmcaddon.Addon().getSetting('meta')=='true':
					addDirM('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,len(all),name)
				else:
					addDir('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,fanart,'')
		try:
			np = tools.regex_from_to(open,'<li class="next"><a href="','"')
			addDir('NEXT PAGE',urllib.quote_plus(np),1,icon,fanart,'')
		except:
			pass
	
	elif '/search/?q=' in url:
		all  = tools.regex_get_all(open,'<div class="ml-item">','</div>')
		for a in all:
			name  = tools.regex_from_to(a,'title="','"')
			if not 'Season' in name or 'Episode' in name:
				url   = tools.regex_from_to(a,'<a href="','"')
				icon  = tools.regex_from_to(a,'data-original="','"')
				qual  = tools.regex_from_to(a,"quality'>","<")
				if xbmcaddon.Addon().getSetting('meta')=='true':
					addDirM('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,len(all),name)
				else:
					addDir('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,fanart,'')
				
	else:
		all = tools.regex_get_all(open,'<div class="ml-item">','</div>')
		for a in all:
			name  = tools.regex_from_to(a,'title="','"')
			if not 'Season' in name or 'Episode' in name:
				url   = tools.regex_from_to(a,'<a href="','"')
				icon  = tools.regex_from_to(a,'data-original="','"')
				qual  = tools.regex_from_to(a,"quality'>","<")
				if xbmcaddon.Addon().getSetting('meta')=='true':
					addDirM('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,len(all),name)
				else:
					addDir('%s [COLOR blue]%s[/COLOR]'%(name,qual),url,mode,icon,fanart,'')
		try:
			np = tools.regex_from_to(open,'<li class="next"><a href="','"')
			addDir('NEXT PAGE',urllib.quote_plus(np),1,icon,fanart,'')
		except:
			pass
			
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
	
def COUNTRY(url):
        link = client.request(url)
        match = re.findall(r'<li><label><input class="country-ids" value="(.*?)" name=".*?" type="checkbox"  >(.*?)</label></li>', str(link), re.I|re.DOTALL)
        for country_id, name in match:
                url = base_url + '/filter/?sort=rating&type=movie&quality=all&countries%%5B%%5D=%s&year=all' %(country_id)
                addDir(name,url,1,icon,fanart,'')
				

def SEARCH():
	kb =xbmc.Keyboard ('', 'Enter Search Query')
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		if text =="":
			xbmcgui.Dialog().notification('[COLOR blue]EMPTY SEARCH QUERY[/COLOR] ','PLEASE TRY AGAIN')
		else:
			text = str(text).replace(' ','+')
			url  = base_url+'/search/?q='+text
			open = client.request(url)
			INDEX(url)


def GETLINKS(url,name):
			progressDialog = xbmcgui.DialogProgress()
			progressDialog.create(addon_name, 'Gathering Links For: [COLOR blue]%s[/COLOR]'%name)
			progressDialog.update(0)
			name = str(name).replace(' [COLOR blue]','').replace('[/COLOR]','').replace('CAM','').replace('SD','').replace('HD','')
			name = tools.geturl(name)
			name = re.sub('-$','',name)
			name = re.sub('^-','',name)
			base_link = 'http://watch5s.is'
			strm_link = 'http://play.watch5s.is/grabber-api/episode/%s?token=%s'
			url = re.sub('/$','',url)
			req = url+'/watch/'
			#Text_Box('h',req)
			referer = req
			r = client.request(req)
			
			if '<title>Watch Free Movies Online, Best Site to Watch Free Movies HD - WATCH5S.TO</title>' in r:
				r = client.request(url)
				part = tools.regex_from_to(r,'<div id="mv-info">','</div>')
				url  = tools.regex_from_to(part,'href="','"')
				r    = client.request(url)

			all  = tools.regex_get_all(r,'<div class="les-content">','</div>')
			for a in all:
				try:
					u    = tools.regex_from_to(a,'<a href="','"')
					qual = tools.regex_from_to(a,'first-ep.*?">','<')
					p    = client.request(u, referer=referer, timeout='10')

					t = re.findall('player_type\s*:\s*"(.+?)"', p)[0]
					if not t == 'embed':

						s = client.parseDOM(p, 'input', ret='value', attrs = {'name': 'episodeID'})[0]
						t = ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 8))
						k = hashlib.md5('!@#$%^&*(' + s + t).hexdigest()
						v = hashlib.md5(t + referer + s).hexdigest()

						stream = strm_link % (s, t)
						cookie = '%s=%s' % (k, v)

						u = client.request(stream, referer=referer, cookie=cookie, timeout='10')
						url = tools.regex_from_to(u,'"file":"','"')
						if not 'grabber-api' in url:
							host = 'GVIDEO'
							addDir('%s | [COLOR blue]%s[/COLOR]'%(host,qual),urllib.quote_plus(str(url).replace('\/','/')),7,icon,fanart,'')
					else:
						url = tools.regex_from_to(p,'embed_src: "','"')
						if 'openload' in url:
							host = 'OPENLOAD'
						addDir('%s | [COLOR blue]%s[/COLOR]'%(host,qual),url,7,icon,fanart,'')
				except:
					pass
					
			progressDialog.close()


def GETAUTOPLAY(url):
			#progressDialog = xbmcgui.DialogProgress()
			#progressDialog.create(addon_name, 'Gathering Links For Your Selected Item: [COLOR blue]%s[/COLOR]'%name)
			#progressDialog.update(0)
			base_link = 'http://watch5s.is'
			strm_link = 'http://play.watch5s.is/grabber-api/episode/%s?token=%s'
			url = re.sub('/$','',url)
			req = url+'/watch/'
			#Text_Box('h',req)
			referer = req
			r = client.request(req)
			
			if '<title>Watch Free Movies Online, Best Site to Watch Free Movies HD - WATCH5S.TO</title>' in r:
				r = client.request(url)
				part = tools.regex_from_to(r,'<div id="mv-info">','</div>')
				url  = tools.regex_from_to(part,'href="','"')
				r    = client.request(url)
			try:
				server = tools.regex_from_to(r,'<strong>SERVER 1</strong>','</a>')
				server = tools.regex_from_to(server,'href="','"')
			except:
				try:
					server = tools.regex_from_to(r,'<strong>SERVER 10</strong>','</a>')
					server = tools.regex_from_to(server,'href="','"')
				except:
					server = tools.regex_from_to(r,'<strong>OpenLoad</strong>','</a>')
					server = tools.regex_from_to(server,'href="','"')
					
			
			open = client.request(server)
			t = re.findall('player_type\s*:\s*"(.+?)"', open)[0]
			if not t == 'embed':

						s = client.parseDOM(open, 'input', ret='value', attrs = {'name': 'episodeID'})[0]
						t = ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 8))
						k = hashlib.md5('!@#$%^&*(' + s + t).hexdigest()
						v = hashlib.md5(t + referer + s).hexdigest()

						stream = strm_link % (s, t)
						cookie = '%s=%s' % (k, v)

						u = client.request(stream, referer=referer, cookie=cookie, timeout='10')
						url = tools.regex_from_to(u,'"file":"','"').replace('\/','/')
						if not 'grabber-api' in url:
							return url
			else:
				url = tools.regex_from_to(open,'embed_src: "','"')
				return url
				
					
def RESOLVE(url):
	if xbmcaddon.Addon().getSetting('autoplay')=='true':
		play = GETAUTOPLAY(url)
	else:
		if 'redirector' in url:
			play = url
		else:
			play = urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
	
	
	
	


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==7:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
def addDirM(name,url,mode,iconimage,itemcount,movie_title):
        meta = metahandlers.MetaData().get_meta('movie',movie_title,'')
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
				pass
        meta['title'] = name
        meta['plot'] = '[B][COLOR white]%s[/COLOR][/B]' %meta['plot']
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&movie_title="+urllib.quote_plus(movie_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo(type="Video", infoLabels=meta)
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
        if mode==7:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok
	
	
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
	MOVIES()

elif mode==1:
	INDEX(url)

elif mode==2:
	MOVIES()
	
elif mode==3:
	GENRES()
	
elif mode==4:
	SEARCH()
	
elif mode==5:
	YEARS()
	
elif mode==6:
	GETLINKS(url,name)
	
elif mode==7:	
	RESOLVE(url)
	
elif mode==8:
	COUNTRY(url)
	
elif mode==9:
	xbmcaddon.Addon(id=addon_id).openSettings()
	
	


xbmcplugin.endOfDirectory(int(sys.argv[1]))