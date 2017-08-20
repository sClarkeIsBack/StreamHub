import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob, zipfile
import shutil
import urllib2,urllib
import re
import downloader
import extract
import uservar
import time
from datetime import date, datetime, timedelta
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from string import digits

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = xbmcaddon.Addon(ADDON_ID)
VERSION        = ADDON.getAddonInfo('version')
USER_AGENT     = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
LOG            = xbmc.translatePath('special://logpath/')
PROFILE        = xbmc.translatePath('special://profile/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
BACKUPLOCATION = os.path.join(HOME,      'My_Builds')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDOND         = os.path.join(USERDATA,  'addon_data')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES        = os.path.join(USERDATA,  'sources.xml')
GUISETTINGS    = os.path.join(USERDATA,  'guisettings.xml')
FAVOURITES     = os.path.join(USERDATA,  'favourites.xml')
PROFILES       = os.path.join(USERDATA,  'profiles.xml')
THUMBS         = os.path.join(USERDATA,  'Thumbnails')
DATABASE       = os.path.join(USERDATA,  'Database')
FANART         = os.path.join(PLUGIN,    'fanart.jpg')
ICON           = os.path.join(PLUGIN,    'icon.png')
ART            = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG         = os.path.join(ADDONDATA, 'wizard.log')
SKIN           = xbmc.getSkinDir()
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
EXCLUDES       = uservar.EXCLUDES
BUILDFILE      = uservar.BUILDFILE
APKFILE        = uservar.APKFILE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
AUTOINSTALL    = uservar.AUTOINSTALL
REPOADDONXML   = uservar.REPOADDONXML
REPOZIPURL     = uservar.REPOZIPURL
CONTACT        = uservar.CONTACT
LOGFILES       = ['xbmc.log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log']

###########################
###### Settings Items #####
###########################

def getS(name):
	try: return ADDON.getSetting(name)
	except: return False

def setS(name, value):
	try: ADDON.setSetting(name, value)
	except: return False

def openS():
	ADDON.openSettings()

def clearS(type):
	build   = {'buildname':'', 'buildversion':'', 'buildtheme':'', 'latestversion':'', 'lastbuildcheck':'2016-01-01'}
	install = {'installed':'false', 'extract':'', 'errors':''}
	default = {'defaultskinignore':'false', 'defaultskin':'', 'defaultskinname':''}
	if type == 'build':
		for set in build:
			setS(set, build[set])
		for set in install:
			setS(set, install[set])
		for set in default:
			setS(set, default[set])
	elif type == 'default':
		for set in default:
			setS(set, default[set])
	elif type == 'install':
		for set in install:
			setS(set, install[set])


###########################
###### Display Items ######
###########################

def TextBoxes(heading,announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def LogNotify(title,message,times=2000,icon=ICON):
	xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , times, icon))


###########################
###### Build Info #########
###########################

def checkBuild(name, ret):
	if not workingURL(BUILDFILE) == True: return False
	link = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for version, url, gui, kodi, theme, icon, fanart in match:
			if ret   == 'version': return version
			elif ret == 'url':     return url
			elif ret == 'gui':     return gui
			elif ret == 'kodi':    return kodi
			elif ret == 'theme':   return theme
			elif ret == 'icon':    return icon
			elif ret == 'fanart':  return fanart
			elif ret == 'all':     return '%s|||%s|||%s|||%s|||%s|||%s|||%s|||%s' % (name, version, url, gui, kodi, theme, icon, fanart)
	else: return False

def checkTheme(name, theme, ret):
	themeurl = checkBuild(name, 'theme')
	if not workingURL(themeurl) == True: return False
	link = openURL(themeurl).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % theme).findall(link)
	if len(match) > 0:
		for url, icon, fanart in match:
			if ret   == 'url':     return url
			elif ret == 'icon':    return icon
			elif ret == 'fanart':  return fanart
			elif ret == 'all':     return '%s|||%s|||%s|||%s|||%s' % (name, theme, url, icon, fanart)
	else: return False

