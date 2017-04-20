import os,re,sys,xbmc,json,base64,client,control,string,urllib,urlparse,shutil,xbmcplugin,xbmcgui,socket


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

def googletag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try: quality = quality[0]
    except: return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return '1080p'
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return 'HD'
    elif quality in ['35', '44', '135', '244', '94']:
        return 'SD'
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return 'SD'
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return 'SD'
    else:
        return []