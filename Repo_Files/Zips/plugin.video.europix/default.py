import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver,ssl
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from addon.common.addon import Addon
from addon.common.net import Net
from resources import control

addon_id   = 'script.module.streamhub'
selfAddon  = xbmcaddon.Addon(id=addon_id)
addon      = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
putlockerhd      = 'http://putlockerhd.co'
ccurl      = 'http://cartooncrazy.me'
s          = requests.session()
net        = Net()
ccurl      = 'http://cartooncrazy.me'
xxxurl     ='http://www.xvideos.com'
kidsurl    = base64.b64decode ('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NDbGFya2VJc0JhY2svU3RyZWFtSHViL21hc3Rlci9MaW5rcy9LaWRzL2tpZHNjb3JuZXIueG1s')
docurl     = 'http://documentaryheaven.com'
mov2       = 'http://zmovies.to'
wwe        = 'http://watchwrestling.in'
tv         = base64.b64decode ('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3NDbGFya2VJc0JhY2svU3RyZWFtSHViL21hc3Rlci9MaW5rcy8yNDcvMjQ3dHYueG1s')
proxy      = 'http://www.justproxy.co.uk/index.php?q='

def CAT():
	addDir('MOVIES','url',100,icon,fanart,'')
	addDir('MOVIES2','url',37,icon,fanart,'')
	addDir('KIDS SECTION',kidsurl,16,icon,fanart,'')
	addDir('XXX SECTION','URL',31,icon,fanart,'')
	addDir('DOCS',docurl+'/watch-online/',35,icon,fanart,'')
	addDir('24/7 TV',tv,48,icon,fanart,'')
	
def MovieCAT():
	addDir('RECENT MOVIES',putlockerhd+'/recent_movies',19,icon,fanart,'')
	addDir('COMEDY MOVIES',putlockerhd+'/comedy_movies',19,icon,fanart,'')
	addDir('CRIME MOVIES',putlockerhd+'/crime_movies',19,icon,fanart,'')
	addDir('WAR MOVIES',putlockerhd+'/war_movies',19,icon,fanart,'')
	addDir('ROMANCE MOVIES',putlockerhd+'/romance_movies',19,icon,fanart,'')
	addDir('MUSICAL MOVIES',putlockerhd+'/musical_movies',19,icon,fanart,'')
	addDir('SPORT MOVIES',putlockerhd+'/sport_movies',19,icon,fanart,'')
	addDir('KIDS MOVIES',putlockerhd+'/family_movies',19,icon,fanart,'')
	addDir('DOCUMENTARY MOVIES',putlockerhd+'/documentary_movies',19,icon,fanart,'')
	
def MOV2CAT():
	addDir('[COLOR red]R[/COLOR]ecently Added',mov2,38,icon,fanart,'')
	addDir('[COLOR red]G[/COLOR]enres',mov2+'/genres/',41,icon,fanart,'')
	addDir('[COLOR red]Y[/COLOR]ears',mov2+'/years/',41,icon,fanart,'')
	addDir('[COLOR red]S[/COLOR]earch','url',40,icon,fanart,'')
	
def TVREQUESTCAT():
	addDir('Everybody Loves Raymond','ELR',50,'http://www.gstatic.com/tv/thumb/tvbanners/184243/p184243_b_v8_ab.jpg','','')
	addDir('How i Met Your Mother','HIMYM',50,'http://www.gstatic.com/tv/thumb/tvbanners/9916255/p9916255_b_v8_aa.jpg','','')
	addDir('Naked And Afraid','NAA',50,'http://www.gstatic.com/tv/thumb/tvbanners/9974211/p9974211_b_v8_ad.jpg','','')
	addDir('The Walking Dead','TWD',50,'http://www.gstatic.com/tv/thumb/tvbanners/13176393/p13176393_b_v8_ab.jpg','','')
	addDir('[COLOR red][B]IF IT FAILS THE FIRST TIME CLICK IT AGAIN[/COLOR][/B]','url','','','','')
	

	