def checkApk(name, ret):
	if not workingURL(APKFILE) == True: return False
	link = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for url, icon, fanart in match:
			if   ret == 'url':     return url
			elif ret == 'icon':    return icon
			elif ret == 'fanart':  return fanart
			elif ret == 'all':     return '%s|||%s|||%s|||%s' % (name, url, icon, fanart)
	else: return False

def checkWizard(ret):
	if not workingURL(WIZARDFILE) == True: return False
	link = openURL(WIZARDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('id="%s".+?ersion="(.+?)".+?ip="(.+?)"' % ADDON_ID).findall(link)
	if len(match) > 0:
		for version, zip in match:
			if ret   == 'version': return version
			elif ret == 'zip':     return zip
			elif ret == 'all':     return '%s|||%s|||%s' % (ADDON_ID, version, zip)
	else: return False

def buildCount(ver=None):
	link = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?odi="(.+?)".+?').findall(link)
	count = 0
	if len(match) > 0:
		for name, kodi in match:
			kodi = int(float(kodi))
			if ver == None: count += 1
			elif int(ver) == 16 and kodi >= 16: count += 1
			elif int(ver) == 15 and kodi <= 15: count += 1
	return count

###########################
###### URL Checks #########
###########################
 
def workingURL(url):
	if url == 'http://': return False
	try: 
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		response.close()
	except Exception, e:
		return e
	return True
 
def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###########################
###### Misc Functions #####
###########################

def Get_Keyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if keyboard.isConfirmed():
		return unicode( keyboard.getText(), "utf-8" )
	return default

def removeFolder(path):
	log("Deleting Folder: %s" % path)
	try: shutil.rmtree(path,ignore_errors=True, onerror=None)
	except: return False
	
def currSkin():
	return xbmc.getSkinDir()

def removeFile(path):
	log("Deleting File: %s" % path)
	try:    os.remove(path)
	except: return False

def cleanHouse(folder, ignore=False):
	total_files = 0; total_folds = 0
	for root, dirs, files in os.walk(folder):
		if ignore == False: dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files)
		if file_count >= 0:
			for f in files:
				try: 
					os.unlink(os.path.join(root, f))
					total_files += 1
				except: 
					try:
						shutil.rmtree(os.path.join(root, f))
					except:
						log("Error Deleting %s" % f)
			for d in dirs:
				total_folds += 1
				try: 
					shutil.rmtree(os.path.join(root, d))
					total_folds += 1
				except: 
					log("Error Deleting %s" % d)
	return '%s/%s' % (total_files, total_folds)

def emptyfolder(folder):
	total = 0
	for root, dirs, files in os.walk(folder, topdown=True):
		dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files) + len(dirs)
		if file_count == 0:
			shutil.rmtree(os.path.join(root))
			total += 1
			log("Empty Folder: %s" % root)
	return total

def log(log):
	xbmc.log("[%s]: %s" % (ADDONTITLE, log))
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
	with open(WIZLOG, 'a') as f:
		line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], log)
		f.write(line.rstrip('\r\n')+'\n')

def latestDB(DB):
	if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
		match = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
		comp = '%s(.+?).db' % DB[1:]
		highest = 0
		for file in match :
			try: check = int(re.compile(comp).findall(file)[0])
			except: check = 0
			if highest < check :
				highest = check
		return '%s%s.db' % (DB, highest)
	else: return False

def addonId(add):
	try: 
		return xbmcaddon.Addon(id=add)
	except:
		return False
	

def percentage(part, whole):
	return 100 * float(part)/float(whole)

def addonInfo(add, info):
	addon = addonId(add)
	if addon: return addon.getAddonInfo(info)
	else: return False

def forceUpdate():
	xbmc.executebuiltin('UpdateAddonRepos()')
	xbmc.executebuiltin('UpdateLocalAddons()')
	LogNotify(ADDONTITLE, 'Forcing Addon Updates')

