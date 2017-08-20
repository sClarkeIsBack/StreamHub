import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
from resources.libs import wizard as wiz
from datetime import date, datetime, timedelta

ADDON_ID       = uservar.ADDON_ID
ADDON          = wiz.addonId(ADDON_ID)
ADDONTITLE     = uservar.ADDONTITLE
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
PACKAGES       = os.path.join(ADDONS,   'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
FANART         = os.path.join(PLUGIN,   'fanart.jpg')
ICON           = os.path.join(PLUGIN,   'icon.png')
ART            = os.path.join(PLUGIN,   'resources', 'art')
NOTIFY         = wiz.getS('notify')
NOTEID         = wiz.getS('noteid')
NOTEDISMISS    = wiz.getS('notedismiss')
BUILDNAME      = wiz.getS('buildname')
BUILDVERSION   = wiz.getS('buildversion')
LATESTVERSION  = wiz.checkBuild(BUILDNAME, 'version')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
UPDATECHECK    = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
FONTSETTINGS   = uservar.FONTSETTINGS if not uservar.FONTSETTINGS == '' else "Font14"
BACKGROUND     = uservar.BACKGROUND if not uservar.BACKGROUND == '' or not wiz.workingURL(uservar.BACKGROUND) else FANART
HEADERTYPE     = uservar.HEADERTYPE if uservar.HEADERTYPE == 'Image' else 'Text'
HEADERMESSAGE  = uservar.HEADERMESSAGE
FONTHEADER     = uservar.FONTHEADER if not uservar.FONTHEADER == '' else "Font16"
HEADERIMAGE    = uservar.HEADERIMAGE
THEME1         = uservar.THEME1
THEME2         = uservar.THEME2
THEME3         = uservar.THEME3
THEME4         = uservar.THEME4
THEME5         = uservar.THEME5
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2

############################
###NOTIFICATIONS############
####THANKS GUYS @ TVADDONS##
######MODIFIED BY AFTERMATH#
ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?

def notification(msg='', resize=False, L=0 ,T=0 ,W=1280 ,H=720 , TxtColor='0xFFFFFFFF', Font=FONTSETTINGS, BorderWidth=15):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
			self.addControl(self.BG)
			#title
			if HEADERTYPE == 'Image':
				iLogoW=144; iLogoH=68
				self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
				self.addControl(self.iLogo)
			else:
				title = HEADERMESSAGE
				times = int(float(FONTHEADER[-2:]))
				temp = title.replace('[', '<').replace(']', '>')
				temp = re.sub('<[^<]+?>', '', temp)
				title_width = len(str(temp))*(times - 1)
				title = THEME3 % title
				self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
				self.addControl(self.title)
				self.title.setText(title)
			#body
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			space   = int(L+(BorderWidth*1.5))
			dismiss = int(space+w1+BorderWidth)
			later   = int(dismiss+w1+BorderWidth)
			
			self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"Dismiss",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonRemindMe=xbmcgui.ControlButton(later,t,w1,h1,"Remind Me Later",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonDismiss); self.addControl(self.buttonRemindMe)
			self.buttonRemindMe.controlLeft(self.buttonDismiss); self.buttonRemindMe.controlRight(self.buttonDismiss)
			self.buttonDismiss.controlLeft(self.buttonRemindMe); self.buttonDismiss.controlRight(self.buttonRemindMe)
			self.setFocus(self.buttonRemindMe);

		def doRemindMeLater(self):
			try:
				wiz.setS("notedismiss","false")
				wiz.log("[Notification] NotifyID %s Remind Me Later" % wiz.getS('noteid'))
			except: pass
			self.CloseWindow()

		def doDismiss(self):
			try:    
				wiz.setS("notedismiss","true")
				wiz.log("[Notification] NotifyID %s Dismissed" % wiz.getS('noteid'))
			except: pass
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()

		def onControl(self,control):
			if   control==self.buttonRemindMe: self.doRemindMeLater()
			elif control== self.buttonDismiss: self.doDismiss()
			else:
				try:    self.setFocus(self.buttonRemindMe)
				except: pass
		
		def CloseWindow(self): self.close()
	if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth)
	TempWindow.doModal()
	del TempWindow

