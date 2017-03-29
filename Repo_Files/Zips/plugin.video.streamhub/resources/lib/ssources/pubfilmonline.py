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


import re,urllib,urlparse,requests

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client
from resources.lib.smodules import debrid
from resources.lib import cfscrape

scraper = cfscrape.create_scraper()



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['pubfilmonline.net']
        self.base_link = 'http://pubfilmonline.net'
        self.search_link = 'http://pubfilmonline.net/?s='


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return 


    def sources(self, url, hostDict, hostprDict):
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			
            open  = scraper.get(self.search_link+title).content
			
            match = regex_from_to(open,'<article>','</article>')
            movie = regex_from_to(match,'<a href="','"')
            open  = scraper.get(movie).content
            qual  = regex_from_to(open,'<span class="qualityx">','<')
            if '1080' in qual:
				qual = '1080p'
            elif '720' in qual:
				qual = 'HD'
            elif 'cam' or 'CAM' or 'ts' in qual:
				qual = 'CAM'
            url   = regex_from_to(open,'"file":"','"').replace('\/','/')
            sources.append({'source': 'gvideo', 'quality': qual, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources


    def resolve(self, url):
        return url
		
def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
	
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


