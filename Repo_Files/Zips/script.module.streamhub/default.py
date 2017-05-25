import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver,ssl,liveresolver,zipfile,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from resources.modules import control,tvplayer,cloudflare


addon_id   = 'script.module.streamhub'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
putlockerhd  = 'http://putlockerhd.co'
ccurl      = 'http://cartooncrazy.me'
s          = requests.session()
bypass     = cloudflare.create_scraper()

ccurl      = 'http://cartooncrazy.me'
xxxurl     ='http://www.xvideos.com'
kidsurl    = base64.b64decode ('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NDbGFya2VJc0JhY2svU3RyZWFtSHViL21hc3Rlci9MaW5rcy9LaWRzL2tpZHNjb3JuZXIueG1s')
docurl     = 'http://documentaryheaven.com'
mov2       = 'http://zmovies.to'
wwe        = 'http://watchwrestling.in'
tv         = base64.b64decode ('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NDbGFya2VJc0JhY2svU3RyZWFtSHViL21hc3Rlci9MaW5rcy8yNDcvMjQ3dHYueG1s')
proxy      = 'http://www.justproxy.co.uk/index.php?q='
music      = 'http://woodmp3.com/search/'
movies_url = 'https://torba.se'
def CAT():
	addDir('EXABYTE','url',85,icon,fanart,'')
	addDir('MOVIES2','url',37,icon,fanart,'')
	addDir('FAMILY SECTION',kidsurl,56,icon,fanart,'')
	addDir('XXX SECTION','URL',31,icon,fanart,'')
	addDir('DOCS',docurl+'/watch-online/',35,icon,fanart,'')
	addDir('24/7 TV',tv,48,icon,fanart,'')
	addDir('MUSIC',tv,64,icon,fanart,'')
	addDir('IPTV','url',84,icon,fanart,'')
	addDir('IPTV2','url',88,icon,fanart,'')

def MOV2CAT():
	addDir('[COLOR red]L[/COLOR]atest Releases','NEW:http://novamovie.net',79,icon,fanart,'')
	addDir('[COLOR red]M[/COLOR]ost Popular','http://novamovie.net',79,icon,fanart,'')
	addDir('[COLOR red]M[/COLOR]ost Viewed','http://novamovie.net/?v_sortby=views&v_orderby=desc',79,icon,fanart,'')
	addDir('[COLOR red]R[/COLOR]ecommended','http://novamovie.net/tag/recommended/',79,icon,fanart,'')
	addDir('[COLOR red]G[/COLOR]enres','url',81,icon,fanart,'')
	addDir('[COLOR red]Y[/COLOR]ears','years',81,icon,fanart,'')
	addDir('[COLOR red]S[/COLOR]earch','url',82,icon,fanart,'')
	
def TVREQUESTCAT():
	addDir('Everybody Loves Raymond','ELR',50,'http://www.gstatic.com/tv/thumb/tvbanners/184243/p184243_b_v8_ab.jpg','','')
	addDir('How i Met Your Mother','HIMYM',50,'http://www.gstatic.com/tv/thumb/tvbanners/9916255/p9916255_b_v8_aa.jpg','','')
	addDir('Naked And Afraid','NAA',50,'http://www.gstatic.com/tv/thumb/tvbanners/9974211/p9974211_b_v8_ad.jpg','','')
	addDir('The Walking Dead','TWD',50,'http://www.gstatic.com/tv/thumb/tvbanners/13176393/p13176393_b_v8_ab.jpg','','')
	addDir('[COLOR red][B]IF IT FAILS THE FIRST TIME CLICK IT AGAIN[/COLOR][/B]','url','','','','')
	
def FAMILYCAT():
	addDir('Disney Movies','url',58,icon,fanart,'')
	addDir('Family Cartoons',kidsurl,51,icon,fanart,'')
	addDir('Family Movies','http://kisscartoon.so/cartoon-movies/',77,icon,fanart,'')
	
def FAMILYMOVIESCAT():
	addDir('All','http://kisscartoon.so/cartoon-movies/',74,icon,fanart,'')
	addDir('By Year','http://kisscartoon.so/cartoon-movies/',78,icon,fanart,'')
	addDir('By Genre','http://kisscartoon.so/cartoon-movies/',76,icon,fanart,'')

def MUSICCAT():
	addDir('Top Music','http://',68,icon,fanart,'')
	addDir('Collections','url',72,icon,fanart,'')
	addDir('Radio','http://',69,icon,fanart,'')
	addDir('Search','search',63,icon,fanart,'')
	
def TOPMUSICAT():
	addDir('UK | The Offical Top 40 Singles','http://www.bbc.co.uk/radio1/chart/singles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Dance Singles','http://www.bbc.co.uk/radio1/chart/dancesingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Rock Singles','http://www.bbc.co.uk/radio1/chart/rocksingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 R&B Singles','http://www.bbc.co.uk/radio1/chart/rnbsingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 30 Indie Singles','http://www.bbc.co.uk/radio1/chart/indiesingles',67,icon,fanart,'')
	
def MUSICCOL():
	addDir('BBC Radio 1 Live Lounge Collection','https://www.discogs.com/label/804379-Radio-1s-Live-Lounge',70,icon,fanart,'')
	addDir('Now Thats What I Call Music Collection','NOW',70,icon,fanart,'')
	

	
	

	
	
	
	
	
	
	
	
	
