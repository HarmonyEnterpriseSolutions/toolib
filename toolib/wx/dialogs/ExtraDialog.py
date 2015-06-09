# -*- coding: Cp1251 -*-
###############################################################################
#
'''
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/03/16 17:54:53 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/wx/dialogs/ExtraDialog.py,v $
###############################################################################
import wx
from toolib.util.lang import normalize_args

# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
wx.HelpProvider_Set(wx.SimpleHelpProvider())

class ExtraDialog(wx.Dialog):
	DEFAULT_EXTRA_STYLE = 0 #wx.DIALOG_EX_CONTEXTHELP

	def __init__(self, *p, **pp):
		"""
		Same as wx.Dialog but have one extra named arg:
			extraStyle
		"""
		extraStyle = pp.pop('extraStyle', self.DEFAULT_EXTRA_STYLE)

		# Instead of calling wx.Dialog.__init__ we precreate the dialog
		# so we can set an extra style that must be set before
		# creation, and then we create the GUI dialog using the Create
		# method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(extraStyle)
		pre.Create(*p, **pp)

		# This next step is the most important, it turns this Python
		# object into the real wrapper of the dialog (instead of pre)
		# as far as the wx.Python extension is concerned.
		self.this = pre.this
		# Now continue with the normal construction of the dialog
		# contents

	def pack(self):
		self.GetSizer().Fit(self)