def testNotification(msg='', resize=False, L=0 ,T=0 ,W=1280 ,H=720 , TxtColor='0xFFFFFFFF', Font=FONTSETTINGS, BorderWidth=15):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border)
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
			self.addControl(self.BG)
			#title
			if HEADERTYPE == 'Image':
				iLogoW=144; iLogoH=68
				self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
				self.addControl(self.iLogo); 
			else:
				title = HEADERMESSAGE
				times = int(float(FONTHEADER[-2:]))
				temp = title.replace('[', '<').replace(']', '>')
				temp = re.sub('<[^<]+?>', '', temp)
				title_width = len(str(temp))*(times - 1)
				title = THEME3 % title
				self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
				self.addControl(self.title)
				self.title.setText(title)
			#body
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			space   = int(L+(BorderWidth*1.5))
			dismiss = int(space+w1+BorderWidth)
			later   = int(dismiss+w1+BorderWidth)
			
			self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"Dismiss",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonRemindMe=xbmcgui.ControlButton(later,t,w1,h1,"Remind Me Later",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonDismiss); self.addControl(self.buttonRemindMe)
			self.buttonRemindMe.controlLeft(self.buttonDismiss); self.buttonRemindMe.controlRight(self.buttonDismiss)
			self.buttonDismiss.controlLeft(self.buttonRemindMe); self.buttonDismiss.controlRight(self.buttonRemindMe)
			self.setFocus(self.buttonRemindMe)

		def doRemindMeLater(self):
			wiz.log("[Test Notification] Remind Me Later")
			self.CloseWindow()

		def doDismiss(self):
			wiz.log("[Test Notification] Dismiss")
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()

		def onControl(self,control):
			if   control==self.buttonRemindMe: self.doRemindMeLater()
			elif control== self.buttonDismiss: self.doDismiss()
			else:
				try:    self.setFocus(self.buttonRemindMe)
				except: pass

		def CloseWindow(self): self.close()
	if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal()
	del TempWindow

def updateWindow(TxtColor='0xFFFFFFFF', Font='font13', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
			if BUILDNAME == "" or not wiz.checkBuild(BUILDNAME, 'version'):
				bgArt   = ICON
				icon    = ICON
				build   = "Test Window"
				version = '1.0'
				latest  = '1.0'
			else:
				bgArt   = wiz.checkBuild(BUILDNAME, 'fanart')
				icon    = wiz.checkBuild(BUILDNAME, 'icon')
				build   = BUILDNAME
				version = BUILDVERSION
				latest  = wiz.checkBuild(BUILDNAME, 'version')
			wiz.log(bgArt)
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth, T+BorderWidth, W-(BorderWidth*2), H-(BorderWidth*2), bgArt, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.BG)
			#title
			times = int(float(Font[-2:]))
			title = ADDONTITLE
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title   = THEME2 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#update
			if version < latest: msg = "Update avaliable for installed build:\n[COLOR %s]%s[/COLOR]\n\nCurrent Version: v[COLOR %s]%s[/COLOR]\nLatest Version: v[COLOR %s]%s[/COLOR]\n\n[COLOR %s]*Recommened: Fresh install[/COLOR]" % (COLOR1, build, COLOR1, version, COLOR1, latest, COLOR1)
			else: msg = "Running latest version of installed build:\n[COLOR %s]%s[/COLOR]\n\nCurrent Version: v[COLOR %s]%s[/COLOR]\nLatest Version: v[COLOR %s]%s[/COLOR]\n\n[COLOR %s]*Recommened: Fresh install[/COLOR]" % (COLOR1, build, COLOR1, version, COLOR1, latest, COLOR1)
			msg = THEME2 % msg
			self.update=xbmcgui.ControlTextBox(L+(BorderWidth*2),T+BorderWidth+30,W-150-(BorderWidth*3),H-(BorderWidth*2)-30,font=Font,textColor=TxtColor)
			self.addControl(self.update)
			self.update.setText(msg)
			#icon
			self.Icon=xbmcgui.ControlImage(L+W-(BorderWidth*2)-150, T+BorderWidth+35, 150, 150, icon, aspectRatio=0, colorDiffuse='0xAFFFFFFF')
			self.addControl(self.Icon)
			#buttons
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			fresh   = int(L+(BorderWidth*1.5))
			normal  = int(fresh+w1+BorderWidth)
			ignore  = int(normal+w1+BorderWidth)
			
			self.buttonFRESH=xbmcgui.ControlButton(fresh,t, w1,h1,"Fresh Install",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonNORMAL=xbmcgui.ControlButton(normal,t,w1,h1,"Normal Install",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonIGNORE=xbmcgui.ControlButton(ignore,t,w1,h1,"Ignore 3 days",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonFRESH); self.addControl(self.buttonNORMAL); self.addControl(self.buttonIGNORE)
			self.buttonIGNORE.controlLeft(self.buttonNORMAL); self.buttonIGNORE.controlRight(self.buttonFRESH)
			self.buttonNORMAL.controlLeft(self.buttonFRESH); self.buttonNORMAL.controlRight(self.buttonIGNORE)
			self.buttonFRESH.controlLeft(self.buttonIGNORE); self.buttonFRESH.controlRight(self.buttonNORMAL)
			self.setFocus(self.buttonFRESH)

		def doFreshInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Fresh Install build]" % (BUILDVERSION, LATESTVERSION))
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK))
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=install&name=%s&url=fresh' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doNormalInstall(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Normal Install build]" % (BUILDVERSION, LATESTVERSION))
			wiz.log("[Check Updates] [Next Check: %s]" % str(NEXTCHECK))
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=install&name=%s&url=normal' % (ADDON_ID, urllib.quote_plus(BUILDNAME))
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		def doIgnore(self):
			wiz.log("[Check Updates] [Installed Version: %s] [Current Version: %s] [User Selected: Ignore 3 Days]" % (BUILDVERSION, LATESTVERSION))
			wiz.log("[Check Updates] [Next Check: %s]" % str(THREEDAYS))
			wiz.setS('lastbuildcheck', str(THREEDAYS))
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()
			elif action == ACTION_MOVE_LEFT and not F: self.setFocus(self.buttonIGNORE)
			elif action == ACTION_MOVE_RIGHT and not F: self.setFocus(self.buttonIGNORE)

		def onControl(self,control):
			if   control==self.buttonIGNORE: self.doIgnore()
			elif control==self.buttonNORMAL: self.doNormalInstall()
			elif control==self.buttonFRESH:  self.doFreshInstall()
			else:
				try:    self.setFocus(self.buttonIGNORE); 
				except: pass

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(350); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

