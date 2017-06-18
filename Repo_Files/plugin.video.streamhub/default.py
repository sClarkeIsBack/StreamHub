# -*- coding: utf-8 -*-

import urlparse,sys,urllib



def check4update():
	import re,time,xbmc,xbmcgui
	from resources.lib.modules import client

	addonxml = xbmc.translatePath('special://home/addons/script.module.streamhub/addon.xml')
	file     = open(addonxml)
	data     = file.read()
	file.close()

	c_version = re.compile('" version="(.+?)"').findall(data)[0]

	html = client.request('https://raw.githubusercontent.com/sClarkeIsBack/StreamHub/master/Repo_Files/addons.xml')

	o_version = re.compile('script.module.streamhub.+?version="(.+?)"').findall(html)[0]
	if c_version < o_version:
		update = 'https://github.com/sClarkeIsBack/StreamHub/raw/master/Repo_Files/Zips/script.module.streamhub/script.module.streamhub-%s.zip'%o_version
		install(o_version,update)
		xbmc.executebuiltin("UpdateAddonRepos")
		xbmc.executebuiltin("UpdateLocalAddons")
		time.sleep(5)
		xbmcgui.Dialog().notification('[COLOR red]StreamHub[/COLOR]','Updated Successfully')
	
	
def install(vers,url):
    import xbmc,xbmcgui,os,re,time
    from resources.lib.modules import downloader2
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR red]StreamHub[/COLOR]","Installing Dependency Update v[COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    lib=os.path.join(path, 'content.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader2.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
    time.sleep(3)
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR red]StreamHub[/COLOR]","Installing Dependency Update Version [COLOR red]%s[/COLOR]"%vers,'', 'Please Wait')
    dp.update(0,"", "Installing... Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    unzip(lib,addonfolder,dp)
	
	
def unzip(_in, _out, dp):
	import zipfile
	__in = zipfile.ZipFile(_in,  'r')
	
	nofiles = float(len(__in.infolist()))
	count   = 0
	
	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok('[COLOR red]StreamHub[/COLOR]', 'Process was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update))
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False
		
	return True	
		
		


params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

fanart = params.get('fanart')

##########################################################################################################################

if action == None:
    check4update()
    from resources.lib.indexers import streamhub
    streamhub.indexer().root()

elif action == 'directory':
    from resources.lib.indexers import streamhub
    streamhub.indexer().get(url)

elif action == 'parental':
    from resources.lib.indexers import streamhub
    streamhub.indexer().parental_controls()

elif action == 'qdirectory':
    from resources.lib.indexers import streamhub
    streamhub.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import streamhub
    streamhub.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import streamhub
    streamhub.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import streamhub
    streamhub.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import streamhub
    streamhub.indexer().youtube(url, action)

elif action == 'play':
    from resources.lib.indexers import streamhub
    streamhub.player().play(url, content)

elif action == 'browser':
    from resources.lib.indexers import streamhub
    streamhub.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import streamhub
    streamhub.indexer().search()

elif action == 'addSearch':
    from resources.lib.indexers import streamhub
    streamhub.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import streamhub
    streamhub.indexer().delSearch()

elif action == 'queueItem':
    from resources.lib.zmodules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.zmodules import control
    control.openSettings()

elif action == 'urlresolverSettings':
    from resources.lib.zmodules import control
    control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
    from resources.lib.zmodules import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.zmodules import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.zmodules import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.zmodules import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.zmodules import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.zmodules import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.zmodules import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.zmodules import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.zmodules import trailer
    trailer.trailer().play(name)

elif action == 'clearCache':
    from resources.lib.zmodules import cache
    cache.clear()

##########################################################################################################################


elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try: import urlresolver
    except: pass
    urlresolver.display_settings()

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play2':
    from resources.lib.modules import sources
    sources.sources().play2(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)
