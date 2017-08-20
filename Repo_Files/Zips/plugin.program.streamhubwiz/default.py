import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import fnmatch
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import extract, downloader, notify, debridit, traktit, loginit, skinSwitch, uploadLog, wizard as wiz

ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(PLUGIN,    'fanart.jpg')
ICON             = os.path.join(PLUGIN,    'icon.png')
ART              = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPLOGIN        = wiz.getS('keeplogin')
LOGINSAVE        = wiz.getS('loginlastsave')
DEVELOPER        = wiz.getS('developer')
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)
KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
MCNAME           = "Kodi"
EXCLUDES         = uservar.EXCLUDES
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
WORKINGURL       = wiz.workingURL(BUILDFILE)
APKWORKINGURL    = wiz.workingURL(APKFILE)
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID
LOGINID          = loginit.LOGINID

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

def index():
	if AUTOUPDATE == 'Yes':
		if wiz.workingURL(WIZARDFILE) == True:
			ver = wiz.checkWizard('version')
			if ver > VERSION: addFile('%s [v%s] [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (ADDONTITLE, VERSION, ver), 'wizardupdate', themeit=THEME2)
			else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
		else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	if len(BUILDNAME) > 0:
		version = wiz.checkBuild(BUILDNAME, 'version')
		build = '%s (v%s)' % (BUILDNAME, BUILDVERSION)
		if version > BUILDVERSION: build = '%s [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (build, version)
		addDir(build,'viewbuild',BUILDNAME, themeit=THEME4)
		themefile = wiz.checkBuild(BUILDNAME, 'theme')
		if not themefile == 'http://' and wiz.workingURL(themefile) == True:
			addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME5)
	else: addDir('None', 'builds', themeit=THEME4)
	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	addDir ('Builds'        ,'builds',   icon=ICONBUILDS,   themeit=THEME1)
	addDir ('Maintenance'   ,'maint',    icon=ICONMAINT,    themeit=THEME1)
	if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Apk Installer' ,'apk', icon=ICONAPK, themeit=THEME1)
	addDir ('Save Data'     ,'savedata', icon=ICONSAVE,     themeit=THEME1)
	if HIDECONTACT == 'No': addFile('Contact' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	addFile('Settings'      ,'settings', icon=ICONSETTINGS, themeit=THEME1)
	if DEVELOPER == 'true': addDir('Developer Menu','developer', icon=ICONSETTINGS, themeit=THEME1)
	setView('files', 'MAIN')

def buildMenu():
	if not WORKINGURL == True:
		addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
		addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:	
		link  = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?odi="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
		if len(match) == 1:
			viewBuild(match[0][0])
		elif len(match) > 1:
			addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
			addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
			if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
			if SEPERATE == 'true':
				for name, version, url, kodi, icon, fanart in match:
					menu = createMenu('install', '', name)
					addDir('[%s] %s (v%s)' % (float(kodi), name, version),'viewbuild',name,fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			else:
				count15 = wiz.buildCount('15'); count16 = wiz.buildCount('16')
				if count16 > 0:
					if count15 > 0: 
						state = '+' if SHOW16 == 'false' else '-'
						addFile('[%s] Jarvis and Above(%s)' % (state, count16), 'showupdate',  '16', themeit=THEME3)
					if SHOW16 == 'true':
						for name, version, url, kodi, icon, fanart in match:
							kodiv = int(float(kodi))
							if kodiv >= 16:
								menu = createMenu('install', '', name)
								addDir('[%s] %s (v%s)' % (float(kodi), name, version),'viewbuild',name,fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
				if count15 > 0:
					if count16 > 0:
						state = '+' if SHOW15 == 'false' else '-'
						addFile('[%s] Isengard and Below(%s)' % (state, count15), 'showupdate',  '15', themeit=THEME3)
					if SHOW15 == 'true':
						for name, version, url, kodi, icon, fanart in match:
							kodiv = int(float(kodi))
							if kodiv <= 15:
								menu = createMenu('install', '', name)
								addDir('[%s] %s (v%s)' % (float(kodi), name, version),'viewbuild',name,fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
		else: addFile('Text file for builds not formated correctly.', '', icon=ICONBUILDS, themeit=THEME3)
	setView('files', 'MAIN')

def viewBuild(name):
	if not WORKINGURL == True:
		addFile('Url for txt file not valid', '', themeit=THEME3)
		addFile('%s' % WORKINGURL, '', themeit=THEME3)
		return 
	if wiz.checkBuild(name, 'version') == False: 
		addFile('Error reading the txt file.', '', themeit=THEME3)
		addFile('%s was not found in the builds list.' % name, '', themeit=THEME3)
		return
	link = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % name).findall(link)
	for version, url, gui, kodi, themefile, icon, fanart in match:
		icon        = icon   if wiz.workingURL(icon)   else ICON
		fanart      = fanart if wiz.workingURL(fanart) else FANART
		build       = '%s (v%s)' % (name, version)
		if BUILDNAME == name and version > BUILDVERSION:
			build = '%s [COLOR red][B][CURRENT v%s][/B][/COLOR]' % (build, BUILDVERSION)
		addFile(build, '', fanart=fanart, icon=icon, themeit=THEME2)
		addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
		if KODIV < 16 and float(kodi) >= 16:
			addFile('[I]Build designed for kodi version %s(installed: %s)[/I]' % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile('===============[ Install ]===================', '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile('Fresh Install'   , 'install', name, 'fresh'   , fanart=fanart, icon=icon, themeit=THEME1)
		addFile('Standard Install', 'install', name, 'normal'  , fanart=fanart, icon=icon, themeit=THEME1)
		if not gui == 'http://': addFile('Apply guiFix'    , 'install', name, 'gui'     , fanart=fanart, icon=icon, themeit=THEME1)
		if not themefile == 'http://':
			if wiz.workingURL(themefile) == True:
				addFile('===============[ Themes ]==================', '', fanart=fanart, icon=icon, themeit=THEME3)
				link  = wiz.openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
				for themename, themeurl, themeicon, themefanart in match:
					themeicon   = themeicon   if themeicon   == 'http://' else icon
					themefanart = themefanart if themefanart == 'http://' else fanart
					addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, fanart=themefanart, icon=themeicon, themeit=THEME3)
	setView('files', 'MAIN')

def apkMenu():
	kver, kurl = wiz.latestApk('kodi').split('|||')
	sver, surl = wiz.latestApk('spmc').split('|||')
	addFile('Kodi (v%s)' % kver     ,'apkinstall',  'kodi', kurl, icon=ICONAPK, themeit=THEME1)
	addFile('SPMC (v%s)' % sver     ,'apkinstall',  'spmc', surl, icon=ICONAPK, themeit=THEME1)
	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	if not APKFILE == 'http://':
		if APKWORKINGURL == True:
			link = wiz.openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
			if len(match) > 0:
				for name, url, icon, fanart in match:
					addFile(name, 'apkinstall', name, url, icon=icon, fanart=fanart, themeit=THEME1)
			else: wiz.log("[APK Menu] ERROR: Invalid Format.")
		else: wiz.log("[APK Menu] ERROR: URL for apk list not working.")
	else: wiz.log("[APK Menu] No APK list added.")
	setView('files', 'MAIN')
	
def maintMenu():
	on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
	autoclean  = 'true' if AUTOCLEANUP   == 'true' else 'false'
	cache      = 'true' if AUTOCACHE     == 'true' else 'false'
	packages   = 'true' if AUTOPACKAGES  == 'true' else 'false'
	addFile('Fresh Start'          ,'freshstart',      icon=ICONMAINT, themeit=THEME1)
	addFile('Clear Cache'          ,'clearcache',      icon=ICONMAINT, themeit=THEME1)
	addFile('Clear Packages'       ,'clearpackages',   icon=ICONMAINT, themeit=THEME1)
	addFile('Clear Thumbnails'     ,'clearthumb',      icon=ICONMAINT, themeit=THEME1)
	addFile('Clear Crash Logs'     ,'clearcrash',      icon=ICONMAINT, themeit=THEME1)
	addFile('Purge Databases'      ,'purgedb',         icon=ICONMAINT, themeit=THEME1)
	addDir ('Remove Addons'        ,'removeaddons',    icon=ICONMAINT, themeit=THEME1)
	addDir ('Remove Addon Data'    ,'removeaddondata', icon=ICONMAINT, themeit=THEME1)
	addFile('Force Update Addons'  ,'forceupdate',     icon=ICONMAINT, themeit=THEME1)
	addFile('Force Close Kodi'     ,'forceclose',      icon=ICONMAINT, themeit=THEME1)
	addFile('Hide Passwords On Keyboard Entry'   ,'hidepassword',   icon=ICONMAINT, themeit=THEME1)
	addFile('Unhide Passwords On Keyboard Entry' ,'unhidepassword', icon=ICONMAINT, themeit=THEME1)
	addFile('Upload Kodi.log'      ,'uploadlog',       icon=ICONMAINT, themeit=THEME1)
	addFile('View Log File'        ,'viewlog',         icon=ICONMAINT, themeit=THEME1)
	addFile('View Wizard Log File' ,'viewwizlog',      icon=ICONMAINT, themeit=THEME1)
	addFile('Clear Wizard Log File','clearwizlog',     icon=ICONMAINT, themeit=THEME1)
	addFile('==============[ Auto Clean ]==============', '', fanart=FANART, icon=ICONMAINT, themeit=THEME3)
	addFile('Auto Clean Up On Startup: %s' % autoclean.replace('true',on).replace('false',off) ,'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME1)
	if autoclean == 'true':
		addFile('--- Clear Cache on Startup: %s' % cache.replace('true',on).replace('false',off) ,'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME1)
		addFile('--- Clear Packages on Startup: %s' % packages.replace('true',on).replace('false',off) ,'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME1)
	setView('files', 'MAIN')

def saveMenu():
	on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
	trakt      = 'true' if KEEPTRAKT     == 'true' else 'false'
	real       = 'true' if KEEPREAL      == 'true' else 'false'
	login      = 'true' if KEEPLOGIN     == 'true' else 'false'
	sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
	advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
	profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
	favourites = 'true' if KEEPFAVS      == 'true' else 'false'

	addDir ('Keep Trakt Data'               ,'trakt',         icon=ICONTRAKT, themeit=THEME1)
	addDir ('Keep Real Debrid'              ,'realdebrid',    icon=ICONREAL, themeit=THEME1)
	addDir ('Keep Login Info'               ,'login',         icon=ICONLOGIN, themeit=THEME1)
	addFile('- Click to toggle settings -', '', themeit=THEME3)
	addFile('Save Trakt: %s' % trakt.replace('true',on).replace('false',off)                       ,'togglesetting', 'keeptrakt',      icon=ICONTRAKT, themeit=THEME1)
	addFile('Save Real Debrid: %s' % real.replace('true',on).replace('false',off)                  ,'togglesetting', 'keepdebrid',     icon=ICONREAL,  themeit=THEME1)
	addFile('Save Login Info: %s' % login.replace('true',on).replace('false',off)                  ,'togglesetting', 'keeplogin',      icon=ICONLOGIN, themeit=THEME1)
	addFile('Keep \'Sources.xml\': %s' % sources.replace('true',on).replace('false',off)           ,'togglesetting', 'keepsources',    icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep \'Profiles.xml\': %s' % profiles.replace('true',on).replace('false',off)         ,'togglesetting', 'keepprofiles',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep \'Advancedsettings.xml\': %s' % advanced.replace('true',on).replace('false',off) ,'togglesetting', 'keepadvanced',   icon=ICONSAVE,  themeit=THEME1)
	addFile('Keep \'Favourites.xml\': %s' % favourites.replace('true',on).replace('false',off)     ,'togglesetting', 'keepfavourites', icon=ICONSAVE,  themeit=THEME1)
	setView('files', 'MAIN')

def traktMenu():
	trakt = '[COLOR green]ON[/COLOR]' if KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(TRAKTSAVE) if not TRAKTSAVE == '' else 'Trakt hasnt been saved yet.'
	addFile('[I]Register FREE Account at http://trakt.tv[/I]', '', icon=ICONTRAKT, themeit=THEME3)
	addFile('Save Trakt Data: %s' % trakt, 'togglesetting', 'keeptrakt', icon=ICONTRAKT, themeit=THEME3)
	if KEEPTRAKT == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONTRAKT, themeit=THEME3)
	if HIDESPACERS == 'No': addFile('============================================', '', icon=ICONTRAKT, themeit=THEME3)
	
	for trakt in traktit.ORDER:
		name   = TRAKTID[trakt]['name']
		path   = TRAKTID[trakt]['path']
		saved  = TRAKTID[trakt]['saved']
		file   = TRAKTID[trakt]['file']
		user   = wiz.getS(saved)
		auser  = traktit.traktUser(trakt)
		icon   = TRAKTID[trakt]['icon']   if os.path.exists(path) else ICONTRAKT
		fanart = TRAKTID[trakt]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Trakt', trakt)
		menu2 = createMenu('save', 'Trakt', trakt)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=trakt)' %   (ADDON_ID, trakt)))
		
		addFile('[+]-- %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	addFile('Save All Trakt Data',          'savetrakt',    'all', icon=ICONTRAKT,  themeit=THEME3)
	addFile('Recover All Saved Trakt Data', 'restoretrakt', 'all', icon=ICONTRAKT,  themeit=THEME3)
	addFile('Import Trakt Data',            'importtrakt',  'all', icon=ICONTRAKT,  themeit=THEME3)
	addFile('Clear All Saved Trakt Data',   'cleartrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
	addFile('Clear All Addon Data',         'addontrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
	setView('files', 'MAIN')
	
def realMenu():
	real = '[COLOR green]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(REALSAVE) if not REALSAVE == '' else 'Real Debrid hasnt been saved yet.'
	addFile('[I]http://real-debrid.com is a PAID service.[/I]', '', icon=ICONREAL, themeit=THEME3)
	addFile('Save Real Debrid Data: %s' % real, 'togglesetting', 'keepdebrid', icon=ICONREAL, themeit=THEME3)
	if KEEPREAL == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONREAL, themeit=THEME3)
	if HIDESPACERS == 'No': addFile('============================================', '', icon=ICONREAL, themeit=THEME3)
	
	for debrid in debridit.ORDER:
		name   = DEBRIDID[debrid]['name']
		path   = DEBRIDID[debrid]['path']
		saved  = DEBRIDID[debrid]['saved']
		file   = DEBRIDID[debrid]['file']
		user   = wiz.getS(saved)
		auser  = debridit.debridUser(debrid)
		icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else ICONTRAKT
		fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Debrid', debrid)
		menu2 = createMenu('save', 'Debrid', debrid)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))
		
		addFile('[+]-- %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	addFile('Save All Real Debrid Data',          'savedebrid',    'all', icon=ICONREAL,  themeit=THEME3)
	addFile('Recover All Saved Real Debrid Data', 'restoredebrid', 'all', icon=ICONREAL,  themeit=THEME3)
	addFile('Import Real Debrid Data',            'importdebrid',  'all', icon=ICONREAL,  themeit=THEME3)
	addFile('Clear All Saved Real Debrid Data',   'cleardebrid',   'all', icon=ICONREAL,  themeit=THEME3)
	addFile('Clear All Addon Data',               'addondebrid',   'all', icon=ICONREAL,  themeit=THEME3)
	setView('files', 'MAIN')

def loginMenu():
	login = '[COLOR green]ON[/COLOR]' if KEEPLOGIN == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(LOGINSAVE) if not LOGINSAVE == '' else 'Login data hasnt been saved yet.'
	addFile('[I]Several of these addons are PAID services.[/I]', '', icon=ICONLOGIN, themeit=THEME3)
	addFile('Save Login Data: %s' % login, 'togglesetting', 'keeplogin', icon=ICONLOGIN, themeit=THEME3)
	if KEEPLOGIN == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONLOGIN, themeit=THEME3)
	if HIDESPACERS == 'No': addFile('============================================', '', icon=ICONLOGIN, themeit=THEME3)

	for login in loginit.ORDER:
		name   = LOGINID[login]['name']
		path   = LOGINID[login]['path']
		saved  = LOGINID[login]['saved']
		file   = LOGINID[login]['file']
		user   = wiz.getS(saved)
		auser  = loginit.loginUser(login)
		icon   = LOGINID[login]['icon']   if os.path.exists(path) else ICONTRAKT
		fanart = LOGINID[login]['fanart'] if os.path.exists(path) else FANART
		menu = createMenu('saveaddon', 'Login', login)
		menu2 = createMenu('save', 'Login', login)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=login)' %   (ADDON_ID, login)))
		
		addFile('[+]-- %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
		if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authlogin', login, icon=icon, fanart=fanart, menu=menu)
		else:                        addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authlogin', login, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importlogin', login, icon=icon, fanart=fanart, menu=menu2)
			else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savelogin', login, icon=icon, fanart=fanart, menu=menu2)
		else:                        addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

	if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
	addFile('Save All Login Data',          'savelogin',    'all', icon=ICONLOGIN,  themeit=THEME3)
	addFile('Recover All Saved Login Data', 'restorelogin', 'all', icon=ICONLOGIN,  themeit=THEME3)
	addFile('Import Login Data',            'importlogin',  'all', icon=ICONLOGIN,  themeit=THEME3)
	addFile('Clear All Saved Login Data',   'clearlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
	addFile('Clear All Addon Data',         'addonlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
	setView('files', 'MAIN')

def removeAddonMenu():
	for folder in glob.glob(os.path.join(ADDONS, '*/')):
		foldername = folder.replace(ADDONS, '').replace('\\', '').replace('/', '')
		icon = os.path.join(folder, 'icon.png')
		fanart = os.path.join(folder, 'fanart.png')
		if foldername in EXCLUDES: pass
		elif foldername == 'packages': pass
		else:
			folderdisplay = foldername
			replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR green][SCRIPT] [/COLOR]', 'service.':'[COLOR green][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
			for rep in replace:
				folderdisplay = folderdisplay.replace(rep, replace[rep])
			addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay, 'removeaddon', foldername, icon=icon, fanart=fanart, themeit=THEME2)
	setView('files', 'MAIN')

def removeAddonDataMenu():
	if os.path.exists(ADDOND):
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
		addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
		if HIDESPACERS == 'No': addFile('============================================', '', themeit=THEME3)
		for folder in glob.glob(os.path.join(ADDOND, '*')):
			foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
			icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
			fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
			folderdisplay = foldername
			replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR green][SCRIPT] [/COLOR]', 'service.':'[COLOR green][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
			for rep in replace:
				folderdisplay = folderdisplay.replace(rep, replace[rep])
			if foldername in EXCLUDES: folderdisplay = '[COLOR green][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
			else: folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
			addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
	else:
		addFile('No Addon data folder found.', '', themeit=THEME3)
	setView('files', 'MAIN')

def developer():
	addFile('===============[ Back Up ]===================', '',    themeit=THEME3)
	addFile('Back Up: Build'                     , 'backupbuild',   themeit=THEME1)
	addFile('Back Up: GuiFix'                    , 'backupgui',     themeit=THEME1)
	addFile('Back Up: Theme'                     , 'backuptheme',   themeit=THEME1)
	addFile('Clean Up Back Up Folder'            , 'clearbackup',   themeit=THEME1)
	addFile('===============[ Restore ]===================', '',    themeit=THEME3)
	addFile('Restore: Local Build'               , 'restorezip',    themeit=THEME1)
	addFile('Restore: Local GuiFix'              , 'restoregui',    themeit=THEME1)
	addFile('Restore: External Build'            , 'restoreextzip', themeit=THEME1)
	addFile('Restore: External GuiFix'           , 'restoreextgui', themeit=THEME1)
	addFile('===============[ Fixes ]====================', '',     themeit=THEME3)
	addFile('Remove special character filenames' , 'asciicheck',    themeit=THEME1)
	addFile('Convert Paths to special'           , 'convertpath',   themeit=THEME1)
	addFile('===============[ Testing ]===================', '',    themeit=THEME3)
	addFile('Test Notifications'                 , 'testnotify',    themeit=THEME1)
	addFile('Test Update'                        , 'testupdate',    themeit=THEME1)
	addFile('Test First Run'                     , 'testfirst',     themeit=THEME1)
	setView('files', 'MAIN')

###########################
###### Build Install ######
###########################

def buildWizard(name, type, theme=None):
	testbuild = wiz.checkBuild(name, 'url')
	if testbuild == False:
		wiz.LogNotify(ADDONTITLE, "Unabled to find build")
		return
	if type == 'gui':
		if name == BUILDNAME:
			yes_pressed=DIALOG.yesno(ADDONTITLE, 'Would you like to apply the guifix for:', '%s?' % name, nolabel='No, Cancel',yeslabel='Yes, Apply Fix')
		else: 
			yes_pressed=DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "%s community build is not currently installed." % name, "Would you like to apply the guiFix anyways?.", yeslabel="Yes, Apply", nolabel="No, Cancel")
		if yes_pressed:
			buildzip = wiz.checkBuild(name,'gui')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify(ADDONTITLE, 'guiFix: [COLOR red]Invalid Zip Url![/COLOR]'); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'Downloading %s GuiFix' % name,'', 'Please Wait')
			lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			DP.update(0,"", "Installing %s GuiFix" % name)
			extract.all(lib,USERDATA,DP)
			DP.close()
			wiz.defaultSkin()
			wiz.killxbmc()
		else:
			wiz.LogNotify(ADDONTITLE, 'guiFix: [COLOR red]Cancelled![/COLOR]')
	elif type == 'fresh':
		freshStart(name)
	elif type == 'normal':
		if url == 'normal':
			if KEEPTRAKT == 'true':
				traktit.autoUpdate('all')
				wiz.setS('traktlastsave', str(THREEDAYS))
			if KEEPREAL == 'true':
				debridit.autoUpdate('all')
				wiz.setS('debridlastsave', str(THREEDAYS))
			if KEEPLOGIN == 'true':
				loginit.autoUpdate('all')
				wiz.setS('loginlastsave', str(THREEDAYS))
		if KODIV < 16.0 and float(wiz.checkBuild(name, 'kodi')) >= 16.0:
			yes_pressed = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, 'There is a chance that the skin will not appear correctly', 'When installing a %s build on a Kodi %s install' % (wiz.checkBuild(name, 'kodi'), KODIV), 'Would you still like to install: %s v%s?' % (name, wiz.checkBuild(name,'version')), nolabel='No, Cancel',yeslabel='Yes, Install')
		else:
			yes_pressed = DIALOG.yesno(ADDONTITLE, 'Would you like to install:', '%s v%s?' % (name, wiz.checkBuild(name,'version')), nolabel='No, Cancel',yeslabel='Yes, Install')
		if yes_pressed:
			wiz.clearS('build')
			buildzip = wiz.checkBuild(name, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(buildzip) == True: wiz.LogNotify(ADDONTITLE, 'Build Install: [COLOR red]Invalid Zip Url![/COLOR]'); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'Downloading %s ' % name,'', 'Please Wait')
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(buildzip, lib, DP)
			xbmc.sleep(500)
			DP.update(0,"", "Installing %s " % name)
			ext = extract.all(lib,HOME,DP)
			percent, errors, error = ext.split('/', 3)
			if percent > 0:
				wiz.defaultSkin()
				wiz.setS('buildname', name)
				wiz.setS('buildversion', wiz.checkBuild( name,'version'))
				wiz.setS('buildtheme', '')
				wiz.setS('latestversion', wiz.checkBuild( name,'version'))
				wiz.setS('lastbuildcheck', str(NEXTCHECK))
				wiz.setS('installed', 'true')
				wiz.setS('extract', str(percent))
				wiz.setS('errors', str(errors))
				wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
				if int(errors) >= 1:
					yes=DIALOG.yesno(ADDONTITLE, 'INSTALLED %s: [ERRORS:%s]' % (percent, errors), 'Would you like to view the errors?', nolabel='No, Cancel',yeslabel='Yes, View')
					if yes:
						wiz.TextBoxes(ADDONTITLE, error.replace('\t','')); xbmc.sleep(3000)
				DP.close()
				themefile = wiz.checkBuild(name, 'theme')
				if not themefile == 'http://' and wiz.workingURL(themefile) == True: buildWizard(name, 'theme')
				DIALOG.ok(ADDONTITLE, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
				wiz.killxbmc()
			else:
				DIALOG.ok(ADDONTITLE, "There was an error installing the build.", errors)
		else:
			wiz.LogNotify(ADDONTITLE, 'Build Install: [COLOR red]Cancelled![/COLOR]')
	elif type == 'theme':
		if theme == None:
			themefile = wiz.checkBuild(name, 'theme')
			themelist = []
			if not themefile == 'http://' and wiz.workingURL(themefile) == True:
				link  = wiz.openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
				match = re.compile('name="(.+?)"').findall(link)
				if len(match) > 0:
					if DIALOG.yesno(ADDONTITLE, "The Build [%s] comes with %s different themes" % (name, len(match)), "Would you like to install one now?", yeslabel="Yes, Install", nolabel="No Thanks"):
						for themename in match:
							themelist.append(themename)
						wiz.log("Theme List: %s " % str(themelist))
						ret = DIALOG.select(ADDONTITLE, themelist)
						wiz.log("Theme install selected: %s" % ret)
						if not ret == -1: theme = themelist[ret]; installtheme = True
						else: wiz.LogNotify(ADDONTITLE,'Theme Install: [COLOR red]Cancelled![/COLOR]'); return
					else: wiz.LogNotify(ADDONTITLE,'Theme Install: [COLOR red]Cancelled![/COLOR]'); return
			else: wiz.LogNotify(ADDONTITLE,'Theme Install: [COLOR red]None Found![/COLOR]')
		else: installtheme = DIALOG.yesno(ADDONTITLE, 'Would you like to install the theme:', theme, 'for %s v%s?' % (name, wiz.checkBuild(name,'version')), nolabel='No, Cancel',yeslabel='Yes, Install')
		if installtheme:
			themezip = wiz.checkTheme(name, theme, 'url')
			zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			if not wiz.workingURL(themezip) == True: wiz.LogNotify(ADDONTITLE, 'Theme Install: [COLOR red]Invalid Zip Url![/COLOR]'); return
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			DP.create(ADDONTITLE,'Downloading %s ' % name,'', 'Please Wait')
			lib=os.path.join(PACKAGES, '%s.zip' % zipname)
			try: os.remove(lib)
			except: pass
			downloader.download(themezip, lib, DP)
			xbmc.sleep(500)
			DP.update(0,"", "Installing %s " % name)
			ext = extract.all(lib,HOME,DP)
			percent, errors, error = ext.split('/', 3)
			wiz.setS('buildtheme', theme)
			wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
			DP.close()
			if url not in ["fresh", "normal"]: xbmc.executebuiltin("ReloadSkin()"); xbmc.sleep(1000); xbmc.executebuiltin("Container.Refresh") 
		else:
			wiz.LogNotify(ADDONTITLE, 'Theme Install: [COLOR red]Cancelled![/COLOR]')

def apkInstaller(apk, url):
	if wiz.platform() == 'android':
		if apk in ['kodi', 'spmc']: 
			yes=DIALOG.yesno(ADDONTITLE, "Would you like to download and install:", "%s (v%s)" % (apk.upper(),wiz.latestApk(apk,'version')))
			if not yes: wiz.LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] Install Cancelled'); return
			display = "%s v%s" % (apk.upper(), wiz.latestApk(apk, 'version'))
		else: 
			yes=DIALOG.yesno(ADDONTITLE, "Would you like to download and install:", "%s" % apk)
			if not yes: wiz.LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] Install Cancelled'); return
			display = apk
		if yes:
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			if not wiz.workingURL(url) == True: wiz.LogNotify(ADDONTITLE, 'APK Installer: [COLOR red]Invalid Apk Url![/COLOR]'); return
			DP.create(ADDONTITLE,'Downloading %s' % display,'', 'Please Wait')
			lib=os.path.join(PACKAGES, "%s.apk" % apk)
			try: os.remove(lib)
			except: pass
			downloader.download(url, lib, DP)
			xbmc.sleep(500)
			DP.close()
			DIALOG.ok(ADDONTITLE, "Launching the APK to be installed", "Follow the install process to complete.")
			xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
		else: wiz.LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] Install Cancelled')
	else: wiz.LogNotify(ADDONTITLE, '[COLOR red]ERROR:[/COLOR] None Android Device')

