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


import re,urllib,urlparse,base64

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client


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


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            ctitle = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			
            year  = data['year']

            title = (ctitle).replace(' ','+').lower()
            url   = 'https://flenix.net/index.php?do=search&story=%s&min_year=%s&max_year=%s'%(title,year,year)

            open  = client.request(url)
		
            match = re.compile(' onclick="openMovie(.+?)<div class="leftInfo">',re.DOTALL).findall(open)[0]
			
            url   = re.compile('href="(.+?)"').findall(match)[0]
            year  = re.compile('<span>(.+?)<').findall(match)[0]

            open = client.request(url)
			
            if ctitle in open:
				
				url  = re.compile('file:"(.+?)"').findall(open)[0]
				url  = 'http:'+url
				qual = re.compile('<div class="quality">(.+?)<').findall(open)[0]
				if '1080' in qual:
					qual = '1080p'
				elif 'HD' in qual or '720' in qual and not '1080' in qual:
					qual = 'HD'
				else:
					qual = 'SD'
				sources.append({'source': 'MP4', 'quality': qual, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
				return sources
        except:
            return sources


    def resolve(self, url):
        return url


