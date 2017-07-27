# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,base64,xbmcaddon

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client

username = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Username')
password = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Password')

logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))
def log(text):
	file = open(logfile,"w+")
	file.write(str(text))



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['crazy4tv.com', 'crazy4ad.in']
        self.base_link = 'http://crazy4tv.com'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return
			
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []

			if url == None: return sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			
			year  = data['year']

			url = 'http://mediahubiptv.ddns.net:4545/enigma2.php?username=%s&password=%s&type=get_vod_streams&cat_id=0'%(username,password)
			
			r   = client.request(url,headers={'User-Agent':'sClarkeAddon'})
			
			all_cats = regex_get_all(r,'<channel>','</channel>')
			for a in all_cats:
				name = regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				if title.lower() in name.lower() and year in name:
					url  = regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					sources.append({'source': '[COLOR gold]Premium Server[/COLOR]', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
			return sources
        except:
			return sources


    def resolve(self, url):
        return url


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