def firstRun(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
			self.addControl(self.BG)
			#title
			title = ADDONTITLE
			times = int(float(Font[-2:]))
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title   = THEME3 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#welcome message
			msg   = "Currently no build installed from %s.\n\nSelect 'Build Menu' to install a Community Build from us or 'Ignore' to never see this message again.\n\nThank you for choosing %s." % (ADDONTITLE, ADDONTITLE)
			msg   = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+(BorderWidth*2),T+30+BorderWidth,W-(BorderWidth*4),H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			#buttons
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1        = int((W-(BorderWidth*5))/3); h1 = 35
			t         = int(T+H-h1-(BorderWidth*1.5))
			save      = int(L+(BorderWidth*1.5))
			buildmenu = int(save+w1+BorderWidth)
			ignore    = int(buildmenu+w1+BorderWidth)
			self.buttonSAVEMENU=xbmcgui.ControlButton(save,t,w1,h1,"Save Data Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonBUILDMENU=xbmcgui.ControlButton(buildmenu,t,w1,h1,"Build Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonIGNORE=xbmcgui.ControlButton(ignore,t,w1,h1,"Ignore",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonSAVEMENU); self.addControl(self.buttonBUILDMENU); self.addControl(self.buttonIGNORE)
			self.buttonIGNORE.controlLeft(self.buttonBUILDMENU); self.buttonIGNORE.controlRight(self.buttonSAVEMENU)
			self.buttonBUILDMENU.controlLeft(self.buttonSAVEMENU); self.buttonBUILDMENU.controlRight(self.buttonIGNORE)
			self.buttonSAVEMENU.controlLeft(self.buttonIGNORE); self.buttonSAVEMENU.controlRight(self.buttonBUILDMENU)
			self.setFocus(self.buttonIGNORE)

		def doSaveMenu(self):
			wiz.log("[Check Updates] [User Selected: Open Save Data Menu] [Next Check: %s]" % str(NEXTCHECK))
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=savedata' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)

		def doBuildMenu(self):
			wiz.log("[Check Updates] [User Selected: Open Build Menu] [Next Check: %s]" % str(NEXTCHECK))
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=builds' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)

		def doIgnore(self):
			wiz.log("[First Run] [User Selected: Ignore Build Menu] [Next Check: %s]" % str(NEXTCHECK))
			wiz.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()
			elif action == ACTION_MOVE_LEFT and not F: self.setFocus(self.buttonBUILDMENU)
			elif action == ACTION_MOVE_RIGHT and not F: self.setFocus(self.buttonIGNORE)

		def onControl(self,control):
			if   control==self.buttonIGNORE: self.doIgnore()
			elif control==self.buttonBUILDMENU:  self.doBuildMenu()
			elif control==self.buttonSAVEMENU:  self.doSaveMenu()
			else:
				try:    self.setFocus(self.buttonIGNORE); 
				except: pass

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(300); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow

def contact(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
			self.addControl(self.BG)
			#title
			title = ADDONTITLE
			times = int(float(Font[-2:]))
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title = THEME3 % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			#icon
			self.Icon=xbmcgui.ControlImage(L+(BorderWidth*2), T+BorderWidth+40, 150, 150, ICON, aspectRatio=0, colorDiffuse='0xAFFFFFFF')
			self.addControl(self.Icon)
			#welcome message
			msg = THEME2 % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+160+(BorderWidth*3),T+45,W-170-(BorderWidth*3),H-(BorderWidth*2)-50,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)

		def doExit(self):
			self.CloseWindow()

		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doExit()
			elif action == ACTION_NAV_BACK: self.doExit()

		def CloseWindow(self): self.close()

	maxW=1280; maxH=720; W=int(700); H=int(250); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow