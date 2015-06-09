# -*- coding: Cp1251 -*-
###############################################################################
#
'''
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/04/13 17:35:52 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/wx/dialogs/OkCancelDialog.py,v $
###############################################################################
from toolib._ import *
import wx
from ButtonBottomedDialog import ButtonBottomedDialog

class OkCancelDialog(ButtonBottomedDialog):

	ID_OK	  = wx.NewId()
	ID_CANCEL = wx.NewId()

	def addButtons(self, sizer):
		ButtonBottomedDialog.addButtons(self, sizer)
		
		ok = self.addButton(wx.Button(self, self.ID_OK, _("Ok")), 'ok')
		#ok.SetHelpText(_('Push to confirm changes'))
		ok.SetDefault()
		
		cancel = self.addButton(wx.Button(self, self.ID_CANCEL, _("Cancel")), 'cancel')
		#cancel.SetHelpText(_("Push to cancel changes. E.g. you have changed nothing."))
		
	def OnOk(self, event):
		self.EndModal(wx.ID_OK)

	def OnCancel(self, event):
		self.EndModal(self.ID_CANCEL)

	def getOkButton(self):
		return self.FindWindowById(self.ID_OK)

	def getCancelButton(self):
		return self.FindWindowById(self.ID_CANCEL)
