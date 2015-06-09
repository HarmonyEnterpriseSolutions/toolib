import wx
import types
from TWindowProperty	import TWindowProperty
from toolib._			import *

###################################################################
# Trait
#
class TWindowUtils(TWindowProperty):
	"""
	Requires:
		GetParent
		GetTitle		# in messageBox it caption not defined

	Provides:
		getParentWindowProperty
		messageBox
		getTopLevelParent
	"""

	def messageBox(self, text, caption=None, flags=0):
		return messageBox(self, text, caption, flags)

	def getTopLevelParent(self):
		return getTopLevelParent(self)

	def iterWindowsRecursive(self, filterFn=lambda window: True):
		return iterWindowsRecursive(self, filterFn)

#################################################################
# Static
#

def messageBox(self, text, caption=None, flags=0):
	dlg = wx.MessageDialog(self, text, caption or self.GetTitle() or _("Message"), flags)
	try:
		return dlg.ShowModal()
	finally:
		dlg.Destroy()

def getTopLevelParent(self):
	parent = self.GetParent()
	while not isinstance(parent, (wx.TopLevelWindow, types.NoneType)):
		parent = parent.GetParent()
	return parent

def iterWindowsRecursive(window, filterFn=lambda window: True):
	if filterFn(window):
		yield window
	for i in window.GetChildren():
		for j in iterWindowsRecursive(i, filterFn):
			yield j

	
