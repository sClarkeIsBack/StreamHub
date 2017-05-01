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


import re,urllib,urlparse,requests,time,json

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client
from resources.lib.smodules import directstream

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gomovies.to']
        self.base_link = 'https://gomovies.to'
        self.search_link = 'https://gomovies.to/movie/search/'


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
            title = str(title).replace(' ','+').replace(':','').lower()
            year  = data['year']

            open  = client.request('https://gomovies.to/movie/search/'+title)
			
            match = regex_from_to(open,'<div data-movie','</a>')
            movie = regex_from_to(match,'<a href="','"')
			
            data  = regex_from_to(match,'data-url="','"').replace('_load_info','_episodes')
            id    = regex_from_to(data,'episodes/','$')
			
            wyear  = client.request(data)
            wyear  = regex_from_to(wyear,'<div class="jt-info">','<')
			
            open  = client.request(data)
            js = json.loads(open)
	
            js = js['html']
			
            server   = regex_from_to(js,'<strong>Server 8</strong>','></div>')
			
            eid      = regex_from_to(server,'id="ep-','"')
            url    = 'https://gomovies.to/ajax/movie_token?eid=%s&mid=%s&_=%s'%(eid,id,time.time())
            
			
            open   = client.request(url)
	
            x      = regex_from_to(open,"x='","'")
            y      = regex_from_to(open,"y='","'")
	
            url    = 'https://gomovies.to/ajax/movie_sources/%s?x=%s&y=%s'%(eid,x,y)
            open   = client.request(url)
	
            try:
				url = regex_from_to(open,'"file":"','"')
				if not url=="" or '.srt' in url and year == wyear:
					sources.append({'source': 'gvideo', 'quality': directstream.googletag2(url) , 'language': 'en', 'url': str(url).replace('\/','/'), 'direct': False, 'debridonly': False})
            except:
				pass
			
            try:
				url = regex_from_to(open,'"label":"1080p","type":"mp4"},{"file":"','"')
				if not url=="" or '.srt' in url and year == wyear:
					sources.append({'source': 'gvideo', 'quality': directstream.googletag2(url) , 'language': 'en', 'url': str(url).replace('\/','/'), 'direct': False, 'debridonly': False})
            except:
				pass
            try:
				url = regex_from_to(open,'"label":"720p","type":"mp4"},{"file":"','"')
				if not url=="" or '.srt' in url and year == wyear:
					sources.append({'source': 'gvideo', 'quality': directstream.googletag2(url) , 'language': 'en', 'url': str(url).replace('\/','/'), 'direct': False, 'debridonly': False})
            except:
				pass
            try:
				url = regex_from_to(open,'"label":"480p","type":"mp4"},{"file":"','"')
				if not url=="" or '.srt' in url and year == wyear:
					sources.append({'source': 'gvideo', 'quality': directstream.googletag2(url) , 'language': 'en', 'url': str(url).replace('\/','/'), 'direct': False, 'debridonly': False})
            except:
				pass
				
            if not sources=="":
				return sources
            else:
				return


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