def convertSpecial(url):
	DP.create(ADDONTITLE, "Changing Physical Paths To Special", "", "Please Wait")
	for root, dirs, files in os.walk(url):
		for file in files:
			if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
				DP.update(0,"Fixing", "[COLOR yellow]%s[/COLOR]" % file, "Please Wait")
				a = open((os.path.join(root, file))).read()
				encodedpath  = HOME.replace(':','%3a').replace('\\','%5c')
				extraslashes = HOME.replace('\\','\\\\')
				b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(extraslashes, 'special://home/')
				f = open((os.path.join(root, file)), mode='w')
				f.write(str(b))
				f.close()
	DP.close()
	log("[Convert Paths to Special] Complete")
	LogNotify("Convert Paths to Special", "[COLOR green]Complete![/COLOR]")

def latestApk(apk):
	if apk == "kodi":
		kodi  = "https://kodi.tv/download/"
		link  = openURL(kodi).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile("<h2>Current release:.+?odi v(.+?) &#8220;(.+?)&#8221;</h2>").findall(link)
		if len(match) == 1:
			ver    = match[0][0]
			title  = match[0][1]
			apkurl = "http://mirrors.kodi.tv/releases/android/arm/kodi-%s-%s-armeabi-v7a.apk" % (ver, title)
			return ver+'|||'+apkurl
		else: return False
		return ver+'|||'+apkurl
	elif apk == "spmc":
		spmc  = 'https://github.com/koying/SPMC/releases/latest/'
		link  = openURL(spmc).replace('\n','').replace('\r','').replace('\t','')
		match = re.compile(".+?class=\"release-title\">(.+?)</h1>.+?").findall(link)
		ver   = re.sub('<[^<]+?>', '', match[0]).replace(' ', '')
		apkurl = 'https://github.com/koying/SPMC/releases/download/%s-spmc/SPMC-armeabi-v7a_%s.apk' % (ver, ver)
		return ver+'|||'+apkurl

def clearCrash():  
	files = []
	for file in glob.glob(os.path.join(LOG, 'xbmc_crashlog*.*')):
		files.append(file)
	if len(files) > 0:
		if DIALOG.yesno(ADDONTITLE, 'Would you like to delete the Crash logs?', '%s Files Found' % len(files)):
			for f in files:
				os.remove(f)
			LogNotify('Clear Crash Logs', '%s Files Removed' % len(files))
		else: LogNotify('Clear Crash Logs', 'Cancelled')
	else: LogNotify('Clear Crash Logs', 'No Files Found')

def hidePassword():
	if DIALOG.yesno(ADDONTITLE, "Would you like to hide all passwords when typing in the add-on settings menus?"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = re.compile('<setting.+?id=(.+?).+?>').findall(f)
				for line in match:
					if 'pass' in line:
						if not 'option="hidden"' in line:
							try:
								change = line.replace('/', 'option="hidden" /')
								f.replace(line, change)
								count += 1
								log("[Hide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line))
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("Hide Passwords", "%s items changed" % count)
		log("[Hide Passwords] %s items changed" % count)
	else: log("[Hide Passwords] Cancelled")

def unhidePassword():
	if DIALOG.yesno(ADDONTITLE, "Would you like to unhide all passwords when typing in the add-on settings menus?"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = re.compile('<setting.+?id=(.+?).+?>').findall(f)
				for line in match:
					if 'pass' in line:
						if 'option="hidden"' in line:
							try:
								change = line.replace('option="hidden"', '')
								f.replace(line, change)
								count += 1
								log("[Unhide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line))
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("Unhide Passwords", "%s items changed" % count)
		log("[Unhide Passwords] %s items changed" % count)
	else: log("[Unhide Passwords] Cancelled")

def wizardUpdate(startup=None):
	if workingURL(WIZARDFILE):
		ver = checkWizard('version')
		zip = checkWizard('zip')
		if ver > VERSION:
			yes = DIALOG.yesno(ADDONTITLE, 'There is a new version of the %s!' % ADDONTITLE, 'Would you like to download v%s?' % ver, nolabel='Remind Me Later', yeslabel="Download")
			if yes:
				log("[Auto Update Wizard] Installing wizard v%s" % ver)
				DP.create(ADDONTITLE,'Downloading Update...','', 'Please Wait')
				lib=os.path.join(PACKAGES, '%s-%s.zip' % (ADDON_ID, ver))
				try: os.remove(lib)
				except: pass
				downloader.download(zip, lib, DP)
				xbmc.sleep(2000)
				DP.update(0,"", "Installing %s update" % ADDONTITLE)
				ext = extract.all(lib, ADDONS, DP, True)
				DP.close()
				xbmc.sleep(1000)
				xbmc.executebuiltin('UpdateAddonRepos()')
				xbmc.executebuiltin('UpdateLocalAddons()')
				xbmc.sleep(1000)
				LogNotify(ADDONTITLE,'Add-on updated')
				log("[Auto Update Wizard] Wizard updated to v%s" % ver)
				xbmc.executebuiltin('RunScript("%s/startup.py")' % ADDON_ID)
			else: log("[Auto Update Wizard] Install New Wizard Ignored: %s" % ver)
		else: 
			if not startup: LogNotify(ADDONTITLE, "No New Version of Wizard")
			log("[Auto Update Wizard] No New Version v%s" % ver)
	else: log("[Auto Update Wizard] Url for wizard file not valid: %s" % WIZARDFILE)

def chunks(s, n):
	for start in range(0, len(s), n):
		yield s[start:start+n]

def asciiCheck(use=None):
	if use == None:
		source   = DIALOG.browse(3, 'Select the folder you want to scan', 'files', HOME, False, False)
		yes      = DIALOG.yesno(ADDONTITLE,'Do you want to delete all filenames with special characters or would you rather just scan and view the results in the log?', yeslabel='Delete', nolabel='Scan')
	else: 
		source   = use
		yes      = DIALOG.yesno(ADDONTITLE,'Would you like to scan for non-ascii file names and remove them?', yeslabel='Yes Please!', nolabel='No Thanks!')
		if not yes: return

	if source == "":
		LogNotify(ADDONTITLE, "ASCII Check: Cancelled")
		return
	
	files_found  = os.path.join(ADDONDATA, 'asciifiles.txt')
	files_fails  = os.path.join(ADDONDATA, 'asciifails.txt')
	afiles       = open(files_found, mode='w+')
	afails       = open(files_fails, mode='w+')
	f1           = 0; f2           = 0
	items        = fileCount(source)
	msg          = ''
	prog         = []
	log("Source file: (%s)" % str(source))
	
	DP.create(ADDONTITLE, 'Please wait...')
	for base, dirs, files in os.walk(source):
		dirs[:] = [d for d in dirs]
		files[:] = [f for f in files]
		for file in files:
			prog.append(file) 
			prog2 = int(len(prog) / float(items) * 100)
			DP.update(prog2,"Checking for non ASCII files",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
			try:
				file.encode('ascii')
			except UnicodeDecodeError:
				badfile = os.path.join(base, file)
				if yes:
					try: 
						os.remove(badfile)
						for chunk in chunks(badfile, 75):
							afiles.write(chunk+'\n')
						afiles.write('\n')
						f1 += 1
						print "[ASCII Check] File Removed: %s " % badfile
					except:
						for chunk in chunks(badfile, 75):
							afails.write(chunk+'\n')
						afails.write('\n')
						f2 += 1
						print "[ASCII Check] File Failed: %s " % badfile
				else:
					for chunk in chunks(badfile, 75):
						afiles.write(chunk+'\n')
					afiles.write('\n')
					f1 += 1
					print "[ASCII Check] File Found: %s " % badfile
				pass
	DP.close(); afiles.close(); afails.close()
	total = int(f1) + int(f2)
	if total > 0:
		if os.path.exists(files_found): afiles = open(files_found, mode='r'); msg = afiles.read(); afiles.close()
		if os.path.exists(files_fails): afails = open(files_fails, mode='r'); msg2 = afails.read(); afails.close()
		if yes:
			if use:
				LogNotify(ADDONTITLE, "ASCII Check: %s Removed / %s Failed." % (f1, f2))
			else:
				TextBoxes(ADDONTITLE, "[COLOR yellow][B]%s Files Removed:[/B][/COLOR]\n %s\n\n[COLOR yellow][B]%s Files Failed:[B][/COLOR]\n %s" % (f1, msg, f2, msg2))
		else: 
			TextBoxes(ADDONTITLE, "[COLOR yellow][B]%s Files Found:[/B][/COLOR]\n %s" % (f1, msg))
	else: LogNotify(ADDONTITLE, "ASCII Check: None Found.")

def fileCount(home, excludes=True):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	item = []
	for base, dirs, files in os.walk(home):
		if excludes:
			dirs[:] = [d for d in dirs if d not in exclude_dirs]
			files[:] = [f for f in files if f not in exclude_files]
		for file in files:
			item.append(file)
	return len(item)

def defaultSkin():
	log("[Default Skin Check]")
	guif = open(GUISETTINGS, 'r+')
	msg = guif.read().replace('\n','').replace('\r','').replace('\t','').replace('    ',''); guif.close()
	log("Opening gui settings")
	match = re.compile('<lookandfeel>.+?<ski.+?>(.+?)</skin>.+?</lookandfeel>').findall(msg)
	log("Matches: %s" % str(match))
	if len(match) > 0:
		skinid = match[0]
		addonxml = os.path.join(ADDONS, match[0], 'addon.xml')
		if os.path.exists(addonxml):
			addf = open(addonxml, 'r+')
			msg2 = addf.read().replace('\n','').replace('\r','').replace('\t',''); addf.close()
			match2 = re.compile('<addon.+?ame="(.+?)".+?>').findall(msg2)
			if len(match2) > 0: skinname = match2[0]
			else: skinname = 'no match'
		else: skinname = 'no file'
		log("[Default Skin Check] Skin name: %s" % skinname)
		log("[Default Skin Check] Skin id: %s" % skinid)
		setS('defaultskin', skinid)
		setS('defaultskinname', skinname)
		setS('defaultskinignore', 'false')
	log("[Default Skin Check] End")

##########################
###BACK UP/RESTORE #######
##########################
def backUpOptions(type, name=""):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	if not os.path.exists(BACKUPLOCATION): os.makedirs(BACKUPLOCATION)
	if type == "build":
		if DIALOG.yesno(ADDONTITLE, "Are you sure you wish to backup the current build?", nolabel="No, Cancel", yeslabel="Yes, Continue"):
			if name == "":
				name = Get_Keyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			zipname       = os.path.join(BACKUPLOCATION, '%s.zip' % name)
			for_progress  = 0
			ITEM          = []
			if not DIALOG.yesno(ADDONTITLE, "Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', '%s addon_data is ignored' % ADDON_ID, yeslabel='Yes',nolabel='No'):
				exclude_dirs.append('addon_data')
			convertSpecial(HOME)
			asciiCheck(HOME)
			zipf = zipfile.ZipFile(zipname , 'w')
			DP.create("%s: Creating Zip" % ADDONTITLE, "Creating back up zip", "", "Please Wait...")
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM) 
						DP.update(int(progress), 'Creating back up zip: %s / %s' % (for_progress, N_ITEM), '[COLOR yellow]%s[/COLOR]'% file, 'Please Wait')
						fn = os.path.join(base, file)
						if not file in LOGFILES:
							try:
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
							except Exception, e:
								log("[Back Up] Type = '%s': Unable to backup %s" % (type, file))
								log("%s / %s" % (Exception, e))
						else: log("[Back Up] Type = '%s': Ignore %s" % (type, file))
					except Exception, e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file))
						log("%s / %s" % (Exception, e))
			zipf.close()
			xbmc.sleep(1000)
			DP.update(100, "Creating %s_guisettings.zip" % name, "", "")
			backUpOptions('guifix', name)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR yellow]%s[/COLOR] backup successful:" % name, "[COLOR yellow]%s[/COLOR]" % zipname)
	elif type == "guifix":
		if name == "":
			guiname = Get_Keyboard("","Please enter a name for the %s zip" % type)
			if not guiname: return False
		else: guiname = name
		guiname = urllib.quote_plus(guiname)
		guizipname = os.path.join(BACKUPLOCATION, '%s_guisettings.zip' % guiname)
		if os.path.exists(GUISETTINGS):
			zipf = zipfile.ZipFile(guizipname, mode='w')
			try:
				zipf.write(GUISETTINGS, 'guisettings.xml', zipfile.ZIP_DEFLATED)
				zipf.write(PROFILES,    'profiles.xml',    zipfile.ZIP_DEFLATED)
				match = glob.glob(os.path.join(ADDOND,'skin.*'))
				for fold in match:
					fd = fold[len(ADDOND)+1:]
					if not fd == 'skin.confluence':
						if DIALOG.yesno(ADDONTITLE, "Would you like to add the following skin folder to the guiFix Zip File?", "[COLOR yellow]%s[/COLOR]" % fd, yeslabel="Yes, Add", nolabel="No, Ignore"):
							for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
						else: log("[Back Up] Type = '%s': %s ignored" % (type, fold))
			except Exception, e:
				log("[Back Up] Type = '%s': %s / %s" % (type, Exception, e))
				pass
			zipf.close()
		else: log("[Back Up] Type = '%s': guisettings.xml not found" % type)
		if name == "":
			LogNotify("GuiFix Zip", "Created!")
	elif type == "theme":
		if not DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to create a theme backup?"): LogNotify("Theme Backup", "Cancelled!"); return False
		if name == "":
			themename = Get_Keyboard("","Please enter a name for the %s zip" % type)
			if not themename: return False
		else: themename = name
		themename = urllib.quote_plus(themename)
		zipname = os.path.join(BACKUPLOCATION, '%s.zip' % themename)
		zipf = zipfile.ZipFile(zipname, mode='w')
		try:
			if not SKIN == 'skin.confluence':
				skinfold = os.path.join(ADDONS, SKIN, 'media')
				match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
				if len(match2) > 1:
					if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to go through the Texture Files for?", "[COLOR yellow]%s[/COLOR]" % SKIN, yeslabel="Yes, Add", nolabel="No, Ignore"):
						skinfold = os.path.join(ADDONS, SKIN, 'media')
						match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
						for xbt in match2:
							if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to add the Texture File [COLOR yellow]%s[/COLOR]?" % xbt.replace(skinfold, "")[1:], "from [COLOR yellow]%s[/COLOR]" % SKIN, yeslabel="Yes, Add", nolabel="No, Ignore"):
								fn  = xbt
								fn2 = fn.replace(HOME, "")
								zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				else:
					for xbt in match2:
						if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to add the Texture File [COLOR yellow]%s[/COLOR]?" % xbt.replace(skinfold, "")[1:], "from [COLOR yellow]%s[/COLOR]" % SKIN, yeslabel="Yes, Add", nolabel="No, Ignore"):
							fn  = xbt
							fn2 = fn.replace(HOME, "")
							zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				ad_skin = os.path.join(ADDOND, SKIN, 'settings.xml')
				if os.path.exists(ad_skin):
					if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to go add the [COLOR yellow]settings.xml[/COLOR] in [COLOR yellow]/addon_data/[/COLOR] for?", "[COLOR yellow]%s[/COLOR]" % SKIN, yeslabel="Yes, Add", nolabel="No, Ignore"):
						skinfold = os.path.join(ADDOND, SKIN)
						zipf.write(ad_skin, ad_skin.replace(HOME, ""), zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to include a backgrounds folder?"):
				fn = DIALOG.browse(0, 'Select location of backgrounds', 'files', '', True, False, HOME, False)
				if not fn == HOME:
					for base, dirs, files in os.walk(fn):
						dirs[:] = [d for d in dirs if d not in exclude_dirs]
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							try:
								fn2 = os.path.join(base, file)
								zipf.write(fn2, fn2[len(HOME):], zipfile.ZIP_DEFLATED)
							except Exception, e:
								log("[Back Up] Type = '%s': Unable to backup %s" % (type, file))
								log("%s / %s" % (Exception, e))
				text = latestDB('Textures')
				if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to include the %s?" % text):
					zipf.write(os.path.join(DATABASE, text), '/userdata/Database/%s' % text, zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('%s: Theme Backup' % ADDONTITLE, "Would you like to include the guisettings.xml?"):
				zipf.write(GUISETTINGS, '/userdata/guisettings.xml', zipfile.ZIP_DEFLATED)
		except Exception, e:
			log("[Back Up] Type = '%s': %s / %s" % (type, Exception, e))
			pass
		zipf.close()
		DIALOG.ok(ADDONTITLE, "[COLOR yellow]%s[/COLOR] theme zip successful:" % themename, "[COLOR yellow]%s[/COLOR]" % zipname)

def restoreLocal(type):
	file = DIALOG.browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, HOME)
	log("[RESTORE BACKUP %s] File: %s " % (type.upper(), file))
	if file == "" or not file.endswith('.zip'):
		LogNotify(ADDONTITLE, "Local Restore: Cancelled")
		return
	DP.create(ADDONTITLE,'Installing Local Backup','', 'Please Wait')
	if type == "gui": loc = USERDATA
	else : loc = HOME
	log(loc)
	DP.update(0,'Installing Local Backup','', 'Please Wait')
	ext = extract.all(file,loc,DP)
	percent, errors, error = ext.split('/', 3)
	clearS('build')
	DP.close()
	defaultSkin()
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, 'INSTALLED %s: [ERRORS:%s]' % (percent, errors), 'Would you like to view the errors?', nolabel='No, Cancel',yeslabel='Yes, View')
		if yes:
			TextBoxes(ADDONTITLE, error.replace('\t',''))
	killxbmc()

def restoreExternal(type):
	source = DIALOG.browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False)
	if source == "" or not source.endswith('.zip'):
		LogNotify(ADDONTITLE, "External Restore: Cancelled")
		return
	try: 
		work = workingURL(source)
	except:
		LogNotify(ADDONTITLE, "External Restore: Error Valid URL")
		log("Not a working url, if source was local then use local restore option")
		log("External Source: %s" % source)
		return

	log("[RESTORE EXT BACKUP %s] File: %s " % (type.upper(), source))
	zipit = str(source).replace('\\', '/').split('/'); zname = zipit[len(zipit)-1]
	DP.create(ADDONTITLE,'Downloading Zip file','', 'Please Wait')
	if type == "gui": loc = USERDATA
	else : loc = HOME
	log(loc)

	if not os.path.exists(BACKUPLOCATION): os.makedirs(BACKUPLOCATION)
	file = os.path.join(BACKUPLOCATION, zname)
	downloader.download(source, file, DP)
	
	DP.update(0,'Installing Local Backup','', 'Please Wait')
	ext = extract.all(file,loc,DP)
	percent, errors, error = ext.split('/', 3)
	clearS('build')
	DP.close()
	defaultSkin()
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, 'INSTALLED %s: [ERRORS:%s]' % (percent, errors), 'Would you like to view the errors?', nolabel='No, Cancel',yeslabel='Yes, View')
		if yes:
			TextBoxes(ADDONTITLE, error.replace('\t',''))
	killxbmc()

##########################
###DETERMINE PLATFORM#####
##########################

def platform():
	if xbmc.getCondVisibility('system.platform.android'):   return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):   return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'): return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):	    return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):    return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):	    return 'ios'

def log_check():
	ret = False
	if os.path.exists(os.path.join(LOG,'xbmc.log')):
		ret = os.path.join(LOG,'xbmc.log')
	elif os.path.exists(os.path.join(LOG,'kodi.log')):
		ret = os.path.join(LOG,'kodi.log')
	elif os.path.exists(os.path.join(LOG,'spmc.log')):
		ret = os.path.join(LOG,'spmc.log')
	elif os.path.exists(os.path.join(LOG,'tvmc.log')):
		ret = os.path.join(LOG,'tvmc.log')
	return ret

def clearPackages(over=None):
	if os.path.exists(PACKAGES):
		try:	
			for root, dirs, files in os.walk(PACKAGES):
				file_count = 0
				file_count += len(files)
				# Count files and give option to delete
				if file_count > 0:
					if over: yes=1
					else: yes=DIALOG.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?", nolabel='No, Cancel',yeslabel='Yes, Remove')
					if yes:
						for f in files:	os.unlink(os.path.join(root, f))
						for d in dirs: shutil.rmtree(os.path.join(root, d))
						LogNotify(ADDONTITLE,'Clear Packages: [COLOR green]Success[/COLOR]!')
				else: LogNotify(ADDONTITLE,'Clear Packages: [COLOR red]None Found![/COLOR]')
		except: LogNotify(ADDONTITLE,'Clear Packages: [COLOR red]Error[/COLOR]!')
	else: LogNotify(ADDONTITLE,'Clear Packages: [COLOR red]None Found![/COLOR]')

