#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmcaddon
import notification
import xbmc,os
import source
	
import os,xbmcgui,xbmc,zipfile


userdatadb = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.module.streamhub','source.db'))
if not os.path.isfile(userdatadb):

	target = xbmc.translatePath('special://home/userdata/addon_data/script.module.streamhub')
	zip   = xbmc.translatePath(os.path.join('special://home/addons/script.module.streamhub/resources/tvguide','source.zip'))
	if not os.path.exists(target):
		os.makedirs(target)
		
	zip_ref = zipfile.ZipFile(zip, 'r')
	zip_ref.extractall(target)
	zip_ref.close()

class Service(object):
    def __init__(self):
        self.database = source.Database()
        self.database.initialize(self.onInit)

    def onInit(self, success):
        if success:
            self.database.updateChannelAndProgramListCaches(self.onCachesUpdated)
        else:
            self.database.close()

    def onCachesUpdated(self):

        if ADDON.getSetting('notifications.enabled') == 'true':
            n = notification.Notification(self.database, ADDON.getAddonInfo('path'))
            n.scheduleNotifications()

        self.database.close(None)
		
xbmc.log('************************************************WORKING')

try:
    ADDON = xbmcaddon.Addon(id = 'script.module.streamhub')
    if ADDON.getSetting('cache.data.on.xbmc.startup') == 'true':
        Service()
except source.SourceNotConfiguredException:
    pass  # ignore
except Exception, ex:
    xbmc.log('[script.module.streamhub] Uncaugt exception in service.py: %s' % str(ex) , xbmc.LOGDEBUG)
