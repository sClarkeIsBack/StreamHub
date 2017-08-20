import xbmcgui
import urllib
import time
import uservar
import wizard as wiz

ADDONTITLE     = uservar.ADDONTITLE
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2

def download(url, dest, dp = None):
	if not dp:
		dp = xbmcgui.DialogProgress()
		dp.create(ADDONTITLE ,"Downloading Content",' ', ' ')
	dp.update(0)
	start_time=time.time()
	urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
	try: 
		percent = min(numblocks * blocksize * 100 / filesize, 100) 
		currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
		kbps_speed = numblocks * blocksize / (time.time() - start_time) 
		if kbps_speed > 0 and not percent == 100: 
			eta = (filesize - numblocks * blocksize) / kbps_speed 
		else: 
			eta = 0
		kbps_speed = kbps_speed / 1024 
		total = float(filesize) / (1024 * 1024) 
		mbs = '[COLOR %s][COLOR %s]%.02f[/COLOR] MB of [COLOR %s]%.02f[/COLOR] MB[/COLOR]' % (COLOR2, COLOR1, currently_downloaded, COLOR1, total) 
		e = '[COLOR %s]Speed: [COLOR %s]%.02f [/COLOR]Kb/s ' % (COLOR2, COLOR1, kbps_speed)
		e += 'ETA: [COLOR '+COLOR1+']%02d:%02d[/COLOR][/COLOR]' % divmod(eta, 60)
		dp.update(percent, mbs, e)
		if dp.iscanceled(): 
			raise Exception("Canceled")
			dp.close()
	except Exception, e:
		wiz.log("ERROR Downloading: %s" % str(e))
		return str(e)