def clearCache():
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	cachelist = [
		(PROFILEADDONDATA),
		(ADDONDATA),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDONDATA,'script.module.simple.downloader')),
		(os.path.join(ADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader')),
		(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images'))]
		
	delfiles = 0

	for item in cachelist:
		if os.path.exists(item) and not item in [ADDONDATA, PROFILEADDONDATA]:
			for root, dirs, files in os.walk(item):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					for f in files:
						if not f in LOGFILES:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass
						else: log('Ignore Log File: %s' % f)
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] cleared %s files from %s" % (str(file_count), os.path.join(item,d)))
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d))
		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower():
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] wiped %s " % os.path.join(item,d))
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d))

	LogNotify(ADDONTITLE,'Clear Cache: Removed %s Files' % delfiles)

#############################
####KILL XBMC ###############
#####THANKS GUYS @ TI########

def killxbmc():
	choice = DIALOG.yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
	if choice == 0: return
	elif choice == 1: pass
	myplatform = platform()
	log("Platform: " + str(myplatform))
	os._exit(1)
	log("Force close failed!  Trying alternate methods.")
	if myplatform == 'osx': # OSX
		log("############ try osx force close #################")
		try: os.system('killall -9 XBMC')
		except: pass
		try: os.system('killall -9 Kodi')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'linux': #Linux
		log("############ try linux force close #################")
		try: os.system('killall XBMC')
		except: pass
		try: os.system('killall Kodi')
		except: pass
		try: os.system('killall -9 xbmc.bin')
		except: pass
		try: os.system('killall -9 kodi.bin')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'android': # Android 
		log("############ try android force close #################")
		try: os.system('adb shell am force-stop org.xbmc.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc')
		except: pass		
		try: os.system('adb shell kill org.xbmc.kodi')
		except: pass
		try: os.system('adb shell kill org.kodi')
		except: pass
		try: os.system('adb shell kill org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell kill org.xbmc')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc());')
		except: pass
		DIALOG.ok(ADDONTITLE, "Press the HOME button on your remote and [COLOR=red][B]FORCE STOP[/COLOR][/B] KODI via the Manage Installed Applications menu in settings on your Amazon home page then re-launch KODI")
	elif myplatform == 'windows': # Windows
		log("############ try windows force close #################")
		try:
			os.system('@ECHO off')
			os.system('tskill XBMC.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('tskill Kodi.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im Kodi.exe /f')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im XBMC.exe /f')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
	else: #ATV
		log("############ try atv force close #################")
		try: os.system('killall AppleTV')
		except: pass
		log("############ try raspbmc force close #################") #OSMC / Raspbmc
		try: os.system('sudo initctl stop kodi')
		except: pass
		try: os.system('sudo initctl stop xbmc')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","iOS detected. Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")

##########################
### PURGE DATABASE #######
##########################
def purgeDb(name):
	#dbfile = name.replace('.db','').translate(None, digits)
	#if dbfile not in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']: return False
	#textfile = os.path.join(DATABASE, name)
	log('Purging DB %s.' % name)
	if os.path.exists(name):
		try:
			textdb = database.connect(name)
			textexe = textdb.cursor()
		except Exception, e:
			log(str(e))
			return False
	else: log('%s not found.' % name); return False
	textexe.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
	for table in textexe.fetchall():
		if table[0] == 'version': 
			log('Data from table `%s` skipped.' % table[0])
		else:
			try:
				textexe.execute("""DELETE FROM %s""" % table[0])
				textdb.commit()
				log('Data from table `%s` cleared.' % table[0])
			except e: log(str(e))
	log('%s DB Purging Complete.' % name)
	show = name.replace('\\', '/').split('/')
	LogNotify("Purge Database", "%s Complete" % show[len(show)-1])