def NOVAMOVIES(url):
	if url.startswith('NEW:'):
		url  = str(url).replace('NEW:','')
		open = OPEN_URL(url)
		part = regex_from_to(open,'<div id="slider2"','<h1 style="display:none;">')
		all  = regex_get_all(part,'<div class="item"','</div>')
		for a in all:
			name = regex_from_to(a,'alt="','"')
			url  = regex_from_to(a,'href="','"')
			icon = regex_from_to(a,'img src="','"')
			addDir(name,url,80,icon,fanart,'')
	else:
		open = OPEN_URL(url)
		part = regex_from_to(open,'<h1 style="display:none;">','</html>')
		if not part == "":
			all  = regex_get_all(part,'<div class="fixyear">','</a>')
			for a in all:
				name = regex_from_to(a,'alt="','"')
				url  = regex_from_to(a,'href="','"')
				icon = regex_from_to(a,'img src="','"')
				addDir(name,url,80,icon,fanart,'')
		else:
			all  = regex_get_all(open,'<div class="fixyear">','</a>')
			for a in all:
				name = regex_from_to(a,'alt="','"')
				url  = regex_from_to(a,'href="','"')
				icon = regex_from_to(a,'img src="','"')
				addDir(name,url,80,icon,fanart,'')
		
		try:
			np = regex_from_to(open,'<div class="pag_b"><a href="','"')
			addDir('[COLOR red][B]NEXT PAGE >[/B][/COLOR]',np,79,icon,fanart,'')
		except:
			pass
	
def NOVAMOVIESGENRE(url):
	open = OPEN_URL('http://novamovie.net')
	if not url == 'years':
		part = regex_from_to(open,'>GENRE</a>','</ul>')
	else:
		part = regex_from_to(open,'>YEAR</a>','</ul>')
	all  = regex_get_all(part,'<li','</li')
	for a in all:
		name = regex_from_to(a,'/">','<')
		url  = regex_from_to(a,' href="','"')
		addDir(name,url,79,icon,fanart,'')
	
	
