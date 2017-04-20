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
import gui,os,xbmcgui,xbmc,zipfile


userdatadb = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.streamhub.tvguide','source.db'))
if not os.path.isfile(userdatadb):

	target = xbmc.translatePath('special://home/userdata/addon_data/script.streamhub.tvguide')
	zip   = xbmc.translatePath(os.path.join('special://home/addons/script.streamhub.tvguide','source.zip'))
	if not os.path.exists(target):
		os.makedirs(target)
		
	zip_ref = zipfile.ZipFile(zip, 'r')
	zip_ref.extractall(target)
	zip_ref.close()


try:
    w = gui.TVGuide()
    w.doModal()
    del w

except Exception:
    xbmc.log('oops')
