#################################################################
# Package: toolib.wx.controls
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/04/27 19:39:38 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/controls/ObjectCheckListBox.py,v $
#
#################################################################

import wx
from toolib._ import *
from ControlWithObjectsMixIn import ControlWithObjectsMixIn
from toolib.util import lang


class ObjectCheckListBox(ControlWithObjectsMixIn, wx.CheckListBox):
	def __init__(self, *args, **kwargs):
		args, kwargs = lang.normalize_args(args, kwargs, 
			('parent', 'id', 'pos', 'size', 'choices', 'style', 'validator', 'name')
		)

		choices = kwargs.get('choices')
		strfunc = kwargs.pop('strfunc', None)
		
		ControlWithObjectsMixIn.__init__(self, choices, strfunc)

		kwargs['choices'] = self._mapObjects(choices or ())

		wx.CheckListBox.__init__(self, *args, **kwargs)

	def Set(self, choices):
		self._setObjects(choices)
		wx.CheckListBox.Set(self, self._mapObjects(choices))

	def iterCheckedObjects(self):
		for i, choice in enumerate(self):
			if self.IsChecked(i):
				yield choice

	def getCheckedObjects(self):
		return tuple(self.iterCheckedObjects())

	def checkObject(self, object, checked=True):
		self.Check(self.getIndex(object), checked)

	def checkObjectAt(self, index, checked=True):
		self.Check(index, checked)

	def checkAll(self, checked=True):
		for i in xrange(self.GetCount()):
			self.Check(i, checked)

	def isObjectChecked(self, object):
		return self.isChecked(self.getIndex(object), checked)

	def GetValue(self):
		return self.getCheckedObjects()
		

class ObjectCheckListBoxWithButons(wx.BoxSizer):

	INDENT = 5

	def __init__(self, parent, *args, **kwargs):
		wx.BoxSizer.__init__(self, wx.VERTICAL)

		#print args, kwargs

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		b = wx.Button(parent, -1, _("Check all"))
		hsizer.Add(b, 1, wx.RIGHT, self.INDENT)
		b.Bind(wx.EVT_BUTTON, lambda event: self._listBox.checkAll(True))

		b = wx.Button(parent, -1, _("Uncheck all"))
		hsizer.Add(b, 1)
		b.Bind(wx.EVT_BUTTON, lambda event: self._listBox.checkAll(False))
		self.Add(hsizer, 0, wx.BOTTOM, self.INDENT)

		self._listBox = ObjectCheckListBox(parent, *args, **kwargs)
		self.Add(self._listBox, 1, wx.EXPAND)

		if parent.GetSizer() is None:
			parent.SetSizer(self)

	def __getattr__(self, name):
		return getattr(self._listBox, name)


if __name__ == '__main__':
	import toolib.startup
	toolib.startup.hookStd()

	class O:
		def __init__(self, s):
			self.s = s

		def __str__(self):
			return self.s

	def cstr(o):
		return "10.01.2004: Transaction %s, 2000$" % o

	class TestApp(wx.PySimpleApp):
		def OnInit(self):
			frame = wx.Dialog(None)
			o1 = O("1")
			clb = ObjectCheckListBoxWithButons(frame, choices=None, strfunc=cstr)

			cs = [o1, O("2"), O("3"), O("4")]*10

			clb.Set(cs)

			clb.checkObject(o1)

			frame.ShowModal()
			print clb.getCheckedObjects()

			return False

	TestApp().MainLoop()
