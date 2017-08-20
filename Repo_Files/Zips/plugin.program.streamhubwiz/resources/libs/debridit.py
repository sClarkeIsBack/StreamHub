import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND         = os.path.join(USERDATA,  'addon_data')
REALFOLD       = os.path.join(ADDONDATA, 'debrid')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPTRAKT      = wiz.getS('keepdebrid')
REALSAVE       = wiz.getS('debridlastsave')
ORDER          = ['exodus', 'specto', 'url']

DEBRIDID = { 
	'exodus': {
		'name'     : 'Exodus',
		'plugin'   : 'plugin.video.exodus',
		'saved'    : 'realexodus',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodus', 'fanart.jpg'),
		'file'     : os.path.join(REALFOLD, 'exodus_debrid'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodus', 'settings.xml'),
		'default'  : 'realdebrid.id',
		'data'     : ['realdebrid.auth', 'realdebrid.id', 'realdebrid.secret', 'realdebrid.token', 'realdebrid.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.exodus/?action=rdAuthorize)'},
	'specto': {
		'name'     : 'Specto',
		'plugin'   : 'plugin.video.specto',
		'saved'    : 'realspecto',
		'path'     : os.path.join(ADDONS, 'plugin.video.specto'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.specto', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.specto', 'fanart.jpg'),
		'file'     : os.path.join(REALFOLD, 'specto_debrid'),
		'settings' : os.path.join(ADDOND, 'plugin.video.specto', 'settings.xml'),
		'default'  : 'realdebrid_client_id',
		'data'     : ['realdebrid_auth', 'realdebrid_token', 'realdebrid_refresh', 'realdebrid_client_id', 'realdebrid_client_secret'],
		'activate' : 'RunPlugin(plugin://plugin.video.specto/?action=realdebridauth)'},
	'url': {
		'name'     : 'URL Resolver',
		'plugin'   : 'script.module.urlresolver',
		'saved'    : 'urlresolver',
		'path'     : os.path.join(ADDONS, 'script.module.urlresolver'),
		'icon'     : os.path.join(ADDONS, 'script.module.urlresolver', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
		'file'     : os.path.join(REALFOLD, 'url_debrid'),
		'settings' : os.path.join(ADDOND, 'script.module.urlresolver', 'settings.xml'),
		'default'  : 'RealDebridResolver_client_id',
		'data'     : ['RealDebridResolver_enabled', 'RealDebridResolver_priority', 'RealDebridResolver_autopick', 'RealDebridResolver_token', 'RealDebridResolver_refresh', 'RealDebridResolver_client_id', 'RealDebridResolver_client_secret'],
		'activate' : 'RunPlugin(plugin://script.module.urlresolver/?mode=auth_rd)'}
}

def debridUser(who):
	user=None
	if DEBRIDID[who]:
		if os.path.exists(DEBRIDID[who]['path']):
			try:
				add = wiz.addonId(DEBRIDID[who]['plugin'])
				user = add.getSetting(DEBRIDID[who]['default'])
			except:
				pass
	return user

def debridIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(REALFOLD):  os.makedirs(REALFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(DEBRIDID[log]['path']): updateDebrid(do, log)
			else: wiz.log('[Real Debrid Data] %s(%s) is not installed' % (DEBRIDID[log]['name'],DEBRIDID[log]['plugin']))
		wiz.setS('debridlastsave', str(THREEDAYS))
	else:
		if DEBRIDID[who]:
			if os.path.exists(DEBRIDID[who]['path']):
				updateDebrid(do, who)
		else: wiz.log('[Real Debrid Data] Invalid Entry: %s' % who)

def clearSaved(who):
	if who == 'all':
		for debrid in DEBRIDID:
			file = DEBRIDID[debrid]['file']
			if os.path.exists(file): os.remove(file)
			wiz.LogNotify(DEBRIDID[debrid]['name'],'Real Debrid Data: [COLOR green]Removed![/COLOR]', 2000, DEBRIDID[debrid]['icon'])
	elif DEBRIDID[who]:
		file = DEBRIDID[who]['file']
		if os.path.exists(file): os.remove(file)
		wiz.LogNotify(DEBRIDID[who]['name'],'Real Debrid Data: [COLOR green]Removed![/COLOR]', 2000, DEBRIDID[who]['icon'])
	xbmc.executebuiltin('Container.Refresh')
		
def updateDebrid(do, who):
	file      = DEBRIDID[who]['file']
	settings  = DEBRIDID[who]['settings']
	data      = DEBRIDID[who]['data']
	addonid   = wiz.addonId(DEBRIDID[who]['plugin'])
	saved     = DEBRIDID[who]['saved']
	default   = DEBRIDID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = DEBRIDID[who]['name']
	icon      = DEBRIDID[who]['icon']

	if do == 'update':
		if not user == '':
			with open(file, 'w') as f:
				for debrid in data: f.write('<debrid>\n\t<id>%s</id>\n\t<value>%s</value>\n</debrid>\n' % (debrid, addonid.getSetting(debrid)))
			f.close()
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'Real Debrid Data: [COLOR green]Saved![/COLOR]', 2000, icon)
		else: wiz.LogNotify(name,'Real Debrid Data: [COLOR red]Not Registered![/COLOR]', 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<debrid><id>(.+?)</id><value>(.+?)</value></debrid>').findall(g)
			if len(match) > 0:
				for debrid, value in match:
					addonid.setSetting(debrid, value)
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'Real Debrid: [COLOR green]Restored![/COLOR]', 2000, icon)
		#else: wiz.LogNotify(name,'Real Debrid Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings))
		if os.path.exists(settings):
			f = open(settings,"r"); lines = f.readlines(); f.close()
			f = open(settings,"w")
			for line in lines:
				match = re.compile('<setting.+?id="(.+?)".+?/>').findall(line)
				if len(match) == 0: f.write(line)
				elif match[0] not in data: f.write(line)
				else: wiz.log('[Debrid Clear Addon] Removing Line: %s' % line)
			f.close()
			wiz.LogNotify(name,'Addon Data: [COLOR green]Cleared![/COLOR]', 2000, icon)
		else: wiz.LogNotify(name,'Addon Data: [COLOR red]Clear Failed![/COLOR]', 2000, icon)
	xbmc.executebuiltin('Container.Refresh')

def autoUpdate(who):
	if who == 'all':
		for log in DEBRIDID:
			if os.path.exists(DEBRIDID[log]['path']):
				autoUpdate(log)
	elif DEBRIDID[who]:
		if os.path.exists(DEBRIDID[who]['path']):
			u  = debridUser(who)
			su = wiz.getS(DEBRIDID[who]['saved'])
			n = DEBRIDID[who]['name']
			if u == None or u == '': return
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "Would you like to save the Real Debrid data for %s?" % n, "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
					debridIt('update', who)

def importlist(who):
	if who == 'all':
		for log in DEBRIDID:
			if os.path.exists(DEBRIDID[log]['file']):
				importlist(log)
	elif DEBRIDID[who]:
		if os.path.exists(DEBRIDID[who]['file']):
			d  = DEBRIDID[who]['default']
			sa = DEBRIDID[who]['saved']
			su = wiz.getS(sa)
			n  = DEBRIDID[who]['name']
			f  = open(DEBRIDID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<debrid><id>%s</id><value>(.+?)</value></debrid>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "Would you like to import the Real Debrid data for %s?" % n, "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)))
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)))
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)))
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)))

def activateDebrid(who):
	if DEBRIDID[who]:
		if os.path.exists(DEBRIDID[who]['path']): 
			act     = DEBRIDID[who]['activate']
			addonid = wiz.addonId(DEBRIDID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(DEBRIDID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % DEBRIDID[who]['name'])
	else: 
		xbmc.executebuiltin('Container.Refresh')
		return
	check = 0
	while debridUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	xbmc.executebuiltin('Container.Refresh')