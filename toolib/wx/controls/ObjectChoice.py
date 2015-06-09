#################################################################
# Package: toolib.wx.controls
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/10/24 18:06:01 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/controls/ObjectChoice.py,v $
#
#################################################################

import wx
from ControlWithObjectsMixIn import ControlWithObjectsMixIn

class ObjectChoice(ControlWithObjectsMixIn, wx.Choice):
	def __init__(self, *args, **kwargs):
		choices = kwargs.pop('choices', None)
		strfunc = kwargs.pop('strfunc', None)
		ControlWithObjectsMixIn.__init__(self, choices, strfunc)
		kwargs['choices']=self._mapObjects(choices)
		wx.Choice.__init__(self, *args, **kwargs)

	def Set(self, choices):
		self._setObjects(choices)
		for string in self._mapObjects(choices):
			self.Append(string)

	def GetValue(self):
		return self.getSelectedObject()
		

if __name__ == '__main__':
	import toolib.startup
	toolib.startup.hookStd()

	class O:
		def __init__(self, s):
			self.s = s

		def __str__(self):
			return self.s

	def cstr(o):
		return "10.01.2004: Tr %s, 2000$" % o

	class TestApp(wx.PySimpleApp):
		def OnInit(self):
			frame = wx.Dialog(None)
			o1 = O("1")
			clb = ObjectChoice(frame, None, cstr)

			cs = [o1, O("2"), O("3"), O("4")]*10

			clb.Set(cs)

			frame.ShowModal()
			print clb.GetValue()

			return False

	TestApp().MainLoop()
