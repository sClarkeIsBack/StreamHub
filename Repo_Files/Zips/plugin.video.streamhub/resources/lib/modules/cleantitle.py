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


import re,unicodedata

from resources.lib.modules import client


def get(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def geturl(title):
    if title == None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    return title


def get_simple(title):
    if title == None: return
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title
	
	
def getsearch(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|-|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title == None: return
    title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ')
    return title


def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        return str( ''.join(c for c in unicodedata.normalize('NFKD', unicode( title.decode('utf-8') )) if unicodedata.category(c) != 'Mn') )
    except:
        return title


def local(title, imdb, lang):
    try:
        t = 'http://www.imdb.com/title/%s' % imdb
        t = client.request(t, headers={'Accept-Language': lang})
        t = client.parseDOM(t, 'title')[0]
        t = re.sub('\((?:.+?|)\d{4}.+', '', t).strip()
        t = normalize(t.encode("utf-8")) 
        return t
    except:
        return title



def movie(title):
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def tv(title):
    title = re.sub('\n|\s(|[(])(UK|US|AU|\d{4})(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def get(title):
    if title == None: return
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title

def query(title):
    if title == None: return
    title = title.replace('\'', ' ').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ')
    return title

def query2(title):
    if title == None: return
    title = title.replace('\'', '').replace('-','')
    return title

def query10(title):
    if title == None: return
    title = title.replace('\'', '').replace(':','').replace('.','').replace(' ','-').lower()
    return title

def geturl(title):
    if title == None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '+')
    title = title.replace('--', '-')
    title = title.replace('\'', '-')
    return title

def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        t = ''
        for i in title:
            c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))
            c = c.encode("ascii","ignore").strip()
            if i == ' ': c = i
            t += c

        return t.encode("utf-8")
    except:
        return title

def getsearch(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title).lower()
    title = ' '.join(title.split())
    return title