def NOVAMOVIESSEARCH():

	kb = xbmc.Keyboard ('', 'Search For a Movie', False)
	kb.doModal()
	if (kb.isConfirmed()):
		query = kb.getText()
		query = str(query).replace(' ','+')

	open = OPEN_URL('http://novamovie.net/?s='+query)
	all  = regex_get_all(open,'<div class="fixyear">','</a>')
	for a in all:
		name = regex_from_to(a,'alt="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		if not name=="":
			addDir(name,url,80,icon,fanart,'')

	
def xxxCAT():
	if control.setting('freshstart')=='true':
		setxxxpass()
		xbmcaddon.Addon().setSetting('freshstart','false')
	if control.setting('enablexxxpass')=='true':
		kb = xbmc.Keyboard ('', 'Enter Your Password', False)
		kb.doModal()
		if (kb.isConfirmed()):
			pw = kb.getText()
			if pw == control.setting('xxxpass'):
				addDir("The Best Videos",xxxurl+'/best',24,icon,fanart,'')
				addDir("Latest Videos",xxxurl,24,icon,fanart,'')
				addDir("Real Videos",xxxurl+'/c/Amateur-17',24,icon,fanart,'')
				addDir("All Videos",xxxurl+'/tags',99,icon,fanart,'')
				addDir("Search",'search',24,icon,fanart,'')
			else:
				xbmcgui.Dialog().ok('[COLOR red][B]StreamHub[/B][/COLOR]','Incorrect Password, Please Try Again')
				return
	else:
		addDir("The Best Videos",xxxurl+'/best',24,icon,fanart,'')
		addDir("Latest Videos",xxxurl,24,icon,fanart,'')
		addDir("Real Videos",xxxurl+'/c/Amateur-17',24,icon,fanart,'')
		addDir("All Videos",xxxurl+'/tags',99,icon,fanart,'')
		addDir("Search",'search',24,icon,fanart,'')
	

def setxxxpass():
	d = xbmcgui.Dialog().yesno('[COLOR red]StreamHub[/COLOR]','Would You Like To Set a Password for the XXX Section?')
	if d:
		kb = xbmc.Keyboard ('', 'Please Enter a Password', False)
		kb.doModal()
		if (kb.isConfirmed()):
			pw = kb.getText()
			if pw =="":
				xbmcgui.Dialog().notification('[COLOR red]Password Cannot Be Blank[/COLOR]','StreamHub')
				setxxxpass()
			else:
				xbmcaddon.Addon().setSetting('xxxpass',pw)
				xbmcaddon.Addon().setSetting('enablexxxpass','true')
				xbmcgui.Dialog().ok('[COLOR red]StreamHub[/COLOR]','Password has been set')
			

		
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


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7 or mode==17 or mode==15 or mode==23 or mode==30 or mode==27 or mode ==36 or mode==39 or mode==50 or mode==53 or mode==55 or mode==57 or mode==60 or mode==62 or mode ==75 or mode==80 or mode==999:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==73 or mode==1000:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
def addDirPlay(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if mode==44:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory

def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
	
	
	
	
def NOVAMOVIERESOLVE(url):
	open = OPEN_URL(url)
	url  = re.compile('<iframe.+?src="(.+?)"').findall(open)[0]
	open = OPEN_URL('http:'+url)
	res_quality = []
	stream_url  = []
	quality     = ''

	match = regex_get_all(open,'file"','type"')
	try:
		for a in match:
			quality = '[B][I][COLOR red]%s[/COLOR][/I][/B]' %regex_from_to(a,'label": "','"')
			url     =  regex_from_to(a,': "','"')
			if not '.srt' in url:
				res_quality.append(quality)
				stream_url.append(url)
		if len(match) >1:
			ret = xbmcgui.Dialog().select('Select Stream Quality',res_quality)
			if ret == -1:
				return
			elif ret > -1:
				url = stream_url[ret]
			else:
				url = regex_from_to(open,'file":"','"')
	except:
		url = regex_from_to(open,'file":"','"')
		
	liz = xbmcgui.ListItem('', iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels='')
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	

	
	
	
	

def tvlist(url):
    thumb = ''
    art   = ''
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		addDir(name,url,46,icon,fanart,'') 
		
		



def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def OPEN_URLputlockerhd(url):
        headers = {}
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers, allow_redirects=False).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        return link
		
def addDirputlockerhd(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3 or mode ==15:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
	
def putlockerhdread(url):
        url = url.replace('https','http')
        link = OPEN_URLputlockerhd(url)
        all_videos = regex_get_all(link, 'cell_container', '<div><b>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'a title="', '\(')
                name = addon.unescape(name)
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                addDirputlockerhd(name,putlockerhd+url,15,'http://'+thumb,fanart,'')
        try:
                match = re.compile('<a href="(.*?)\?page\=(.*?)">').findall(link)
                for url, pn in match:
                        url = putlockerhd+url+'?page='+pn
                        addDir('[I][B][COLOR red]Page %s [/COLOR][/B][/I]' %pn,url,19,icon,fanart,'')
        except: pass
		
def putlockerhdplay(url):
    try:
        url = re.split(r'#', url, re.I)[0]
        request_url = putlockerhd+'/video_info/iframe'
        link = OPEN_URLputlockerhd(url)
        form_data={'v': re.search(r'v\=(.*?)$',url,re.I).group(1)}
        headers = {'origin':'http://putlockerhd.co', 'referer': url,
                   'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
        r = requests.post(request_url, data=form_data, headers=headers, allow_redirects=False)
        try:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[-1]
        except:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[0]
        url = url.replace("&amp;","&").replace('%3A',':').replace('%3D','=').replace('%2F','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
	
#setxxxpass()
		
def xxx(url):
        if url=='search':
			kb = xbmc.Keyboard ('', 'Enter a Search Query', False)
			kb.doModal()
			if (kb.isConfirmed()):
				query = kb.getText()
				query = str(query).replace(' ','+').lower()
				url   = xxxurl+'/?k='+query
        link = OPEN_URL(url)
        try:
			xxxadd_next_button(link)
        except:pass
        all_videos = regex_get_all(link, 'class="thumb-block ">', '</a></p>')
        for a in all_videos:
			name = regex_from_to(a, 'title="', '"')
			name = str(name).replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#039;',"'")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			thumb = regex_from_to(a, '<img src="', '"')
			addDir(name,'http://www.xvideos.com'+url,27,thumb,'','')
			

def xxxadd_next_button(link):
			try:
				if '/tags/' in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp=regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			
			try:
				if '/tags/' not in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp = regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					if not nextp=='':return
					addDir('[B][COLOR red]Next Page[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			return
		
def xxxgenre(url):
		if xbmcaddon.Addon().getSetting('enablexxxpass')=='true':
			kb = xbmc.Keyboard ('', 'Please Enter Your XXX Password', False)
			kb.doModal()
			if (kb.isConfirmed()):
				pw = kb.getText()
				if pw == xbmcaddon.Addon().getSetting('xxxpass'):
					url = url
				else:
					xbmcgui.Dialog().ok('Attention','Incorrect Password, Please Try Again')
					return
			else:
				xbmcgui.Dialog().ok('Attention','Blank Password is Not Aloud, Please Try Again')
				return
		link = OPEN_URL(url)
		main = regex_from_to(link,'<strong>All tags</strong>','mobile-hide')
		all_videos = regex_get_all(main, '<li>', '</li>')
		for a in all_videos:
			name = regex_from_to(a, '"><b>', '</b><span').replace("&amp;","&")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			url = url+'/'
			thumb = regex_from_to(a, 'navbadge default">', '<')
			addDir('%s     [B][COLOR red](%s Videos)[/COLOR][/B]' %(name,thumb),xxxurl+url,24,'','','')
			

def resolvexxx(url):
	base = 'http://www.xvideos.com'
	page  = OPEN_URL(url)
	page=urllib.unquote(page.encode("utf8"))
	page=str(page).replace('\t','').replace('\n','').replace('\r','').replace('                                            	','')
	play = regex_from_to(page,"setVideoUrlHigh.+?'","'")
	url = str(play).replace('[','').replace("'","").replace(']','')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	

def passpopup(url):
 kb =xbmc.Keyboard ('', 'heading', True)
 kb.setHeading('Enter 18+ Password') # optional
 kb.setHiddenInput(True) # optional
 kb.doModal()
 if (kb.isConfirmed()):
    text = kb.getText()
    if text == str(xbmcaddon.Addon().getSetting('xxxpass')):
		url = str(url).replace('****','/tags')
		return url
    else:
        xbmcgui.Dialog().ok('Attention', "Incorrect Password, You would of set this on first use of this Addon.")

'''def resolvecartooncrazy(url,icon):
	bypass  = cloudflare.create_scraper()
	u       = bypass.get(url).content
	embed = re.compile('<iframe src="(.+?)"').findall(u)
	embed = str(embed).replace("', '/300.html', '/300.html']","").replace('[','').replace("'","")
	get = OPEN_URL(embed)
	regex = re.compile('<iframe src=(.+?)"').findall(get)
	regex = str(regex).replace('[','').replace('"','').replace(']','').replace("'","")
	geturl = OPEN_URL(regex)
	stream = re.compile('file: "(.+?)"').findall(geturl)
	stream = str(stream).replace('[','').replace('"','').replace(']','').replace("'","")
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={"Title": name})
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmc.Player().play(stream,liz)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def opencartooncrazy(url):
	bypass  = cloudflare.create_scraper()
	u       = bypass.get(url).content
	regex   = regex_from_to(u,'data-id="','"')
	url     = ccurl+'/ep.php?id='+regex
	#link    = regex_from_to(u,'<img src="','"')
	openurl = bypass.get(url).content
	all_videos = regex_get_all(openurl, '<tr>', '</tr>')
	for a in all_videos:
		name = regex_from_to(a, '<h2>', '</h2>')
		name = str(name).replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		url  = regex_from_to(a, 'href="', '"')
		addDir(name,ccurl+url,30,'','','')
		
def CartooncrazyList():
    OPEN = Open_Url('http://mkodi.co.uk/streamhub/lists/cartooncrazy.xml')
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		fanart='http://'
		addDir(name,url,34,icon,fanart,'') 
    xbmc.executebuiltin('Container.SetViewMode(50)')

def CartooncrazysubList(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		fanart='http://'
		addDir(name,url,26,icon,fanart,'') 
    xbmc.executebuiltin('Container.SetViewMode(50)')'''
def documentary(url):
	OPEN = OPEN_URL(url)
	regex = regex_get_all(OPEN,'<h2><a href','alt="')
	for a in regex:
		url = regex_from_to(a,'="','"')
		title = regex_from_to(a,'">','<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		thumb = regex_from_to(a,'img src="','"')
		vids = regex_from_to(a,'</a> (',')</h2>').replace('(','').replace(')','')
		if vids == "":
			addDir(title,url,36,thumb,fanart,'')
		else:
			addDir(title,docurl+url,35,thumb,fanart,'')
	try:
		link = re.compile('<li class="next-btn"><a href="(.+?)"').findall(OPEN)
		link = str(link).replace('[','').replace(']','').replace("'","")
		xbmc.log(str(link))
		if link == "":
			return False
		else:
			addDir('[B][COLOR red]NEXT PAGE[/COLOR][/B]',link,35,thumb,fanart,'')
	except:pass
def resolvedoc(url):
	open = OPEN_URL(url)
	xbmc.log(str(open))
	url = regex_from_to(open,'height=".*?" src="','"')
	link = urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(link))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
'''def openmov2(url):
	link = OPEN_URL(url)
	link = link.encode('ascii', 'ignore').decode('ascii')
	nexp=regex_from_to(link,'<link rel="next" href="','"')
	if nexp=="":
		nexp = 'none'
	else:
		addDir('[COLOR red]NEXT PAGE[/COLOR]',nexp,38,'','','')
	all_videos = regex_get_all(link, '<div class="featured-thumbnail">', '</header>')
	for a in all_videos:
		icon = regex_from_to(a, 'src="', '"').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'")
		url = regex_from_to(a, '                                    <a href="', '" title=.+?').replace("&amp;","&")
		name = regex_from_to(a, 'rel="bookmark">', '<').replace('&#8217;',"'")
		addDir(name,url,39,icon,fanart,'')
		
def SEARCHmov2(type):
		keyb = xbmc.Keyboard('', 'Type in Query')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText().replace(' ','+')
			if search == '':
				xbmc.executebuiltin("XBMC.Notification([COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search,7000,"+icon+")")
				return
			else: pass
		url = mov2+'/?s='+search
		print url
		openmov2(url)
		
def GENREmov2(url):
        link = OPEN_URL(url)
        link = link.encode('ascii', 'ignore')
        match=regex_get_all(link,'<button type="button">','</button>')
        xbmc.log(str(match))
        for a in match:
			link = regex_from_to(a,'href="','"').replace('https','http')
			name = regex_from_to(a,'target="_blank">','<')
			xbmc.log(str(link))
			xbmc.log(str(name))
			addDir(name,link,38,icon,fanart,'')
def playmov2(url):
		link = OPEN_URL(url)
		referer = url
		vid = re.compile('link: "(.*?)"').findall(link)[0]
		url2 =  'http://zmovies.to/wp-content/themes/magxp/phim/getlink.php?poster=&link='+vid
		page = OPEN_URL(url2)
		xbmc.log(str(page))
		if '720p' in page:
				play = re.compile(',{"file":"(.*?)","type":"mp4","label":"720p"').findall(page)[0]
				pla2 = str(play).replace('\/','/').replace("[",'').replace(':"','').replace("'","").replace(']','').replace('":','')
				play3 = str(pla2).replace('\\','').replace('//','/').replace('https:/','https://')
				play4 =urlresolver.HostedMediaFile(play3).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
				liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
				liz.setProperty('IsPlayable','true')
				liz.setPath(str(play4))
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
				xbmcplugin.endOfDirectory(int(sys.argv[1]))
				
		if 'openload' in page:
			url = regex_from_to(page,'<iframe src="','"')
			play=urlresolver.HostedMediaFile(url).resolve()
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
		else:
			all_links = regex_get_all(page,'"file"','}')
			url = regex_from_to(page,':"','"')
			url = str(url).replace('\/','/').replace("[",'').replace(':"','').replace("'","").replace(']','').replace('":','')
			url = str(url).replace('\\','').replace('//','/').replace('https:/','https://')
			xbmc.log('******************')
			xbmc.log(str(url))
			qual = regex_from_to(page,'"label":"','"')
			addDir(qual,url,39,icon,fanart,'')'''

	
def opentwentyfourseven(url):
	page = proxy+url
	m3ubase= 'plugin://plugin.video.f4mTester/?streamtype=HLS&amp;url='
	m3ubase2= '&amp;name='
	all_vids=re.compile('<li id="menu-item-(.*?)</div> </div></div>').findall(page)
	xbmc.log(str(all_vids))
	for a in all_vids:
		url = regex_from_to(a,'<a href="','"')
		name = regex_from_to(a,'<span class="link_text">\n','\n')
		xbmc.log(str(url))
		xbmc.log(str(name))
		
		
def resolvetwentyfourseven(url,icon):
	m3ubase= 'plugin://plugin.video.f4mTester/?streamtype=HLS&amp;url='
	name='24/7'
	m3ubase2= '&amp;icon='+icon+'&amp;name='+name
	xbmc.log(str(proxy)+str(url))
	open = OPEN_URL(proxy+url)
	m3u  = re.compile('<source.*?src="(.*?)"',re.DOTALL).findall(open)[0]
	play = m3ubase+m3u+m3ubase2
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	xbmc.Player().play(play,liz)
	tvlist(tv)
	
def home():
	home = xbmc.executebuiltin('XBMC.RunAddon(plugin://plugin.video.streamhub/?action=)')
	return home
	

#get = OPEN_URL(cartoons)
#xbmc.log(str(get))
	
def TVREQUESTCATPLAY(name,url,icon):
	if 'TWD' in url:
		play='plugin://plugin.video.streamhub/?action=tvtuner&url=<preset>tvtuner</preset><url>http://opentuner.is/the-walking-dead-2010/</url><thumbnail>https://fanart.tv/fanart/tv/153021/clearart/TheWalkingDead-153021-5.png</thumbnail><fanart>0</fanart><content>tvtuner</content><imdb>tt1520211</imdb><tvdb>153021</tvdb><tvshowtitle>The+Walking+Dead</tvshowtitle><year>2010</year>&content=tvtuners'
	elif 'ELR' in url:
		play='plugin://plugin.video.streamhub/?action=tvtuner&url=<preset>tvtuner</preset><url>http://opentuner.is/everybody-loves-raymond-1996/</url><thumbnail>http://www.gstatic.com/tv/thumb/tvbanners/184243/p184243_b_v8_ab.jpg</thumbnail><fanart>0</fanart><content>tvtuner</content><imdb>tt0115167</imdb><tvdb>73663</tvdb><tvshowtitle>Everybody+Loves+Raymond</tvshowtitle><year>1996</year>&content=tvtuners'
	elif 'NAA' in url:
		play='plugin://plugin.video.streamhub/?action=tvtuner&url=<preset>tvtuner</preset><url>http://opentuner.is/naked-and-afraid-2013/</url><thumbnail>http://www.gstatic.com/tv/thumb/tvbanners/9974211/p9974211_b_v8_ad.jpg</thumbnail><fanart>0</fanart><content>tvtuner</content><imdb>tt3007640</imdb><tvdb>270693</tvdb><tvshowtitle>Naked+And+Afraid</tvshowtitle><year>2013</year>&content=tvtuners'
	elif 'HIMYM' in url:
		play='plugin://plugin.video.streamhub/?action=tvtuner&url=<preset>tvtuner</preset><url>http://opentuner.is/how-i-met-your-mother-2005/</url><thumbnail>http://www.gstatic.com/tv/thumb/tvbanners/9916255/p9916255_b_v8_aa.jpg</thumbnail><fanart>0</fanart><content>tvtuner</content><imdb>tt0460649</imdb><tvdb>75760</tvdb><tvshowtitle>How+I+Met+Your+Mother</tvshowtitle><year>2005</year>&content=tvtuners'
	xbmc.executebuiltin('XBMC.RunPlugin('+play+')')
		
		
		
def toongetlist(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<td>','</td>')
	for a in all:
		url = regex_from_to(a,'href="','"')
		name= regex_from_to(a,'">','<')
		addDir('[COLOR white]%s[/COLOR]'%name,url,52,icon,fanart,'')
		
def toongeteps(url):
		open = OPEN_URL(url)
		all  = regex_get_all(open,'&nbsp;&nbsp;','<span')
		for a in all:
			url = regex_from_to(a,'href="','"')
			name = regex_from_to(a,'">','<')
			addDir('[COLOR white]%s[/COLOR]'%name,url,53,icon,fanart,'')
			
def toongetresolve(name,url):
    OPEN = OPEN_URL(url)
    url1=regex_from_to(OPEN,'Playlist 1</span></div><div><iframe src="','"')
    url2=regex_from_to(OPEN,'Playlist 2</span></div><div><iframe src="','"')
    url3=regex_from_to(OPEN,'Playlist 3</span></div><div><iframe src="','"')
    url4=regex_from_to(OPEN,'Playlist 4</span></div><div><iframe src="','"')
    xbmc.log(str(url1))
    xbmc.log(str(url2))
    xbmc.log(str(url3))
    xbmc.log(str(url4))
    try:
			u   = OPEN_URL(url1)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url2)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url3)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url4)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
		xbmcgui.Dialog().notification('[COLOR red][B]StreamHub[/B][/COLOR]','Oops, This Link Is Down!')
	
def disneymovies(url):
	open = OPEN_URL(url)
	a    = regex_from_to(open,'<br /></div>','<center>')
	all  = regex_get_all(a,'<a href','</div>')
	for a in all:
		url = regex_from_to(a,'="','"')
		name= regex_from_to(a,'<b>','</b>').replace('#038;','').replace('&#8217;',"'")
		addDir('[COLOR white]%s[/COLOR]'%name,url,57,icon,fanart,'')
		
def disneymoviesresolve(url):
	open = OPEN_URL(url)
	try:
		url1 = re.compile('scrolling="no" src="(.*?)"').findall(open)[0]
	except:
		url1 = re.compile('<iframe.+?src="(.*?)"').findall(open)[0]
	if url1.startswith('https://href.li/?'):
		url1 = str(url1).replace('https://href.li/?','')
	play=urlresolver.HostedMediaFile(url1).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def tvguidepick(name):
	if name =='BBC1':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD','HD Backup'])
		if a ==0:
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_one_west_midlands.m3u8'
		elif a ==1:
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_hd.m3u8'
		else:
			url = 'http://tvplayer.com/watch/bbcone'
	elif name =='BBC2':
		a = xbmcgui.Dialog().select('Select a link',['HD','HD Backup','HD Backup 2'])
		if a ==0:
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_two_england.m3u8'
		elif a ==1:
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_two_hd.m3u8'
		else:
			url = 'http://tvplayer.com/watch/bbctwo'
	elif name =='ITV1':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/itv1'
		elif a ==1:
			url = 'http://itv1liveios-i.akamaihd.net/hls/live/203437/itvlive/ITV1MN/master_Main1800.m3u8'
			
	elif name =='CHAN4':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/channel-4'
		else:
			url = 'http://tvplayer.com/watch/channel4'
	elif name =='CHAN5':
			url = 'http://tvplayer.com/watch/channel5'
	elif name =='ITV2':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/itv2'
		else:
			url = 'http://itv2liveios-i.akamaihd.net/hls/live/203495/itvlive/ITV2MN/master_Main1800.m3u8'
	elif name =='DAVE':
			url = 'http://tvplayer.com/watch/dave'
	elif name =='ITV3':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/itv3'
		else:
			url = 'http://itv3liveios-i.akamaihd.net/hls/live/207262/itvlive/ITV3MN/master_Main1800.m3u8'
	elif name =='ITV4':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/itv4'
		else:
			url = 'http://itv4liveios-i.akamaihd.net/hls/live/207266/itvlive/ITV4MN/master_Main1800.m3u8'
	elif name =='ITVBE':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/itvbe'
		else:
			url = 'http://itvbeliveios-i.akamaihd.net/hls/live/219078/itvlive/ITVBE/master_Main1800.m3u8'
	elif name =='ITV11':
			url = 'http://www.filmon.com/channel/itv-plus-1'
	elif name =='ITV21':
			url = 'http://www.filmon.com/channel/itv2-plus-1'
	elif name =='ITV31':
			url = 'http://www.filmon.com/channel/itv3-plus-1'
	elif name =='ITV41':
			url = 'http://www.filmon.com/channel/itv4-plus-1'
	elif name =='BBC4':
			url = 'http://www.filmon.com/channel/cbeebiesbbc-four'
	elif name =='CBSR':
			url = 'http://www.filmon.com/channel/cbs-reality'
	elif name =='CBSR1':
			url = 'http://www.filmon.com/channel/cbs-reality1'
	elif name =='CBSA':
			url = 'http://www.filmon.com/channel/cbs-action'
	elif name =='5USA':
			url = 'http://www.filmon.com/channel/5usa'
	elif name =='DRAMA':
			url = 'http://tvplayer.com/watch/drama'
	elif name =='HOME':
			url = 'http://tvplayer.com/watch/home'
	elif name =='E4':
			url = 'http://www.filmon.com/channel/e4'
	elif name =='MORE4':
			url = 'http://www.filmon.com/channel/more4'
	elif name =='QUEST':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/quest'
		else:
			url = 'http://tvplayer.com/watch/quest'
	elif name =='REALLY':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/really'
		else:
			url = 'http://tvplayer.com/watch/really'
	elif name =='TRUTV':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/tru-tv'
		else:
			url = 'http://tvplayer.com/watch/trutv'
	elif name =='TRAVCHANNEL':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/travel-channel1'
		else:
			url = 'http://tvplayer.com/watch/travelchannel'
	elif name =='FOODNET':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/food-network'
		else:
			url = 'http://tvplayer.com/watch/foodnetwork'
	elif name =='FOODNET1':
			url = 'http://www.filmon.com/channel/food-network-plus-1'
	elif name =='FASHTV':
			url = 'http://www.filmon.com/channel/fashion-tv'
	elif name =='YESTERDAY':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/yesterday'
		else:
			url = 'http://tvplayer.com/watch/yesterday'
	elif name =='YESTERDAY1':
			url = 'http://tvplayer.com/watch/yesterday1'
	elif name =='QVC':
			url = 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi5/3/prog_index.m3u8'
	elif name =='QVCS':
			url = 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi8/3/prog_index.m3u8'	
	elif name =='QVCE':
			url = 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi5/1/prog_index.m3u8'
	elif name =='QVCP':
			url = 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi1/3/prog_index.m3u8'
	elif name =='QVCB':
			url = 'http://llnw.live.qvc.simplestream.com/hera/remote/qvcuk_primary_sdi6/3/prog_index.m3u8'	
	elif name =='JEWL':
			url = 'https://d2hee8qk5g0egz.cloudfront.net/live/tjc_sdi1/bitrate1.isml/bitrate1-audio_track=64000-video=1800000.m3u8'
	elif name =='CBBC':
			url = 'http://www.filmon.com/channel/cbbc'
	elif name =='CBEEB':
		a = xbmcgui.Dialog().select('Select a link',['SD','HD'])
		if a ==0:
			url = 'http://www.filmon.com/channel/cbeebies'
		else:
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/cbeebies_hd.m3u8'
	elif name =='CITV':
			url = 'http://citvliveios-i.akamaihd.net/hls/live/207267/itvlive/CITVMN/master_Main1800.m3u8'
	elif name =='POP':
			url = 'http://www.filmon.com/channel/pop'
	elif name =='TPOP':
			url = 'http://www.filmon.com/channel/tiny-pop'
	elif name =='SNEWS':
			url = 'plugin://plugin.video.youtube/play/?video_id=y60wDzZt8yg'
	elif name =='BNEWS':
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_news24.m3u8'
	elif name =='FILM4':
			url = 'http://www.filmon.com/channel/film-4'
	elif name =='ALBA':
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/bbc_alba.m3u8'
	elif name =='S4C':
			url = 'http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/hls_tablet/ak/s4cpbs.m3u8'
	else:
		    url = 'url'
	
	
	if 'filmon' in url:
		url = liveresolver.resolve(url)
	elif 'tvplayer' in url:
		url = tvplayer.resolve_tvplayer(url)
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		
def musicsearch(url):
		if url == 'search':
			kb = xbmc.Keyboard ('', 'Enter Your Favourite Song or Artist', False)
			kb.doModal()
			if (kb.isConfirmed()):
				query = kb.getText()
				query = (query.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
				open  = OPEN_URL(music+query)
				all   = regex_get_all(open,'<li><div class="song-list"','</li>')
				for a in all:
					name = regex_from_to(a,'title="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'data-original="','"')
					url  = regex_from_to(a,'http://woodmp3.com/download/','/')
					addDir(name,url,62,icon,fanart,'')
		else:
				xbmc.log(str(url))
				open  = OPEN_URL(url)
				all   = regex_get_all(open,'<li><div class="song-list"','</li>')
				for a in all:
					name = regex_from_to(a,'title="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'data-original="','"')
					url  = regex_from_to(a,'http://woodmp3.com/download/','/')
					addDir(name,url,62,icon,fanart,'')
			
def musicindex(url):
	open  = OPEN_URL(url)
	all   = regex_get_all(open,'<div class="song-list"','<i class="fa fa-download">')
	for a in all:
		name = regex_from_to(a,'title="','"').replace('Free','').replace('mp3','')
		icon = regex_from_to(a,' src="','"')
		url  = regex_from_to(a,'none;"><a href="','"')
		addDir(name,url,63,icon,fanart,'')			
def musicresolve(url):
	url  = 'http://www.youtubeinmp3.com/widget/button/?video=https://www.youtube.com/watch?v=%s&color=008000'%url
	open = OPEN_URL(url)
	mp3  = regex_from_to(open,'downloadButton" href="','"')
	xbmc.log(str(mp3))
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str('http://www.youtubeinmp3.com'+mp3))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
		

def replacemalicious():		
        target = xbmc.translatePath('special://home/addons/plugin.video.exodus/resources/lib/modules/sources.py')
        home = xbmc.translatePath('special://home/addons/script.module.streamhub/resources/')
        if os.path.exists(target):
            file = open(os.path.join(home, 'exodusclean.py'))
            data = file.read()
            file.close()
            file = open(target,"w")
            file.write(data)
            file.close()
			
def bbcmusicindex(url):
	open = OPEN_URL(url)
	all = regex_get_all(open,'<div class="cht-entry-wrapper">','<div class="cht-entry-status">')
	if 'singles' in url:
		for a in all:
			num  = regex_from_to(a,'<div class="cht-entry-position">','<').strip()
			name = regex_from_to(a,'data-title="','"').replace('||','-').replace('&amp;','')
			name = '[COLOR red]%s[/COLOR] | %s'%(num,name)
			icon = regex_from_to(a,'         src="','"')
			url  = 'http://woodmp3.com/search/'+(name.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
			url  = regex_from_to(url,']-','$').replace('(','ABCD')
			url  = re.sub(r'ABCD(.*?)$','',url)
			addDir(name,'http://woodmp3.com/search/'+re.sub('-$','',url),63,icon,fanart,'')
			
			
def top40(url):
	open = OPEN_URL(url)
	part  = regex_from_to(open,'<table align=center','<BR><BR>')
	all   = regex_get_all(part,'big>&nbsp;&nbsp;&nbsp;','font class=small>')
	for a in all:
		name = regex_from_to(a,'hspace=5 border=0>','<')
		addDir(name,'url',4,icon,fanart,'')
		
def radio():
	open =OPEN_URL('https://raw.githubusercontent.com/sClarkeIsBack/StreamHub/master/Links/RADIO.xml')
	all = regex_get_all(open,'<item>','</item>')
	for a in all:
		name = regex_from_to(a,'<title>','</title>')
		url  = regex_from_to(a,'<link>','</link>')
		icon = regex_from_to(a,'<thumbnail>','</thumbnail>')
		addDir(name,url,999,icon,fanart,'')

def UKNowMusic(url):
	if 'Live-Lounge' in url:
		desc = 'BBCL'
	else:
		desc = 'url'
	if url == 'NOW':
		d    = xbmcgui.Dialog().select('Choose a Country', ['UK Version', 'US Version'])
		if d==0:
			url = 'https://www.discogs.com/label/266040-Now-Thats-What-I-Call-Music!-UK'
		elif d==1:
			url = 'https://www.discogs.com/label/266110-Now-Thats-What-I-Call-Music!-US'
		else:
			return
	
	
	if '-US' in url:
		country = 'USA'
	else:
		country = 'UK'
	open = OPEN_URL(url)
	all  = regex_get_all(open,'td class="artist">','<td class="actions">')
	for a in all:
		url   = regex_from_to(a,' <a href="','"')
		title = regex_from_to(a,'[0-9]">','<').replace('&#39;',"'")
		year  = regex_from_to(a,'Year: ">','<')
		if not 'DVD' in title:
			xbmc.log(str(url))
			addDir('[COLOR red]%s[/COLOR] | [COLOR red]%s[/COLOR]'%(country,year)+' | '+title,url,71,icon,fanart,desc)
			
def UKNowMusic2(url,description):
	open = OPEN_URL('https://www.discogs.com'+url)
	all = regex_get_all(open,'<td class="tracklist_track_artists">','<tr class=" tracklist_track track"')
	for a in all:
		artist = re.compile('a href=".*?">(.*?)<',re.DOTALL).findall(a)
		artist = str(artist).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		
		track  = regex_from_to(a,'itemprop="name">','<')
		track  = str(track).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		if 'BBCL' in description:
			url = 'bbc+radio+1+live+lounge %s %s'%(artist,track)
		else:
			url    = '%s %s'%(artist,track)
		url    = str(url).replace(' ','-').replace(':','').lower()
		addDir('%s - %s'%(artist,track),'http://woodmp3.com/search/'+url,63,icon,fanart,'')
		

		
		
		
def WORLDIPTV():
	open = bypass.get('http://freeworldwideiptv.com').content
	all  = regex_get_all(open,'<div class="post-date-ribbon">','</header>')
	for a in all:
		url  = regex_from_to(a,'href="','"').replace('https://','http://')
		name = regex_from_to(a,'title="','"')
		addDir(name,url,83,icon,fanart,'')
		
def WORLDIPTVM3U(url):
	try:
		open = bypass.get(url).content
		m3u  = regex_from_to(open,'Link :</strong>','</p>').strip()
		open = bypass.get(str(m3u).replace('&amp;','&')).content
		all  = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
		for name,url in all:
			addDir(name,url,1000,icon,fanart,'')
	except:
		xbmcgui.Dialog().notification('[COLOR red][B]StreamHub[/B][/COLOR]','Oops, This M3U Is Down')
		return
		
		
def WORLDIPTV2():
	open = OPEN_URL_RAW('http://iptvlivestream.com/iptv/')
	all  = regex_get_all(open,'<div class="post-headline"','</div>')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'href="','"')
		if not 'FREE M3U' in name:
			if not 'FREE BEINSPORTS' in name:
				if not 'FREE SPORTS IPTV' in name:
					if not 'FREE ARABIC' in name:
						if not 'FREE GERMANY' in name:
							addDir(name,url,87,icon,fanart,'')
		
def WORLDIPTVM3U2(url):
		open = OPEN_URL_RAW(url)
		m3u  = regex_from_to(open,'<pre>','\n').replace('https:','http:')
		xbmc.log(str(m3u))
		open = OPEN_URL_RAW(str(m3u).replace('&amp;','&'))
		all  = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
		for name,url in all:
			addDir(name,url,1000,icon,fanart,'')

		
		
		
		
		
		
		
def EXABYTE():
	addDir('[COLOR lime][B]==EXABYTE TV[/B]==[/COLOR]','http://www.exabytetv.info/UK.m3u',980898,icon,fanart,'')
	addDir('UK Server','http://www.exabytetv.info/UK.m3u',86,icon,fanart,'')
	addDir('US Server','http://www.exabytetv.info/USA.m3u',86,icon,fanart,'')
	addDir('DE Server','http://www.exabytetv.info/DEU.m3u',86,icon,fanart,'')
	addDir('ALB Server','http://www.exabytetv.info/ALB.m3u',86,icon,fanart,'')
	addDir('NLD Server','http://www.exabytetv.info/NLD.m3u',86,icon,fanart,'')
	addDir('SAU Server','http://www.exabytetv.info/SAU.m3u',86,icon,fanart,'')
	addDir('TUR Server','http://www.exabytetv.info/TUR.m3u',86,icon,fanart,'')
		
		
def listEXABYTE(url):
	open   = OPEN_URL_RAW(url)
	all    = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in all:
		addDir(name,url,1000,icon,fanart,'')
		
def OPEN_URL_RAW(url):
	req = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
	response = urllib2.urlopen(req)
	html = response.read()
	response.close()
	return html
	
	

def playf4m(url, name):
            try:
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
            except:
                pass


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

elif mode==2:
	INDEX2(url)

elif mode==3:
	LINKS(url)

elif mode==6:
	EPIS(url)

elif mode==7:
	LINKS2(url,description)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)

elif mode==9:
	GENRE(url)

elif mode==10:
	COUNTRY(url)

elif mode==11:
	YEAR(url)
	
elif mode==12:
	INDEX3(url)
	
elif mode==13:
	resolve(name,url,iconimage,description)
	
elif mode==19:
	putlockerhdread(url)
	
elif mode==15:
	putlockerhdplay(url)
	
elif mode==24:
	xxx(url)
	
elif mode==25:
	LiveTV()
	
elif mode==26:
	opencartooncrazy(url)
	
elif mode==27:
	resolvexxx(url)
	
elif mode==99:
	xxxgenre(url)
	
elif mode==30:
	resolvecartooncrazy(url,icon)
	
elif mode==31:
	xxxCAT()
	
elif mode==32:
	CartooncrazyList()
	
elif mode==33:
	listgenre(url)
	
elif mode==34:
	CartooncrazysubList(url)
	
elif mode==35:
	documentary(url)
	
elif mode==36:
	resolvedoc(url)
	
elif mode==37:
	MOV2CAT()
	
elif mode==43:
	wweopen(url)
	
elif mode==44:
	playwwe(url,description)
	
elif mode==45:
	wwepages(url)
	
elif mode==46:
	resolvetwentyfourseven(url,icon)
	
elif mode==47:
	opentwentyfourseven(url)

elif mode==48:
	tvlist(url)

elif mode==49:
	TVREQUESTCAT()
	
elif mode==50:
	TVREQUESTCATPLAY(name,url,icon)

elif mode==51:
	toongetlist(url)
	
elif mode==52:
	toongeteps(url)
	
elif mode==53:
	toongetresolve(name,url)

elif mode==56:
	FAMILYCAT()

elif mode==57:
	disneymoviesresolve(url)
	
elif mode==58:
	disneymovies(url)
	
elif mode==59:
	playresolved(url)
	
elif mode==60:
	tvguidepick(name)

elif mode==61:
	setxxxpass()
	
elif mode==62:
	musicresolve(url)
	
elif mode==63:
	musicsearch(url)
	
elif mode==64:
	MUSICCAT()
	
elif mode==65:
	musicindex(url)
	
elif mode==66:
	bbcmusicresolve(name)
	
elif mode==67:
	bbcmusicindex(url)
	
elif mode==68:
	TOPMUSICAT()
	
elif mode==69:
	radio()
	
elif mode==70:
	UKNowMusic(url)
	
elif mode==71:
	UKNowMusic2(url,description)
	
elif mode==72:
	MUSICCOL()
	
elif mode==73:
	xbmc.executebuiltin('XBMC.RunScript(script.module.streamhub)')
	
elif mode==74:
	kisscartoonindex(url)
	
elif mode==75:
	kisscartoonresolve(url)

elif mode==76:
	kisscartoongenre(url)
	
elif mode==77:
	FAMILYMOVIESCAT()
	
elif mode==78:
	kisscartoonyear(url)
	
elif mode==79:
	NOVAMOVIES(url)
	
elif mode==80:
	NOVAMOVIERESOLVE(url)

elif mode==81:
	NOVAMOVIESGENRE(url)
	
elif mode==82:
	NOVAMOVIESSEARCH()
	
elif mode==83:
	WORLDIPTVM3U(url)
	
elif mode==84:
	WORLDIPTV()
	
elif mode==85:
	EXABYTE()
	
elif mode==86:
	listEXABYTE(url)
	
elif mode==87:
	WORLDIPTVM3U2(url)
	
elif mode==88:
	WORLDIPTV2()

elif mode==98:
	xxxstars(url)
	
elif mode==100:
	MovieCAT()
	
elif mode==999:
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


elif mode==1000:
	url = str(url).replace('\t','').replace('\r','').replace('\n','').replace(' ','%20')
	try:
		playf4m(url,name)
	except:
		pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))