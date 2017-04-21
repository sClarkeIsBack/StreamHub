import re,urllib,json,string,xbmc,urllib2,cookielib


def resolve_tvplayer(url):
  watchHtml=getUrl(str(url))
  channelid=re.findall('resourceId = "(.*?)"' ,watchHtml)[0]
  validate=re.findall('var validate = "(.*?)"' ,watchHtml)[0]
       
  cj = cookielib.LWPCookieJar()
  data = urllib.urlencode({'service':'1','platform':'website','token':'null','validate':validate ,'id' : channelid})
  headers=[('Referer','http://tvplayer.com/watch/'),('Origin','http://tvplayer.com'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
  retjson=getUrl("http://api.tvplayer.com/api/v2/stream/live",post=data, headers=headers,cookieJar=cj);
  jsondata=json.loads(retjson)
    #    print cj
  cj = cookielib.LWPCookieJar()
  playurl1=jsondata["tvplayer"]["response"]["stream"]
  m3utext=getUrl(playurl1, headers=headers,cookieJar=cj);
        #playurl1=re.findall('(http.*)',m3utext)[-1]
  playurl=playurl1+'|Cookie=%s&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'%getCookiesString(cj)
  xbmc.log(str('**********'+playurl))
  return playurl
  
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;
	
def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString