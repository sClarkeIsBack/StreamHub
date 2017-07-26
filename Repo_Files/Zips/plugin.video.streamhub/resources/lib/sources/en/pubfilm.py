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
			
            title = (ctitle).replace(' ','+').replace(':','').replace('.','').lower()
            query = title + '+' + year
            r = client.request('https://pubfilmonline.net/?s='+query)
			
            all = regex_get_all(r,'<article>','</article>')
            for a in all:
				name = regex_from_to(a,'alt="','"')
				iyear  = regex_from_to(a,'year">','<')
				url   = regex_from_to(a,'href="','"')
				if ctitle.lower() in name.lower() and year == iyear:
			
					r      = client.request(url)
					
					all   = re.findall('{file.+?"(.+?)".+?label".+?"(.+?)"', r, re.I|re.DOTALL)
					for url, qual in all:
						if '720' in qual:
							qual = 'HD'
						elif '1080' in qual:
							qual = '1080p'
						else:
							qual = 'SD'
						sources.append({'source': 'gvideo', 'quality': qual, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
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