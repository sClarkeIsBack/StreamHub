# -*- coding: utf-8 -*-




import json,urlparse

from resources.lib.zmodules import client


def getTrakt(url, post=None):
    try:
        url = urlparse.urljoin('http://api-v2launch.trakt.tv', url)

        headers = {'Content-Type': 'application/json', 'trakt-api-key': 'c029c80fd3d3a5284ee820ba1cf7f0221da8976b8ee5e6c4af714c22fc4f46fa', 'trakt-api-version': '2'}

        if not post == None: post = json.dumps(post)

        result = client.request(url, post=post, headers=headers)
        return result
    except:
        pass


def getMovieTranslation(id, lang):
    url = '/movies/%s/translations/%s' % (id, lang)
    try: return json.loads(getTrakt(url))[0]['title'].encode('utf-8')
    except: pass


def getTVShowTranslation(id, lang):
    url = '/shows/%s/translations/%s' % (id, lang)
    try: return json.loads(getTrakt(url))[0]['title'].encode('utf-8')
    except: pass