def xxxCAT():
	addDir("[COLOR orange]G[/COLOR][COLOR white]enre's[/COLOR]",xxxurl+'/a',99,icon,fanart,'')

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
	if mode==3 or mode==7 or mode==17 or mode==15 or mode==23 or mode==30 or mode==27 or mode ==36 or mode==39 or mode==50:
		liz.setProperty("IsPlayable","true")
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
	
def tvlist(url):
    thumb = ''
    art   = ''
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    addDir('[COLOR red][B]Requested 24/7 Shows[/B][/COLOR]','url',49,'','','')
    for name,url,icon in Regex:
		addDir(name,url,46,icon,fanart,'') 

def toonlist(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>.+?art>(.+?)</art>',re.DOTALL).findall(OPEN)
    for name,url,icon,fanart in Regex:
		addDir(name,url,18,icon,fanart,'')
	
def toon_get(url):
    OPEN = Open_Url(url)
    Regex = re.compile('&nbsp;&nbsp;<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(OPEN)
    for url,name in Regex:
            name = name.replace('&#8217;','')
            addDir(name,url,17,iconimage,fanart,'')
    np = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(OPEN)
    for url,name in np:
            if 'Next' in name:
                    addDir('[B][COLOR red]More >[/COLOR][/B]',url,2,iconimage,fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    xbmcplugin.endOfDirectory
	
def resolvetoons(name,url,iconimage,description):
    OPEN = Open_Url(url)
    url1=regex_from_to(OPEN,'Playlist 1</span></div><div><iframe src="','"')
    url2=regex_from_to(OPEN,'Playlist 2</span></div><div><iframe src="','"')
    url3=regex_from_to(OPEN,'Playlist 3</span></div><div><iframe src="','"')
    url4=regex_from_to(OPEN,'Playlist 4</span></div><div><iframe src="','"')
    try:
        play=urlresolver.HostedMediaFile(url1).resolve()
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
        liz.setProperty('IsPlayable','true')
        liz.setPath(str(play))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:
        play=urlresolver.HostedMediaFile(url2).resolve()
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
        liz.setProperty('IsPlayable','true')
        liz.setPath(str(play))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:
        play=urlresolver.HostedMediaFile(url3).resolve()
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
        liz.setProperty('IsPlayable','true')
        liz.setPath(str(play))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:
        play=urlresolver.HostedMediaFile(url4).resolve()
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
        liz.setProperty('IsPlayable','true')
        liz.setPath(str(play))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
	
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
		
def xxx(url):
        link = OPEN_URL(url)
        xxxadd_next_button(link)
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
					xbmc.log(str(nextp))
					addDir('[B][COLOR red]Next Page[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			return
			
def xxxgenre(url):
        link = passpopup(url)
        link = OPEN_URL(link)
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
    if 'saucy' in text:
       text = str(text).replace('saucy','/tags')
       return (str(xxxurl+text)).replace('%3a','').replace('%2f','')
    else:
        Msg="                                   Incorrect Password\n\n                            Password is available from\n                                [COLOR red]http://facebook.com/groups/streamhub[/COLOR]"
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('Attention', Msg)
        return False

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
	addDir('DOCUMENTARY MOVIES',putlockerhd+'/documentary_movies',19,icon,fanart,'')
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

if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodus'):
	targetfolder = xbmc.translatePath('special://home/addons/plugin.video.exodus/resources/lib/modules/')
	targetfile = open(os.path.join(targetfolder, 'sources.py'))
	targetread = targetfile.read()
	targetclose = targetfile.close()
	if 'mkodi' in targetread:
		replacemalicious()

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

elif mode==4:
	TV()

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
	
elif mode==16:
	toonlist(url)
	
elif mode==17:
	resolvetoons(name,url,iconimage,description)
	
elif mode==18:
	toon_get(url)
	
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
	
elif mode==98:
	xxxstars(url)
	
elif mode==100:
	MovieCAT()
	
elif mode==999:
	home()





xbmcplugin.endOfDirectory(int(sys.argv[1]))