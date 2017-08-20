import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
from datetime import date, datetime, timedelta
from resources.libs import extract, downloader, notify, loginit, debridit, traktit, skinSwitch, uploadLog, wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
VERSION        = wiz.addonInfo(ADDON_ID,'version')
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
PROFILE        = xbmc.translatePath('special://profile/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
FANART         = os.path.join(PLUGIN,   'fanart.jpg')
ICON           = os.path.join(PLUGIN,   'icon.png')
ART            = os.path.join(PLUGIN,   'resources', 'art')
SKIN           = xbmc.getSkinDir()
BUILDNAME      = wiz.getS('buildname')
DEFAULTSKIN    = wiz.getS('defaultskin')
DEFAULTNAME    = wiz.getS('defaultskinname')
DEFAULTIGNORE  = wiz.getS('defaultskinignore')
BUILDVERSION   = wiz.getS('buildversion')
BUILDLATEST    = wiz.getS('latestversion')
BUILDCHECK     = wiz.getS('lastbuildcheck')
AUTOCLEANUP    = wiz.getS('autoclean')
AUTOCACHE      = wiz.getS('clearcache')
AUTOPACKAGES   = wiz.getS('clearpackages')
TRAKTSAVE      = wiz.getS('traktlastsave')
REALSAVE       = wiz.getS('debridlastsave')
LOGINSAVE      = wiz.getS('loginlastsave')
KEEPTRAKT      = wiz.getS('keeptrakt')
KEEPREAL       = wiz.getS('keepdebrid')
KEEPLOGIN      = wiz.getS('keeplogin')
INSTALLED      = wiz.getS('installed')
EXTRACT        = wiz.getS('extract')
EXTERROR       = wiz.getS('errors')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid') 
NOTEID         = 0 if NOTEID == "" else int(NOTEID)
NOTEDISMISS    = wiz.getS('notedismiss')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
EXCLUDES       = uservar.EXCLUDES
BUILDFILE      = uservar.BUILDFILE
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
HEADERMESSAGE  = uservar.HEADERMESSAGE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
AUTOINSTALL    = uservar.AUTOINSTALL
REPOID         = uservar.REPOID
REPOADDONXML   = uservar.REPOADDONXML
REPOZIPURL     = uservar.REPOZIPURL
WORKING        = True if wiz.workingURL(BUILDFILE) == True else False
failed         = False

###########################
#### Check Updates   ######
###########################
def checkUpdate():
	BUILDNAME      = wiz.getS('buildname')
	BUILDVERSION   = wiz.getS('buildversion')
	link           = wiz.openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match          = re.compile('name="%s".+?ersion="(.+?)"' % BUILDNAME).findall(link)
	if len(match) > 0:
		version = match[0]
		wiz.setS('latestversion', version)
		if version > BUILDVERSION:
			notify.updateWindow()
		else: wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s]" % (BUILDVERSION, version))
	else: wiz.log("[Check Updates] ERROR: Unable to find build version in build text file")

