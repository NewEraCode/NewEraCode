# -*- coding: utf-8 -*-
import xbmcaddon #@UnresolvedImport
import xbmc, xbmcgui #@UnresolvedImport
import sys, os, time, re, traceback
import elementtree.ElementTree as etree #@UnresolvedImport
#import jsonrpc
import difflib, htmlentitydefs


__addon__ = xbmcaddon.Addon(id='script.enigma')
__version__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources') ).decode('utf-8')
sys.path.append (BASE_RESOURCE_PATH)

IMAGE_PATH = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path'), 'resources', 'skin','Default','media') ).decode('utf-8')
THUMB_PATH = xbmc.translatePath(os.path.join( __addon__.getAddonInfo('profile'),'images') ).decode('utf-8')
if not os.path.exists(THUMB_PATH): os.makedirs(THUMB_PATH)

ACTION_MOVE_LEFT        = 1
ACTION_MOVE_RIGHT       = 2
ACTION_MOVE_UP          = 3
ACTION_MOVE_DOWN        = 4
ACTION_PAGE_UP          = 5
ACTION_PAGE_DOWN        = 6
ACTION_SELECT_ITEM      = 7
ACTION_HIGHLIGHT_ITEM   = 8
ACTION_PARENT_DIR       = 9
ACTION_PREVIOUS_MENU    = 10
ACTION_SHOW_INFO        = 11
ACTION_PAUSE            = 12
ACTION_STOP             = 13
ACTION_NEXT_ITEM        = 14
ACTION_PREV_ITEM        = 15
ACTION_SHOW_GUI         = 18
ACTION_PLAYER_PLAY      = 79
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_CONTEXT_MENU     = 117

import locale
loc = locale.getdefaultlocale()
print loc
ENCODING = loc[1] or 'utf-8'

def ENCODE(string):
	return string.encode(ENCODING,'replace')

def ERROR(message,caption='',dialog=True):
	LOG(message)
	traceback.print_exc()
	err = str(sys.exc_info()[1])
	if dialog: xbmcgui.Dialog().ok(__language__(32520) + caption,err)
	return err


class Main_Menu(xbmcgui.WindowXML):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__( self )
	
	def onInit(self):
		self.lastUpdateFile = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('profile'),'last') ).decode('utf-8')
		self.dataFile = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('profile'),'data') ).decode('utf-8')
		self.loadSettings()
		
		self.shows = []
		self.loadData()
		self.update(force=self.isStale())

		self.setFocus(self.getControl(120))
	
	def isStale(self):
		last = self.fileRead(self.lastUpdateFile)
		if not last: return True
		return (time.time() - (3600 * self.hours) > float(last))
		
	def setLast(self):
		self.fileWrite(self.lastUpdateFile,str(time.time()))
		
	def onClick( self, controlId ):
		pass

	def onFocus( self, controlId ):
		self.controlId = controlId

	def update(self,force=False):
		if force:
			self.updateData()
			self.saveData()
		self.updateDisplay()
		
	def onAction(self,action):
		#print "ACTION: " + str(action.getId()) + " FOCUS: " + str(self.getFocusId()) + " BC: " + str(action.getButtonCode())
		if action == ACTION_CONTEXT_MENU:
			self.doMenu()
		elif action == ACTION_SELECT_ITEM:
			if self.getFocusId() == 8000:
                                w = Main_Menu("script-movies.xml" , __addon__.getAddonInfo('path'), "Default")
                                w.doModal()
                                del w
                        elif self.getFocusId() == 8001:
                                w = Main_Menu("script-tvshows.xml" , __addon__.getAddonInfo('path'), "Default")
                                w.doModal()
                                del w
                        elif self.getFocusId() == 8002:
                                w = Main_Menu("script-livetv.xml" , __addon__.getAddonInfo('path'), "Default")
                                w.doModal()
                                del w
                        elif self.getFocusId() == 8003:
                                w = Main_Menu("script-music.xml" , __addon__.getAddonInfo('path'), "Default")
                                w.doModal()
                                del w
                        elif self.getFocusId() == 8004:
                                w = Main_Menu("script-settings.xml" , __addon__.getAddonInfo('path'), "Default")
                                w.doModal()
                                del w
				
			elif self.getFocusId() == 201:
				self.addFromLibrary()
			elif self.getFocusId() == 202:
				self.openSettings()
			else:
				print "##################################################################"
				
		elif action == ACTION_PARENT_DIR:
			action = ACTION_PREVIOUS_MENU
		elif action == ACTION_MOUSE_LEFT_CLICK:
			if self.getFocusId() == 200:
				print "##################################################################"
		xbmcgui.WindowXMLDialog.onAction(self,action)
			
	def openSettings(self):
		rs = self.reverse_sort
		ao = self.air_offset
		__addon__.openSettings()
		self.loadSettings()
		if rs != self.reverse_sort or ao != self.air_offset: self.updateDisplay()
		
	def doMenu(self):
		dialog = xbmcgui.Dialog()
		#idx = dialog.select(__language__(32011),[__language__(32007),__language__(32026),__language__(32013),__language__(32006)])
		idx = dialog.select(__language__(32011),[__language__(32013),__language__(32054),__language__(32006),__language__(32041)])
		#if idx == 0: self.search()
		#elif idx == 1: self.addFromLibrary()
		if idx == 0: self.reverse()
		elif idx == 1: self.update(force=True)
		elif idx == 2: self.deleteShow()
		
		
	def fileRead(self,fname):
		if not os.path.exists(fname): return ''
		f = open(fname,'r')
		data = f.read()
		f.close()
		return data
	
	def fileReadList(self,fname):
		return self.fileRead(fname).splitlines()
		
	def fileWrite(self,fname,data):
		f = open(fname,'w')
		f.write(data)
		f.close()

	def fileWriteList(self,fname,dataList):
		self.fileWrite(fname,'\n'.join(dataList))




w = Main_Menu("script-main.xml" , __addon__.getAddonInfo('path'), "Default")
w.doModal()
del w
#sys.modules.clear()