###########################
###### Misc Functions######
###########################

def showHide(ver):
	if ver == '15': wiz.setS('show15', 'true' if SHOW15 == 'false' else 'false')
	elif ver == '16': wiz.setS('show16', 'true' if SHOW16 == 'false' else 'false')
	xbmc.executebuiltin('Container.Refresh')

def percentage(part, whole):
	return 100 * float(part)/float(whole)

def createMenu(type, add, name):
	if   type == 'saveaddon':
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'save'    :
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Register %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Import %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'install'  :
		menu_items=[]
		name2 = urllib.quote_plus(name)
		menu_items.append((THEME2 % name,             ' '))
		menu_items.append((THEME3 % 'Fresh Install',          'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Normal Install',         'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Apply guiFix',           'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
	menu_items.append((THEME2 % '%s Settings' % ADDONTITLE, 'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
	return menu_items

def viewLogFile():
	log     = wiz.log_check()
	logtype = log.replace(LOG,"")
	if os.path.exists(log) or not log == False:
		f = open(log,mode='r'); msg = f.read(); f.close()
		wiz.TextBoxes("%s - %s" % (ADDONTITLE, logtype), msg)
	else: 
		wiz.LogNotify('View Log', 'No Log File Found!')

def viewWizLogFile():
	if os.path.exists(WIZLOG):
		f = open(WIZLOG,mode='r'); msg = f.read(); f.close()
		wiz.TextBoxes("%s - Wizard.log" % ADDONTITLE, msg)
	else:
		wiz.LogNotify('View Log', 'Wizard.log not found!')

def removeAddon(addon):
	if DIALOG.yesno(ADDONTITLE, 'Are you sure you want to delete the addon:', '[COLOR yellow]%s[/COLOR]' % addon, yeslabel='Yes, Remove', nolabel='No, Cancel'):
		wiz.cleanHouse(os.path.join(ADDONS, addon))
		removeAddonData(addon)
		wiz.LogNotify('Remove Addon', 'Complete!')
		DIALOG.ok(ADDONTITLE, 'The addon has been removed but will remain in the addons list until the next time you reload Kodi.')
	else: wiz.LogNotify('Remove Addon', 'Cancelled!')
	xbmc.executebuiltin('Container.Refresh')

def removeAddonData(addon):
	if addon == 'all':
		if DIALOG.yesno(ADDONTITLE, 'Would you like to remove ALL addon data stored in you Userdata folder?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			wiz.cleanHouse(ADDOND)
		else: wiz.LogNotify('Remove Addon Data', 'Cancelled!')
	elif addon == 'uninstalled':
		if DIALOG.yesno(ADDONTITLE, 'Would you like to remove ALL addon data stored in you Userdata folder for uninstalled addons?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			total = 0
			for folder in glob.glob(os.path.join(ADDOND, '*')):
				foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify('Clean up Uninstalled', '[COLOR yellow]%s[/COLOR] Folders(s) Removed' % total)
		else: wiz.LogNotify('Remove Addon Data', 'Cancelled!')
	elif addon == 'empty':
		if DIALOG.yesno(ADDONTITLE, 'Would you like to remove ALL empty addon data folders in you Userdata folder?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			total = wiz.emptyfolder(ADDOND)
			wiz.LogNotify('Remove Empty Folders', '[COLOR yellow]%s[/COLOR] Folders(s) Removed' % total)
		else: wiz.LogNotify('Remove Empty Folders', 'Cancelled!')
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("Protected Plugin", "Not allowed to remove Addon_Data")
		elif os.path.exists(addon_data):  
			if DIALOG.yesno(ADDONTITLE, 'Would you also like to remove the addon data for:', '[COLOR yellow]%s[/COLOR]' % addon, yeslabel='Yes, Remove', nolabel='No, Cancel'):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error deleting: %s" % addon_data)
			else: 
				wiz.log('Addon data for %s was not removed' % addon)
	xbmc.executebuiltin('Container.Refresh')

def restoreit(type):
	if type == 'build':
		freshStart('restore')
	wiz.restoreLocal(type)

def restoreextit(type):
	if type == 'build':
		freshStart('restore')
	wiz.restoreExternal(type)

###########################
###### Fresh Install ######
###########################

def freshStart(install=None):
	if KEEPTRAKT == 'true':
		traktit.autoUpdate('all')
		wiz.setS('traktlastsave', str(THREEDAYS))
	if KEEPREAL == 'true':
		debridit.autoUpdate('all')
		wiz.setS('debridlastsave', str(THREEDAYS))
	if KEEPLOGIN == 'true':
		loginit.autoUpdate('all')
		wiz.setS('loginlastsave', str(THREEDAYS))

	if install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE,"Do you wish to restore your","Kodi configuration to default settings", "Before installing the local backup?", nolabel='No, Cancel', yeslabel='Yes, Continue')
	elif install: yes_pressed=DIALOG.yesno(ADDONTITLE,"Do you wish to restore your","Kodi configuration to default settings", "Before installing %s?" % install, nolabel='No, Cancel', yeslabel='Yes, Continue')
	else: yes_pressed=DIALOG.yesno(ADDONTITLE,"Do you wish to restore your","Kodi configuration to default settings?", nolabel='No, Cancel', yeslabel='Yes, Continue')
	if yes_pressed:
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
			yes=DIALOG.yesno(ADDONTITLE, "The skin needs to be set back to [COLOR yellow]%s[/COLOR]" % skin[5:], "Before doing a fresh install to clear all Texture files!", "Would you like us to do that for you?", nolabel="No, Thanks", yeslabel="Yes, Swap Skin");
			if yes:
				skinSwitch.swapSkins(skin)
				x = 0
				xbmc.sleep(1000)
				while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
					if x == 150:
						break
					x += 1
					xbmc.sleep(200)
					
				if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
					xbmc.executebuiltin('SetFocus(11)')
					xbmc.executebuiltin('Action(Select)')
				else: wiz.LogNotify(ADDONTITLE,'Fresh Install: [COLOR red]Skin Swap Timed Out![/COLOR]'); return
				xbmc.sleep(500)
			else: wiz.LogNotify(ADDONTITLE,'Fresh Install: [COLOR red]Cancelled![/COLOR]'); return
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			wiz.LogNotify(ADDONTITLE,'Fresh Install: [COLOR red]Skin Swap Failed![/COLOR]')
			return		
		xbmcPath=os.path.abspath(HOME)
		DP.create(ADDONTITLE,"Clearing all files and folders:",'', '')
		total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0;
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			EXCLUDES.append('My_Builds')
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				del_file += 1
				fold = root.split('\\')
				x = len(fold)-1
				print os.path.join(root,name)
				if name == 'sources.xml' and fold[x] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep Sources: %s\\%s" % (root, name))
				elif name == 'favourites.xml' and fold[x] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep Favourites: %s\\%s" % (root, name))
				elif name == 'profiles.xml' and fold[x] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep Profiles: %s\\%s" % (root, name))
				elif name == 'advancedsettings.xml' and fold[x] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s\\%s" % (root, name))
				elif name in LOGFILES: wiz.log("Keep Log File: %s" % name)
				elif name.endswith('.db'):
					try:os.remove(os.path.join(root,name))
					except: 
						wiz.log('Failed to delete, Purging DB')
						if name.find('Addon') and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV))
						else: wiz.purgeDb(os.path.join(root,name))
				else:
					DP.update(int(percentage(del_file, total_files)), '', 'File: [COLOR yellow]%s[/COLOR]' % name, '')
					try: os.remove(os.path.join(root,name))
					except: wiz.log("Error removing %s\\%s" % (root, name))
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				DP.update(100, '', 'Cleaning Up Empty Folder: [COLOR yellow]%s[/COLOR]' % name, '')
				if name not in ["Database","userdata","temp","addons","addon_data"]:
					shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
		DP.close()
		wiz.clearS('build')
		if install == 'restore': 
			DIALOG.ok(ADDONTITLE, "Your current setup for kodi has been cleared!", "Now we will install the local backup")
		elif install: 
			DIALOG.ok(ADDONTITLE, "Your current setup for kodi has been cleared!", "Now we will install: %s v%s" % (install, wiz.checkBuild(install,'version')))
			buildWizard(install, 'normal')
		else:
			DIALOG.ok(ADDONTITLE, "The process is complete, you're now back to a fresh Kodi configuration with %s" % ADDONTITLE,"Please reboot your system or restart Kodi in order for the changes to be applied.")
			wiz.killxbmc()
	else: 
		if not install == 'restore': wiz.LogNotify(ADDONTITLE,'Fresh Install: [COLOR red]Cancelled![/COLOR]'); xbmc.executebuiltin('Container.Refresh')

#############################
###DELETE CACHE##############
####THANKS GUYS @ NaN #######
def clearCache():
	if DIALOG.yesno(ADDONTITLE, 'Would you like to clear cache?', nolabel='Cancel',yeslabel='Delete'):
		wiz.clearCache()
		clearThumb()

def clearThumb():
	latest = wiz.latestDB('Textures')
	if DIALOG.yesno(ADDONTITLE, "Would you like to delete the %s and Thumbnails folder?" % latest, "They will repopulate on startup", nolabel='No, Cancel',yeslabel='Yes, Remove'):
		try: wiz.removeFile(os.join(DATABASE, latest))
		except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
		wiz.removeFolder(THUMBS)
		wiz.killxbmc()
	else: wiz.log('Clear thumbnames cancelled')

def purgeDb():
	DB = []; display = []
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIV >= 16: 
		choice = DIALOG.multiselect("Select DB File to Purge", display)
		if choice == None: wiz.LogNotify("Purge Database", "Cancelled")
		elif len(choice) == 0: wiz.LogNotify("Purge Database", "Cancelled")
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = DIALOG.select("Select DB File to Purge", display)
		if choice == -1: wiz.LogNotify("Purge Database", "Cancelled")
		else: wiz.purgeDb(DB[purge])

##########################
### DEVELOPER MENU #######
##########################
def testnotify():
	url = wiz.workingURL(NOTIFICATION)
	if url == True:
		link  = wiz.openURL(NOTIFICATION).replace('\r','').replace('\t','')
		id, msg = link.split('|||')
		notify.testNotification(msg)
	else: wiz.LogNotify(ADDONTITLE, "Invalid URL for Notification")

def testupdate():
	notify.updateWindow()

def testfirst():
	notify.firstRun()

###########################
## Making the Directory####
###########################

def addDir(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None):
	u='%s?mode=%s' % (sys.argv[0], urllib.quote_plus(mode))
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": ADDONTITLE} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None):
	u='%s?mode=%s' % (sys.argv[0], urllib.quote_plus(mode))
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": ADDONTITLE} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]

		return param

params=get_params()
url=None
name=None
mode=None

try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass

wiz.log('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ Url : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if wiz.getS('auto-view')=='true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % wiz.getS(viewType) )

if   mode==None             : index()

elif mode=='wizardupdate'   : wiz.wizardUpdate()
elif mode=='builds'         : buildMenu()
elif mode=='showupdate'     : showHide(name)
elif mode=='viewbuild'      : viewBuild(name)
elif mode=='install'        : buildWizard(name, url)
elif mode=='theme'          : buildWizard(name, mode, url)

elif mode=='maint'          : maintMenu()
elif mode=='clearcache'     : clearCache()
elif mode=='clearpackages'  : wiz.clearPackages()
elif mode=='clearcrash'     : wiz.clearCrash()
elif mode=='clearthumb'     : clearThumb()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='uploadlog'      : uploadLog.LogUploader()
elif mode=='viewlog'        : viewLogFile()
elif mode=='viewwizlog'     : viewWizLogFile()
elif mode=='clearwizlog'    : f = open(WIZLOG, 'w'); f.close(); wiz.LogNotify(ADDONTITLE, "Wizard Log Cleared!")
elif mode=='purgedb'        : purgeDb()
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify(ADDONTITLE, "Addon_Data reset")

elif mode=='apk'            : apkMenu()
elif mode=='apkinstall'     : apkInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); xbmc.executebuiltin('Container.Refresh')

elif mode=='trakt'          : traktMenu()
elif mode=='savetrakt'      : traktit.traktIt('update',      name)
elif mode=='restoretrakt'   : traktit.traktIt('restore',     name)
elif mode=='addontrakt'     : traktit.traktIt('clearaddon',  name)
elif mode=='cleartrakt'     : traktit.clearSaved(name)
elif mode=='authtrakt'      : traktit.activateTrakt(name); xbmc.executebuiltin('Container.Refresh')
elif mode=='updatetrakt'    : traktit.autoUpdate('all')
elif mode=='importtrakt'    : traktit.importlist(name); xbmc.executebuiltin('Container.Refresh')

elif mode=='realdebrid'     : realMenu()
elif mode=='savedebrid'     : debridit.debridIt('update',      name)
elif mode=='restoredebrid'  : debridit.debridIt('restore',     name)
elif mode=='addondebrid'    : debridit.debridIt('clearaddon',  name)
elif mode=='cleardebrid'    : debridit.clearSaved(name)
elif mode=='authdebrid'     : debridit.activateDebrid(name); xbmc.executebuiltin('Container.Refresh')
elif mode=='updatedebrid'   : debridit.autoUpdate('all')
elif mode=='importdebrid'   : debridit.importlist(name); xbmc.executebuiltin('Container.Refresh')

elif mode=='login'          : loginMenu()
elif mode=='savelogin'      : loginit.loginIt('update',      name)
elif mode=='restorelogin'   : loginit.loginIt('restore',     name)
elif mode=='addonlogin'     : loginit.loginIt('clearaddon',  name)
elif mode=='clearlogin'     : loginit.clearSaved(name)
elif mode=='authlogin'      : loginit.activateLogin(name); xbmc.executebuiltin('Container.Refresh')
elif mode=='updatelogin'    : loginit.autoUpdate('all')
elif mode=='importlogin'    : loginit.importlist(name); xbmc.executebuiltin('Container.Refresh')

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(); xbmc.executebuiltin('Container.Refresh')
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); xbmc.executebuiltin('Container.Refresh')

elif mode=='developer'      : developer()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='clearbackup'    : wiz.cleanHouse(os.path.join(HOME, 'My_Builds')); wiz.LogNotify(ADDONTITLE, "Backup Location: Cleared!")
elif mode=='restorezip'     : restoreit('build')
elif mode=='restoregui'     : restoreit('gui')
elif mode=='restoreextzip'  : restoreextit('build')
elif mode=='restoreextgui'  : restoreextit('gui')
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='testnotify'     : testnotify()
elif mode=='testupdate'     : testupdate()
elif mode=='testfirst'      : testfirst()

xbmcplugin.endOfDirectory(int(sys.argv[1]))