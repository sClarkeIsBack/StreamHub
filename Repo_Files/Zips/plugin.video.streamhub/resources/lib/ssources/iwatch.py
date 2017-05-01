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


####USED FROM SPECTO####


import re,urllib,urlparse,hashlib,string,time,json,base64,urlresolver

from resources.lib.smodules import cleantitle
from resources.lib.smodules import client
from resources.lib.smodules import cache
from resources.lib.smodules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwatchonline.cr']
        self.base_link = 'https://www.iwatchonline.cr'


    def movie(self, imdb, title, year):
            post = {'searchquery': title, 'searchin': '1'}
            post = urllib.urlencode(post)
            result = ''

            headers = {"Content-Type":"application/x-www-form-urlencoded", "Referer":'https://www.iwatchonline.cr/advance-search'}
            result = client.request('https://www.iwatchonline.cr/advance-search', post=post, headers=headers)
                        #if 'widget search-page' in str(result): break
            print("R",result)
            result = client.parseDOM(result, 'div', attrs = {'class': 'widget search-page'})[0]
            result = client.parseDOM(result, 'td')

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, 'a', ret='href')[-1], client.parseDOM(i, 'a')[-1]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = urlparse.urlparse(url).path
            url = url.encode('utf-8')
            return url

    def sources(self, url, hostDict, hostprDict):
            sources = []

            mylinks = []
			
            if url == None: return []

            result = ''
            headers = {"Referer":urlparse.urljoin('https://www.iwatchonline.cr', url)}
            r100 = client.request(urlparse.urljoin('https://www.iwatchonline.cr', url), output='extended', headers=headers)
            cookie = r100[4] ; headers = r100[3] ; result = r100[0]


            links = client.parseDOM(result, 'tr', attrs = {'id': 'pt.+?'})

            for i in links:
                    lang = re.compile('<img src=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[1]

                    if not 'English' in lang: raise Exception()

                    host = re.compile('<img src=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[0]
                    host = host.split('/')[-1]
                    host = host.split('.')[-3]
                    host = host.strip().lower()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if '>Cam<' in i or '>TS<' in i: quality = 'CAM'
                    #elif '>HD<' in i and host in hostDict: quality = 'HD'
                    else: quality = 'SD'

                    #if quality == 'HD' and not host in hosthdDict: raise Exception()
                    #if quality == 'SD' and not host in hostDict: raise Exception()

                    if '>3D<' in i: info = '3D'
                    else: info = ''

                    url = re.compile('href=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[0]
                    url = client.replaceHTMLCodes(url)

                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    if url.startswith('http'): url = urlparse.urlparse(url).path
                    if not url.startswith('http'): url = urlparse.urljoin('https://www.iwatchonline.cr', url)


                    url = url.encode('utf-8')
                    #control.log('########  IWATCH LINK url:%s  host:%s q:%s' % (url,host,quality))
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            return sources


    def resolve(self, url):
        open = client.request(url,output='headers')
        url = open['Refresh'].replace('0;url=','')
        return url


