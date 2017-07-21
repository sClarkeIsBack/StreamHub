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
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''



import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['tinydl.com']
        self.base_link = 'http://tinydl.com'
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

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            title = (title).replace(' ','+')
			
            url   = 'http://openhub.pw/?s='+title.lower()

            open  = client.request(url)
		
            match = re.compile('<div class="result-item">(.+?)</article>',re.DOTALL).findall(open)[0]
			
            url   = re.compile('href="(.+?)"').findall(match)[0]
            year  = re.compile('<span class="year">(.+?)<').findall(match)[0]
            if title in match.lower():
			
				open = client.request(url)
				
				url  = re.compile('iframe class.+?src="(.+?)"').findall(open)[0]
				qual = re.compile('<span class="qualityx">(.+?)<').findall(open)[0]
				
				if '720' in qual or 'hd' in qual or 'HD' in qual:
					qual = 'HD'
				elif '1080' in qual:
					qual = '1080p'
				else:
					qual = 'SD'
                    sources.append({'source': 'openload', 'quality': qual, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


