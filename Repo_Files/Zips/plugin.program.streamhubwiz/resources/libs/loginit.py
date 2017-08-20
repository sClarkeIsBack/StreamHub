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
LOGINFOLD      = os.path.join(ADDONDATA, 'login')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPLOGIN      = wiz.getS('keeplogin')
LOGINSAVE      = wiz.getS('loginlastsave')
ORDER          = ['sportsaccess', 'communityportal', 'tvportal', 'sportsmania', 'sportsnationhdtv', 'ultimatemania', 'dexter', 'reboot', 'ivue', 'ontapptv', 'vpnicity', 'overlordtv', 'xtreamcodes']

LOGINID = { 
	'sportsaccess': {
		'name'     : 'Sports Access',
		'plugin'   : 'plugin.video.sportsaccess',
		'saved'    : 'loginsportsaccess',
		'path'     : os.path.join(ADDONS, 'plugin.video.sportsaccess'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.sportsaccess', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.sportsaccess', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'sportsaccess_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.sportsaccess', 'settings.xml'),
		'default'  : 'skyusername',
		'data'     : ['skyusername', 'skypassword'],
		'activate' : 'RunPlugin(plugin://plugin.video.sportsaccess/?mode=259)'},
	'communityportal': {
		'name'     : 'Community Portal',
		'plugin'   : 'plugin.program.totalinstaller',
		'saved'    : 'logintotalinstaller',
		'path'     : os.path.join(ADDONS, 'plugin.program.totalinstaller'),
		'icon'     : os.path.join(ADDONS, 'plugin.program.totalinstaller', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.program.totalinstaller', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'totalinstaller_login'),
		'settings' : os.path.join(ADDONS, 'plugin.program.totalinstaller', 'settings.xml'),
		'default'  : 'username',
		'data'     : ['login', 'username', 'password'],
		'activate' : ''},
	'tvportal': {
		'name'     : 'TV Portal',
		'plugin'   : 'script.tvportal',
		'saved'    : 'logintvportal',
		'path'     : os.path.join(ADDONS, 'script.tvportal'),
		'icon'     : os.path.join(ADDONS, 'script.tvportal', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.tvportal', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'tvportal_login'),
		'settings' : os.path.join(ADDONS, 'script.tvportal', 'settings.xml'),
		'default'  : 'username',
		'data'     : ['login', 'username', 'password'],
		'activate' : ''},
	'sportsmania': {
		'name'     : 'Sports Mania',
		'plugin'   : 'plugin.video.sportsmania',
		'saved'    : 'loginsportsmania',
		'path'     : os.path.join(ADDONS, 'plugin.video.sportsmania'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.sportsmania', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.sportsmania', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'sportsmania_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.sportsmania', 'settings.xml'),
		'default'  : 'snusername',
		'data'     : ['snusername', 'snpassword'],
		'activate' : 'RunPlugin(plugin://plugin.video.sportsmania/?mode=202)'},
	'sportsnationhdtv': {
		'name'     : 'Sports NationHD',
		'plugin'   : 'plugin.video.sportsnationhdtv',
		'saved'    : 'loginsportsnationhd',
		'path'     : os.path.join(ADDONS, 'plugin.video.sportsnationhdtv'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.sportsnationhdtv', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.sportsnationhdtv', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'sportsnationhd_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.sportsnationhdtv', 'settings.xml'),
		'default'  : 'snusername',
		'data'     : ['snusername', 'snpassword'],
		'activate' : 'RunPlugin(plugin://plugin.video.sportsnationhdtv/?mode=202)'},
	'ultimatemania': {
		'name'     : 'Ultimate Mania',
		'plugin'   : 'plugin.video.ultimatemania',
		'saved'    : 'loginultimatemania',
		'path'     : os.path.join(ADDONS, 'plugin.video.ultimatemania'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.ultimatemania', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.ultimatemania', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'sportsmania_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.ultimatemania', 'settings.xml'),
		'default'  : 'snusername',
		'data'     : ['snusername', 'snpassword'],
		'activate' : 'RunPlugin(plugin://plugin.video.ultimatemania/?mode=202)'},
	'dexter': {
		'name'     : 'Dexter',
		'plugin'   : 'plugin.video.dex',
		'saved'    : 'logindexter',
		'path'     : os.path.join(ADDONS, 'plugin.video.dex'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.dex', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.dex', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'dexter_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.dex', 'settings.xml'),
		'default'  : 'kasutajanimi',
		'data'     : ['kasutajanimi', 'salasona', 'pordinumber'],
		'activate' : ''},
	'reboot': {
		'name'     : 'Reboot',
		'plugin'   : 'plugin.video.reboot',
		'saved'    : 'loginreboot',
		'path'     : os.path.join(ADDONS, 'plugin.video.reboot'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.reboot', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.reboot', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'reboot_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.reboot', 'settings.xml'),
		'default'  : 'USER',
		'data'     : ['username', 'password'],
		'activate' : ''},
	'ivue': {
		'name'     : 'Ivue TV Guide',
		'plugin'   : 'script.ivueguide',
		'saved'    : 'loginivue',
		'path'     : os.path.join(ADDONS, 'script.ivueguide'),
		'icon'     : os.path.join(ADDONS, 'script.ivueguide', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.ivueguide', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'ivue_login'),
		'settings' : os.path.join(ADDONS, 'script.ivueguide', 'settings.xml'),
		'default'  : 'username',
		'data'     : ['username', 'password'],
		'activate' : ''},
	'ontapptv': {
		'name'     : 'OnTapp.TV Guide',
		'plugin'   : 'script.tvguidedixie',
		'saved'    : 'loginontapptv',
		'path'     : os.path.join(ADDONS, 'script.tvguidedixie'),
		'icon'     : os.path.join(ADDONS, 'script.tvguidedixie', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.tvguidedixie', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'ontapptv_login'),
		'settings' : os.path.join(ADDONS, 'script.tvguidedixie', 'settings.xml'),
		'default'  : 'username',
		'data'     : ['username', 'password'],
		'activate' : ''},
	'vpnicity': {
		'name'     : 'VPNicity',
		'plugin'   : 'plugin.program.vpnicity',
		'saved'    : 'loginvpnicity',
		'path'     : os.path.join(ADDONS, 'plugin.program.vpnicity'),
		'icon'     : os.path.join(ADDONS, 'plugin.program.vpnicity', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.program.vpnicity', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'vpnicity_login'),
		'settings' : os.path.join(ADDONS, 'plugin.program.vpnicity', 'settings.xml'),
		'default'  : 'USER',
		'data'     : ['USER', 'PASS'],
		'activate' : ''},
	'overlordtv': {
		'name'     : 'Overlord TV',
		'plugin'   : 'plugin.video.overlordtv',
		'saved'    : 'loginoverlord',
		'path'     : os.path.join(ADDONS, 'plugin.video.overlordtv'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.overlordtv', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.overlordtv', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'overlordtv_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.overlordtv', 'settings.xml'),
		'default'  : 'Username',
		'data'     : ['Username', 'Password'],
		'activate' : ''},
	'xtreamcodes': {
		'name'     : 'Xtream Codes',
		'plugin'   : 'plugin.video.xtream-codes',
		'saved'    : 'loginxtreamcodes',
		'path'     : os.path.join(ADDONS, 'plugin.video.xtream-codes'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.xtream-codes', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.xtream-codes', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'xtreamcodes_login'),
		'settings' : os.path.join(ADDONS, 'plugin.video.xtream-codes', 'settings.xml'),
		'default'  : 'kasutajanimi',
		'data'     : ['kasutajanimi', 'salasona'],
		'activate' : ''}
}

def loginUser(who):
	user=None
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			try:
				add = wiz.addonId(LOGINID[who]['plugin'])
				user = add.getSetting(LOGINID[who]['default'])
			except:
				pass
	return user

def loginIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(LOGINFOLD):  os.makedirs(LOGINFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(LOGINID[log]['path']): updateLogin(do, log)
			else: wiz.log('[Login Data] %s(%s) is not installed' % (LOGINID[log]['name'],LOGINID[log]['plugin']))
		wiz.setS('loginlastsave', str(THREEDAYS))
	else:
		if LOGINID[who]:
			if os.path.exists(LOGINID[who]['path']):
				updateLogin(do, who)
		else: wiz.log('[Login Data] Invalid Entry: %s' % who)
		
def clearSaved(who):
	if who == 'all':
		for login in LOGINID:
			file = LOGINID[login]['file']
			if os.path.exists(file): os.remove(file)
			wiz.LogNotify(LOGINID[login]['name'],'Login Data: [COLOR green]Removed![/COLOR]', 2000, LOGINID[login]['icon'])
	elif LOGINID[who]:
		file = LOGINID[who]['file']
		if os.path.exists(file): os.remove(file)
		wiz.LogNotify(LOGINID[who]['name'],'Login Data: [COLOR green]Removed![/COLOR]', 2000, LOGINID[who]['icon'])
	xbmc.executebuiltin('Container.Refresh')
		
def updateLogin(do, who):
	file      = LOGINID[who]['file']
	settings  = LOGINID[who]['settings']
	data      = LOGINID[who]['data']
	addonid   = wiz.addonId(LOGINID[who]['plugin'])
	saved     = LOGINID[who]['saved']
	default   = LOGINID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = LOGINID[who]['name']
	icon      = LOGINID[who]['icon']

	if do == 'update':
		if not user == '':
			with open(file, 'w') as f:
				for login in data: f.write('<login>\n\t<id>%s</id>\n\t<value>%s</value>\n</login>\n' % (login, addonid.getSetting(login)))
			f.close()
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'Login Data: [COLOR green]Saved![/COLOR]', 2000, icon)
		else: wiz.LogNotify(name,'login Data: [COLOR red]Not Registered![/COLOR]', 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<login><id>(.+?)</id><value>(.+?)</value></login>').findall(g)
			if len(match) > 0:
				for login, value in match:
					addonid.setSetting(login, value)
			user = addonid.getSetting(default)
			wiz.setS(saved, user)
			wiz.LogNotify(name,'login: [COLOR green]Restored![/COLOR]', 2000, icon)
		#else: wiz.LogNotify(name,'login Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
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
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['path']):
				autoUpdate(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			u  = loginUser(who)
			su = wiz.getS(LOGINID[who]['saved'])
			n = LOGINID[who]['name']
			if u == None or u == '': return
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "Would you like to save the Login data for %s?" % n, "Addon: [COLOR green][B]%s[/B][/COLOR]" % u, "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
					loginIt('update', who)
					
def importlist(who):
	if who == 'all':
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['file']):
				importlist(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['file']):
			d  = LOGINID[who]['default']
			sa = LOGINID[who]['saved']
			su = wiz.getS(sa)
			n  = LOGINID[who]['name']
			f  = open(LOGINID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<login><id>%s</id><value>(.+?)</value></login>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "Would you like to import the Login data for %s?" % n, "File: [COLOR green][B]%s[/B][/COLOR]" % m[0], "Saved: [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved: [COLOR red][B]None[/B][/COLOR]', yeslabel="Yes Save", nolabel="No Cancel"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)))
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)))
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)))
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)))

def activateLogin(who):
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']): 
			act     = LOGINID[who]['activate']
			addonid = wiz.addonId(LOGINID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(LOGINID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % LOGINID[who]['name'])
	else: 
		xbmc.executebuiltin('Container.Refresh')
		return
	check = 0
	while loginUser(who) == None or loginUser(who) == "":
		if check == 30: break
		check += 1
		time.sleep(10)
	xbmc.executebuiltin('Container.Refresh')