def checkSkin():
	wiz.log("[Build Check] Invalid Skin Check Start")
	DEFAULTSKIN   = wiz.getS('defaultskin')
	DEFAULTNAME   = wiz.getS('defaultskinname')
	DEFAULTIGNORE = wiz.getS('defaultskinignore')
	if not DEFAULTSKIN == '':
		if os.path.exists(os.path.join(ADDONS, DEFAULTSKIN)):
			if DIALOG.yesno(ADDONTITLE, "It seems that the skin has been set back to [COLOR yellow]%s[/COLOR]" % SKIN[5:].title(), "Would you like to set the skin back to:", '[COLOR yellow]%s[/COLOR]' % DEFAULTNAME):
				gotoskin = DEFAULTSKIN
				gotoname = DEFAULTNAME
			else: wiz.log("Skin was not reset"); wiz.setS('defaultskinignore', 'true')
		else: wiz.setS('defaultskin', ''); wiz.setS('defaultskinname', ''); DEFAULTSKIN = ''; DEFAULTNAME = ''
	if DEFAULTSKIN == '':
		skinname = []
		skinlist = []
		for folder in glob.glob(os.path.join(ADDONS, 'skin.*/')):
			xml = "%s/addon.xml" % folder
			if os.path.exists(xml):
				f  = open(xml,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
				match = re.compile('<addon.+?id="(.+?)".+?>').findall(g)
				match2 = re.compile('<addon.+?name="(.+?)".+?>').findall(g)
				wiz.log("%s: %s" % (folder, str(match[0])))
				if len(match) > 0: skinlist.append(str(match[0])); skinname.append(str(match2[0]))
				else: wiz.log("ID not found for %s" % folder)
			else: wiz.log("ID not found for %s" % folder)
		if len(skinlist) > 0:
			if len(skinlist) > 1:
				if DIALOG.yesno(ADDONTITLE, "It seems that the skin has been set back to [COLOR yellow]%s[/COLOR]" % SKIN[5:].title(), "Would you like to view a list of avaliable skins?"):
					choice = DIALOG.select("Select skin to switch to!", skinname)
					if choice == -1: wiz.log("Skin was not reset"); wiz.setS('defaultskinignore', 'true')
					else: 
						gotoskin = skinlist[choice]
						gotoname = skinname[choice]
				else: wiz.log("Skin was not reset"); wiz.setS('defaultskinignore', 'true')
			else:
				if DIALOG.yesno(ADDONTITLE, "It seems that the skin has been set back to [COLOR yellow]%s[/COLOR]" % SKIN[5:].title(), "Would you like to set the skin back to:", '[COLOR yellow]%s[/COLOR]' % skinname[0]):
					gotoskin = skinlist[0]
					gotoname = skinname[0]
				else: wiz.log("Skin was not reset"); wiz.setS('defaultskinignore', 'true')
		else: wiz.log("No skins found in addons folder."); wiz.setS('defaultskinignore', 'true')
	if gotoskin:
		skinSwitch.swapSkins(gotoskin)
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
			wiz.LogNotify("Skin Swap", 'Skin reset to %s' % gotoname)
		else: 
			wiz.LogNotify(ADDONTITLE,'[COLOR red]Skin Swap Timed Out![/COLOR]')
	wiz.log("[Build Check] Invalid Skin Check End")

while xbmc.Player().isPlayingVideo():
	xbmc.sleep(1000)

wiz.log("[Path Check] Started")
id   = xbmcaddon.Addon().getAddonInfo('id')
path = xbmcaddon.Addon().getAddonInfo('path').replace(ADDONS,'')[1:]
if not id == path: DIALOG.ok(ADDONTITLE, 'Please make sure that the plugin folder is the', 'Same as the ADDON_ID.'); wiz.log("[Path Check] ADDON_ID and plugin folder doesnt match. %s / %s " % (id, path))
else: wiz.log("[Path Check] Good!")

wiz.log("[Auto Clean Up] Started")
if AUTOCLEANUP == 'true':
	if AUTOCACHE == 'true': wiz.log('[Auto Clean Up] Cache: On'); wiz.clearCache()
	else: wiz.log('[Auto Clean Up] Cache: Off')
	if AUTOPACKAGES == 'true': wiz.log('[Auto Clean Up] Packages: On'); wiz.clearPackages('startup')
	else: wiz.log('[Auto Clean Up] Packages: Off')
else: wiz.log('[Auto Clean Up] Turned off')

wiz.log("[Auto Install Repo] Started")
if AUTOINSTALL == 'Yes' and not os.path.exists(os.path.join(ADDONS, REPOID)):
	workingxml = wiz.workingURL(REPOADDONXML)
	if workingxml == True:
		link    = wiz.openURL(REPOADDONXML).replace('\n','').replace('\r','').replace('\t','')
		match   = re.compile('<addon.+?id="%s".+?ersion="(.+?)".+?>' % REPOID).findall(link)
		installzip = '%s-%s.zip' % (REPOID, match[0])
		workingrepo = wiz.workingURL(REPOZIPURL+installzip)
		if workingrepo == True:
			DP.create(ADDONTITLE,'Downloading Repo...','', 'Please Wait')
			if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
			lib=os.path.join(PACKAGES, installzip)
			try: os.remove(lib)
			except: pass
			downloader.download(REPOZIPURL+installzip,lib, DP)
			extract.all(lib, ADDONS, DP)
			f = open(os.path.join(ADDONS, REPOID, 'addon.xml'), mode='r').read()
			match = re.compile('<addon.+?id="%s".+?ame="(.+?)".+?>' % REPOID).findall(f)
			wiz.LogNotify(match[0], "Add-on updated", icon=os.path.join(ADDONS, REPOID, 'icon.png'))
			xbmc.sleep(1000)
			xbmc.executebuiltin('UpdateAddonRepos()')
			xbmc.executebuiltin('UpdateLocalAddons()')
			xbmc.sleep(1000)
			wiz.log("[Auto Install Repo] Successfully Installed")
		else: 
			wiz.LogNotify("Repo Install Error", "Invalid url for zip!")
			wiz.log("[Auto Install Repo] Was unable to create a working url for repository. %s" % workingrepo)
	else: 
		wiz.LogNotify("Repo Install Error", "Invalid addon.xml file!")
		wiz.log("[Auto Install Repo] Unable to read the addon.xml file.")
elif not AUTOINSTALL == 'Yes': wiz.log("[Auto Install Repo] Not Enabled")
elif os.path.exists(os.path.join(ADDONS, REPOID)): wiz.log("[Auto Install Repo] Repository already installed")

wiz.log("[Auto Update Wizard] Started")
if AUTOUPDATE == 'Yes':
	wiz.wizardUpdate('startup')
else: wiz.log("[Auto Update Wizard] Not Enabled")

wiz.log("[Notifications] Started")
if ENABLE == 'Yes':
	if not NOTIFY == 'true':
		url = wiz.workingURL(NOTIFICATION)
		if url == True:
			link  = wiz.openURL(NOTIFICATION).replace('\r','').replace('\t','')
			id, msg = link.split('|||')
			if int(id) == int(NOTEID):
				if NOTEDISMISS == 'false':
					notify.notification(msg=msg)
				else: wiz.log("[Notifications] id[%s] Dismissed" % int(id))
			elif int(id) > int(NOTEID):
				wiz.log("[Notifications] id: %s" % str(int(id)))
				wiz.setS('noteid', str(int(id)))
				wiz.setS('notedismiss', 'false')
				notify.notification(msg=msg)
				wiz.log("[Notifications] Complete")
		else: wiz.log("[Notifications] URL(%s): %s" % (NOTIFICATION, url))
	else: wiz.log("[Notifications] Turned Off")
else: wiz.log("[Notifications] Not Enabled")

wiz.log("[Installed Check] Started")
if INSTALLED == 'true':
	if not EXTRACT == '100':
		wiz.log("[Installed Check] Build was extracted %s/100 with [ERRORS: %s]" % (EXTRACT, EXTERROR))
		yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'Installed: %s / Error Count:%s' % (EXTRACT, EXTERROR), 'Would you like to try again?', nolabel='No Thanks!', yeslabel='Yes Please!')
		wiz.clearS('build')
		failed = True
		if yes: 
			xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=fresh)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
			wiz.log("[Installed Check] Fresh Installed Re-activated")
		else: wiz.log("[Installed Check] Reinstall Ignored")
	elif SKIN in ['skin.confluence', 'skin.estuary']:
		wiz.log("[Installed Check] Incorrect skin: %s" % SKIN)
		gui = wiz.checkBuild(BUILDNAME, 'gui')
		failed = True
		if gui == 'http://':
			wiz.log("[Installed Check] Guifix was set to http://")
			DIALOG.ok(ADDONTITLE, "It looks like the skin settings was not applied to the build.", "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close")
		elif wiz.workingURL(gui):
			yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'It looks like the skin settings was not applied to the build.', 'Would you like to apply the guiFix?', nolabel='No Thanks!', yeslabel='Yes Please!')
			if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=gui)" % (ADDON_ID, urllib.quote_plus(BUILDNAME))); wiz.log("[Installed Check] Guifix attempting to install")
			else: wiz.log('[Installed Check] Guifix url working but cancelled: %s' % gui)
		else:
			DIALOG.ok(ADDONTITLE, "It looks like the skin settings was not applied to the build.", "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close")
			wiz.log('[Installed Check] Guifix url not working: %s' % gui)
	else:
		wiz.log('[Installed Check] Install seems to be completed correctly')
	if KEEPTRAKT == 'true': traktit.traktIt('restore', 'all'); wiz.log('[Installed Check] Restoring Trakt Data')
	if KEEPREAL  == 'true': debridit.debridIt('restore', 'all'); wiz.log('[Installed Check] Restoring Real Debrid Data')
	if KEEPLOGIN == 'true': loginit.loginIt('restore', 'all'); wiz.log('[Installed Check] Restoring Login Data')
	wiz.clearS('install')
