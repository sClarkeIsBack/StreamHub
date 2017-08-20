import zipfile, xbmcaddon, xbmc, uservar
from resources.libs import wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDON          = wiz.addonId(ADDON_ID)
KEEPFAVS       = wiz.getS('keepfavourites')
KEEPSOURCES    = wiz.getS('keepsources')
KEEPPROFILES   = wiz.getS('keepprofiles')
KEEPADVANCED   = wiz.getS('keepadvanced')
LOGFILES       = ['xbmc.log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log', 'Thumbs.db', '.DS_Store']

def all(_in, _out, dp=None, ignore=None):
	if dp: return allWithProgress(_in, _out, dp, ignore)
	else: return allNoProgress(_in, _out, ignore)

def allNoProgress(_in, _out, ignore):
	try:
		zin = zipfile.ZipFile(_in, 'r')
		zin.extractall(_out)
	except Exception, e:
		print str(e)
		return False
	return True

def allWithProgress(_in, _out, dp, ignore):
	count = 0; errors = 0; error = ''; update = 0;
	try:
		zin = zipfile.ZipFile(_in,  'r')
	except Exception, e:
		errors += 1; error += '%s\n' % e
		wiz.log('%s / %s' % (Exception, e))
		return '%d/%d/%s' % (update, errors, error)
	nFiles = float(len(zin.namelist()))
	zipit = str(_in).replace('\\', '/').split('/'); zname = zipit[len(zipit)-1].replace('.zip', '')
	for item in zin.infolist():
		count += 1; update = int(count / nFiles * 100);
		file = str(item.filename).split('/')
		x = len(file)-1
		if file[x] == 'sources.xml' and file[x-1] == 'userdata' and KEEPSOURCES == 'true': dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		elif file[x] == 'favourites.xml' and file[x-1] == 'userdata' and KEEPFAVS == 'true': dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		elif file[x] == 'profiles.xml' and file[x-1] == 'userdata' and KEEPPROFILES == 'true': dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		elif file[x] == 'advancedsettings.xml' and file[x-1] == 'userdata' and KEEPADVANCED == 'true': dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		elif file[x] in LOGFILES: dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		elif not str(item.filename).find(ADDON_ID) == -1 and ignore == None: dp.update(update, '' ,'Skipping: [COLOR yellow]%s[/COLOR]' % item.filename); wiz.log("Skipping: %s" % item.filename)
		else:
			dp.update(update, '[COLOR dodgerblue]%s[/COLOR] [Errors:%s]' % (zname, errors),'Extracting: [COLOR yellow]%s[/COLOR]' % item.filename)
			try:
				zin.extract(item, _out)
			except Exception, e:
				errors += 1; error += '%s\n' % e
				wiz.log('%s / %s / %s' % (Exception, e, item.filename))
				pass
	return '%d/%d/%s' % (update, errors, error)