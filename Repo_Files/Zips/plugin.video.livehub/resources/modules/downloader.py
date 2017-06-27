import xbmcgui
import urllib
import time
from urllib import FancyURLopener
import sys

class MyOpener(FancyURLopener):
	version = 'Live Hub'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open

def download(url, dest, dp = None):
    start_time=time.time()
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def auto(url, dest, dp = None):
	start_time=time.time()
	urlretrieve(url, dest, lambda nb, bs, fs: _pbhookauto(nb, bs, fs, dp, start_time))

def _pbhookauto(numblocks, blocksize, filesize, url, dp):
	none = 0

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB[/COLOR] of %.02f MB' % (currently_downloaded, total)
            e = 'Speed: [COLOR lime]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            e += 'ETA: [COLOR yellow]%02d:%02d' % divmod(eta, 60) + '[/COLOR]'
        except: 
            percent = 100 
			

def unzip(zip,dest):
	import zipfile
	zip_ref = zipfile.ZipFile(zip, 'r')
	zip_ref.extractall(dest)
	zip_ref.close()