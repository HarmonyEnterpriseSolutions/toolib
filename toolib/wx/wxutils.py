# -*- coding: Cp1251 -*-
#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/11/04 14:33:17 $"
__version__ = "$Revision: 1.7 $"
# $Source: D:/HOME/cvs/toolib/wx/wxutils.py,v $
#
#################################################################

from toolib._ import *

import wx
import types

def messageBox(parent, text, caption, flags):
	dlg = wx.MessageDialog(parent, text, caption, flags)
	res = dlg.ShowModal()
	dlg.Destroy()
	return res

def showComErrorMessage(parent, e):
	caption = "%s" % ( e[1] )
	if type(e[2]) in (types.ListType, types.TupleType):
		message = e[2][2]
	else:
		message = e[1]
	text = "%s\n\nКод ошибки: 0x%08X" % (message, e[0])
	return messageBox(parent, text, caption, wx.OK | wx.ICON_ERROR)

def getCore(wnd):
	while wnd is not None:
		wnd = wnd.GetParent()
		if hasattr(wnd, 'getCore'):
			return wnd.getCore()
		#elif hasattr(wnd, 'core'):
		#	return wnd.core()
	raise AttributeError, "core() not found among parent windows"


class ProgressCanceledException(Exception):
	pass

class ProgressDialog(wx.ProgressDialog):
	def __init__(self, title, message, maximum=100, parent=None, style = wx.PD_APP_MODAL):
		wx.ProgressDialog.__init__(self, title, message, maximum, parent, style)
		self.__max = maximum
		self.__message = None   # last message
		self.__count = 0		# last count

	def update(self, count, message):
		if count >= self.__max:
			count = self.__max - 1
		##print "update", count, message
		if message is None: # @Oleg do not now what's default message...
			proceed = self.Update(count)
		else:
			proceed = self.Update(count, message)
		if not proceed:
			raise ProgressCanceledException(self.__message, self.__count)
		else:
			if message is not None:
				self.__message = message
			if count != -1:
				self.__count = count

	def increment(self, message=None):
		self.update(self.__count+1, message)

	def setMessage(self, message):
		self.update(-1, message)

	def destroy(self):
		""" Calls Hide and then Destroy """
		self.Hide()
		self.Destroy()


def findFileDialog(path, parent=None, title=None, extensions=None):
	import os
	import toolib.utils as utils

	rc = messageBox(parent, _("File not found: %s\n"
							  "Would You like to find it manually?") % (path,), title or _("File is missing"), wx.YES_NO | wx.ICON_QUESTION)

	if rc == wx.ID_YES:
		dlg = wx.FileDialog(
			parent,
			_("Find the file"),
			utils.existentPath(path),
			"",
			extensions or (_("All files") + " (*.*)|*.*"),
			wx.OPEN)
		try:
			if dlg.ShowModal() == wx.ID_OK:
				return dlg.GetPath()
		finally:
			dlg.Destroy()


class MessageBoxParentMixIn:

	def messageBox(self, text, caption=None, flags=0):
		if caption is None:
			caption = self.GetTitle() or _("Message")
		return messageBox(self, text, caption, flags)
