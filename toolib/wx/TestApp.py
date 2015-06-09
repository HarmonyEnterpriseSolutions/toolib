#################################################################
# Program: pyras
"""
	
"""
__author__  = "Oleg Noga"
__date__    = "$Date: 2014/08/13 16:51:25 $"
__version__ = "$Revision: 1.5 $"
# $Source: C:/HOME/cvs/toolib/wx/TestApp.py,v $
#
#################################################################

IMAGE_PATH	= r"Z:\projects\lider\res\images"

import wx
from toolib.wx.Resources import Resources
from toolib.wx.menu.MenuResources import MenuResources

def static():
	import toolib.startup
	toolib.startup.hookStd()
	toolib.startup.setDefaultEncoding()
	_static_init = True
			
	import locale
	locale.setlocale(locale.LC_ALL, "")

	
class MainFrame(wx.Frame):
	def __init__(self, *p, **pp):
		self._oninit		= pp.pop('oninit')
		self._ondestroy	= pp.pop('ondestroy')
		self._ontimer	= pp.pop('ontimer')
		wx.Frame.__init__(self, *p, **pp)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self._menuResources=None
		self._resources=None

		self.actions = None

		self._oninit(self)

		self.__timer = wx.Timer(self, -1)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.__timer.Start(1000)



	def OnTimer(self, event):
		self._ontimer(self)
		
	def OnClose(self, event):
		self._ondestroy(self)
		self.Destroy()

	def getResources(self):
		if self._resources is None:
			self._resources = Resources(IMAGE_PATH)
		return self._resources

	def getMenuResources(self):
		if self._menuResources is None:
			#from lider.config.MainFrame import ACTIONS as actions
			self._menuResources = MenuResources(self.getResources(), self.actions or {})
		return self._menuResources


class TestApp(wx.PySimpleApp):

	def __init__(self, oninit=lambda frame: None, ondestroy=lambda frame: None, frameClass=MainFrame, ontimer=lambda frame: None):
		self._oninit = oninit
		self._ondestroy	= ondestroy
		self._ontimer = ontimer
		self._frameClass= frameClass
		wx.PySimpleApp.__init__(self)

	def OnInit(self):
		try:
			static()
			del static
		except NameError:
			pass

		f = self._frameClass(None, wx.NewId(), "Test frame", oninit=self._oninit, ondestroy=self._ondestroy, ontimer=self._ontimer)
		f.Size = 800, 600
		f.Show()
		return True


		

if __name__ == '__main__':

	def oninit(self):
		pass
		
	def ondestroy(self):
		pass

	def ontimer(self):
		print "t",

	from TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
