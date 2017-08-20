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
TRAKTFOLD      = os.path.join(ADDONDATA, 'trakt')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPTRAKT      = wiz.getS('keeptrakt')
TRAKTSAVE      = wiz.getS('traktlastsave')
ORDER          = ['exodus', 'metalliq', 'salts', 'saltshd', 'velocity', 'velocitykids', 'meta', 'royalwe', 'specto', 'trakt']

TRAKTID = { 
	'exodus': {
		'name'     : 'Exodus',
		'plugin'   : 'plugin.video.exodus',
		'saved'    : 'exodus',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodus'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodus', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodus', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'exodus_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodus', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
		'activate' : 'RunPlugin(plugin://plugin.video.exodus/?action=authTrakt)'},
	'metalliq': {
		'name'     : 'MetalliQ',
		'plugin'   : 'plugin.video.metalliq',
		'saved'    : 'metalliq',
		'path'     : os.path.join(ADDONS, 'plugin.video.metalliq'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.metalliq', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.metalliq', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'metalliq_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.metalliq', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.metalliq/authenticate_trakt)'},
	'salts': {
		'name'     : 'Streaming All The Sources',
		'plugin'   : 'plugin.video.salts',
		'saved'    : 'salts',
		'path'     : os.path.join(ADDONS, 'plugin.video.salts'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.salts', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.salts', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'salts_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.salts', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_oauth_token', 'trakt_refresh_token', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.salts/?mode=auth_trakt)'},
	'saltshd': {
		'name'     : 'Salts HD',
		'plugin'   : 'plugin.video.saltshd.lite',
		'saved'    : 'saltshd',
		'path'     : os.path.join(ADDONS, 'plugin.video.saltshd.lite'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.saltshd.lite', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.saltshd.lite', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'saltshd_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.saltshd.lite', 'settings.xml'),
		'default'  : 'trakt_user',
		'data'     : ['trakt_oauth_token', 'trakt_refresh_token', 'trakt_user'],
		'activate' : 'RunPlugin(plugin://plugin.video.saltshd.lite/?mode=auth_trakt)'},
	'velocity': {
		'name'     : 'Velocity',
		'plugin'   : 'plugin.video.velocity',
		'saved'    : 'velocity',
		'path'     : os.path.join(ADDONS, 'plugin.video.velocity'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.velocity', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.velocity', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'velocity_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.velocity', 'settings.xml'),
		'default'  : 'trakt_username',
		'data'     : ['trakt_authorized', 'trakt_username', 'trakt_oauth_token', 'trakt_refresh_token'],
		'activate' : 'RunPlugin(plugin://plugin.video.velocity/?mode=get_pin)'},
	'velocitykids': {
		'name'     : 'Velocity Kids',
		'plugin'   : 'plugin.video.velocitykids',
		'saved'    : 'velocitykids',
		'path'     : os.path.join(ADDONS, 'plugin.video.velocitykids'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.velocitykids', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.velocitykids', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'velocitykids_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.velocitykids', 'settings.xml'),
		'default'  : 'trakt_username',
		'data'     : ['trakt_authorized', 'trakt_username', 'trakt_oauth_token', 'trakt_refresh_token'],
		'activate' : 'RunPlugin(plugin://plugin.video.velocitykids/?mode=get_pin)'},
	'meta': {
		'name'     : 'Meta',
		'plugin'   : 'plugin.video.meta',
		'saved'    : 'meta',
		'path'     : os.path.join(ADDONS, 'plugin.video.meta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.meta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.meta', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'meta_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.meta', 'settings.xml'),
		'default'  : 'trakt_access_token',
		'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at'],
		'activate' : 'RunPlugin(plugin://plugin.video.meta/authenticate_trakt)'},
	'royalwe': {
		'name'     : 'The Royal We',
		'plugin'   : 'plugin.video.theroyalwe',
		'saved'    : 'royalwe',
		'path'     : os.path.join(ADDONS, 'plugin.video.theroyalwe'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.theroyalwe', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.theroyalwe', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'royalwe_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.theroyalwe', 'settings.xml'),
		'default'  : 'trakt_account',
		'data'     : ['trakt_authorized', 'trakt_account', 'trakt_client_id', 'trakt_oauth_token', 'trakt_refresh_token', 'trakt_secret'],
		'activate' : 'RunScript(plugin.video.theroyalwe, ?mode=authorize_trakt)'},
	'specto': {
		'name'     : 'Specto',
		'plugin'   : 'plugin.video.specto',
		'saved'    : 'specto',
		'path'     : os.path.join(ADDONS, 'plugin.video.specto'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.specto', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.specto', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'specto_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.specto', 'settings.xml'),
		'default'  : 'trakt.user',
		'data'     : ['trakt.user', 'trakt.token', 'trakt.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.specto/?action=authTrakt)'},
	'trakt': {
		'name'     : 'Trakt',
		'plugin'   : 'script.trakt',
		'saved'    : 'trakt',
		'path'     : os.path.join(ADDONS, 'script.trakt'),
		'icon'     : os.path.join(ADDONS, 'script.trakt', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.trakt', 'fanart.jpg'),
		'file'     : os.path.join(TRAKTFOLD, 'trakt_trakt'),
		'settings' : os.path.join(ADDOND, 'script.trakt', 'settings.xml'),
		'default'  : 'user',
		'data'     : ['user', 'Auth_Info', 'authorization'],
		'activate' : 'RunScript(script.trakt, action=auth_info)'}
}

def traktUser(who):
	user=None
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			try:
				add = wiz.addonId(TRAKTID[who]['plugin'])
				user = add.getSetting(TRAKTID[who]['default'])
			except:
				return None
	return user


def traktIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(TRAKTFOLD):  os.makedirs(TRAKTFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(TRAKTID[log]['path']): updateTrakt(do, log)
			else: wiz.log('[Trakt Data] %s(%s) is not installed' % (TRAKTID[log]['name'],TRAKTID[log]['plugin']))
		wiz.setS('traktlastsave', str(THREEDAYS))
	else:
		if TRAKTID[who]:
			if os.path.exists(TRAKTID[who]['path']):
				updateTrakt(do, who)
		else: wiz.log('[Trakt Data] Invalid Entry: %s' % who)

def clearSaved(who):
	if who == 'all':
		for trakt in TRAKTID:
			file = TRAKTID[trakt]['file']
			if os.path.exists(file): os.remove(file)
			wiz.LogNotify(TRAKTID[trakt]['name'],'Trakt Data: [COLOR green]Removed![/COLOR]', 2000, TRAKTID[trakt]['icon'])
	elif TRAKTID[who]:
		file = TRAKTID[who]['file']
		if os.path.exists(file): os.remove(file)
		wiz.LogNotify(TRAKTID[who]['name'],'Trakt Data: [COLOR green]Removed![/COLOR]', 2000, TRAKTID[who]['icon'])
	xbmc.executebuiltin('Container.Refresh')
		
def updateTrakt(do, who):
	file      = TRAKTID[who]['file']
	settings  = TRAKTID[who]['settings']
	data      = TRAKTID[who]['data']
	addonid   = wiz.addonId(TRAKTID[who]['plugin'])
	saved     = TRAKTID[who]['saved']
	default   = TRAKTID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = TRAKTID[who]['name']
	icon      = TRAKTID[who]['icon']

	if do == 'update':
		if not user == '':
			with open(file, 'w') as f:
				for trakt in data: f.write('<trakt>\n\t<id>%s</id>\n\t<value>%s</value>\n</trakt>\n' % (trakt, addonid.getSetting(trakt)))
			f.close()
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'Trakt Data: [COLOR green]Saved![/COLOR]', 2000, icon)
		else: wiz.LogNotify(name,'Trakt Data: [COLOR red]Not Registered![/COLOR]', 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<trakt><id>(.+?)</id><value>(.+?)</value></trakt>').findall(g)
			if len(match) > 0:
				for trakt, value in match:
					addonid.setSetting(trakt, value)
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'Trakt: [COLOR green]Restored![/COLOR]', 2000, icon)
		#else: wiz.LogNotify(name,'Trakt Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings))
		if os.path.exists(settings):
			f = open(set,"r"); lines = f.readlines(); f.close()
			f = open(settings,"w")
			for line in lines:
				match = re.compile('<setting.+?id="(.+?)".+?/>').findall(line)
				if len(match) == 0: f.write(line)
				elif match[0] not in data: f.write(line)
				else: wiz.log('Removing Line: %s' % line)
			f.close()
			wiz.LogNotify(name,'Addon Data: [COLOR green]Cleared![/COLOR]', 2000, icon)
		else: wiz.LogNotify(name,'Addon Data: [COLOR red]Clear Failed![/COLOR]', 2000, icon)
	xbmc.executebuiltin('Container.Refresh')

def autoUpdate(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['path']):
				autoUpdate(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			u  = traktUser(who)
			su = wiz.getS(TRAKTID[who]['saved'])
			n = TRAKTID[who]['name']
			if u == None or u == '': return
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "Would you like to save the Trakt data for %s?" % n, "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
					traktIt('update', who)

def importlist(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['file']):
				importlist(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['file']):
			d  = TRAKTID[who]['default']
			sa = TRAKTID[who]['saved']
			su = wiz.getS(sa)
			n  = TRAKTID[who]['name']
			f  = open(TRAKTID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<trakt><id>%s</id><value>(.+?)</value></trakt>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "Would you like to import the Trakt data for %s?" % n, "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)))
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)))
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)))
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)))

def activateTrakt(who):
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']): 
			act     = TRAKTID[who]['activate']
			addonid = wiz.addonId(TRAKTID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(TRAKTID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % TRAKTID[who]['name'])
	else: 
		xbmc.executebuiltin('Container.Refresh')
		return
	check = 0
	while traktUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	xbmc.executebuiltin('Container.Refresh')