# -*- coding: Cp1251 -*-
###############################################################################
#
'''
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/02/20 20:09:53 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/dialogs/ButtonBottomedDialog.py,v $
###############################################################################
from toolib._ import *
import wx
from ExtraDialog import ExtraDialog
from toolib import debug

class ButtonBottomedDialog(ExtraDialog):

	INDENT = 5

	def __init__(self, *args, **kwargs):
		ExtraDialog.__init__(self, *args, **kwargs)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.createContentSizer(), 1, wx.ALL | wx.GROW, self.INDENT)
		sizer.Add(wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL), 0, wx.GROW|wx.ALIGN_CENTER|wx.TOP, 5)
		self._buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self._buttonSizer, 0, wx.ALIGN_CENTER|wx.ALL, self.INDENT)
		self.addButtons(self._buttonSizer)
		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		self.pack()

	def createContentSizer(self):
		raise NotImplementedError, 'abstract'

	def getContentSizer(self):
		return self.createContentSizer()

	def addButton(self, button, key=None):
		self._buttonSizer.Add(button, 0, wx.ALIGN_CENTRE|wx.ALL, self.INDENT)
		if key:
			try:
				method = "On%s%s" % (key[0].upper(), key[1:])
				self.Bind(wx.EVT_BUTTON, getattr(self, method), button)
			except AttributeError:
				debug.warning("%s has no handler: %s" % (self.__class__, method))
		return button
		
	def addButtons(self, sizer):
		if wx.Platform != "__WXMSW__":
			self.AddButton(wx.ContextHelpButton(self))