else: wiz.log("[Installed Check] Not Enabled")

if failed == False:
	wiz.log("[Build Check] Started")
	if not WORKING:
		wiz.log("[Build Check] Not a valid URL for Build File: %s" % BUILDFILE)
	elif BUILDCHECK == '' and BUILDNAME == '':
		wiz.log("[Build Check] First Run")
		notify.firstRun()
		wiz.setS('lastbuildcheck', str(NEXTCHECK))
	elif not BUILDNAME == '':
		wiz.log("[Build Check] Build Installed")
		if SKIN in ['skin.confluence', 'skin.estuary'] and not DEFAULTIGNORE == 'true':
			checkSkin()
			wiz.log("[Build Check] Build Installed: Checking Updates")
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			checkUpdate()
		elif BUILDCHECK <= str(TODAY):
			wiz.log("[Build Check] Build Installed: Checking Updates")
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			checkUpdate()
		else: 
			wiz.log("[Build Check] Build Installed: Next check isnt until: %s / TODAY is: %s" % (BUILDCHECK, str(TODAY)))

wiz.log("[Trakt Data] Started")
if KEEPTRAKT == 'true':
	if TRAKTSAVE <= str(TODAY):
		wiz.log("[Trakt Data] Saving all Data")
		traktit.autoUpdate('all')
		wiz.setS('traktlastsave', str(THREEDAYS))
	else: 
		wiz.log("[Trakt Data] Next Auto Save isnt until: %s / TODAY is: %s" % (TRAKTSAVE, str(TODAY)))
else: wiz.log("[Trakt Data] Not Enabled")

wiz.log("[Real Debrid Data] Started")
if KEEPREAL == 'true':
	if REALSAVE <= str(TODAY):
		wiz.log("[Real Debrid Data] Saving all Data")
		debridit.autoUpdate('all')
		wiz.setS('debridlastsave', str(THREEDAYS))
	else: 
		wiz.log("[Real Debrid Data] Next Auto Save isnt until: %s / TODAY is: %s" % (REALSAVE, str(TODAY)))
else: wiz.log("[Real Debrid Data] Not Enabled")

wiz.log("[Login Data] Started")
if KEEPLOGIN == 'true':
	if LOGINSAVE <= str(TODAY):
		wiz.log("[Login Data] Saving all Data")
		loginit.autoUpdate('all')
		wiz.setS('loginlastsave', str(THREEDAYS))
	else: 
		wiz.log("[Login Data] Next Auto Save isnt until: %s / TODAY is: %s" % (LOGINSAVE, str(TODAY)))
else: wiz.log("[Login Data] Not Enabled")