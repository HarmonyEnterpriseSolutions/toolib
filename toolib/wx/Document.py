#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/12/02 15:01:58 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/Document.py,v $
#
#################################################################
import wx
import os
import toolib.wx.wxutils as wxutils
from toolib._ import *

class Document: 

	def __init__(self):
		self.m_documentModified = False
		self.m_documentViews = []
		self.m_documentFile = ""
		self.__lastPath = ""

	def getFileExtensions(self):
		return _("All files") + " (*.*)|*.*"

	def OnNewDocument(self):
		self.OnSaveModified()
		self.DeleteContents()
		self.m_documentFile = ""
		self.UpdateAllViews()
		
	def __errorMessage(self, message):
		wxutils.messageBox(self.GetDocumentWindow(), message, self.GetClassTitle(), wx.ICON_HAND)

	def OnOpenDocument(self, fileName):
		try:
			f = file(fileName, 'rb')
			try:
				if not self.LoadObject(f):
					raise IOError, "LoadObject returned FALSE"
			finally:
				f.close()
		except:
			self.__errorMessage(_("Can't open document: ") + fileName)
		else:
			self.m_documentFile = fileName
			self.m_documentModified = False
			self.UpdateAllViews()

	def OnSaveDocument(self, fileName):
		try:
			f = file(fileName, 'wb')
			try:
				saved = self.SaveObject(f)
			finally:
				f.close()
			if not saved:
				try:
					os.remove(fileName)
				except Exception, e:
					error("Failed to remove %s: %s" % (fileName, e))
				raise IOError, "SaveObject returned FALSE"
		except:
			##raise
			self.__errorMessage(_("Error saving document: ") + fileName)
			return False
		else:
			self.m_documentFile = fileName			# set file name for this document
			self.m_documentModified = False
			self.UpdateAllViews()
			return True

	def GetClassTitle(self):
		"""
		Title of document class:
		e.g. "Word Document"
		"""
		return _("Document")

	def OnSaveModified(self, canCancel=True):
		if self.IsModified():
			##print "parent wnd:", self.GetDocumentWindow()

			style = wx.YES_NO | wx.ICON_QUESTION
			if canCancel: 
				style |= wx.CANCEL

			rc = wxutils.messageBox(
				self.GetDocumentWindow(),
				_("%s was modified. Save changes?") % self.GetClassTitle(),
				self.GetClassTitle(),
				style)

			if rc == wx.ID_YES:
				self.Save()
			elif rc == wx.ID_NO:
				self.m_documentModified = False
			else:
				return False		# return false only if user have pressed CANCEL
		return True

	def GetViews(self):
		return self.m_documentViews

	def GetFirstView(self):
		if len(self.m_documentViews) > 0:
			return self.m_documentViews[0]

	def AddView(self, view):
		self.m_documentViews.append(view)
		view.SetDocument(self)

	def GetDocumentWindow(self):
		return self.GetFirstView()
			
	def IsModified(self):
		return self.m_documentModified

	def SetModified(self, modified):
		self.m_documentModified = modified

	def Modify(self):
		self.m_documentModified = True

	def UpdateAllViews(self, sender=None, hint=None):
		for view in self.m_documentViews:
			if view != sender:
				view.Update()

	def GetFileName(self):
		return self.m_documentFile

	def SetFileName(self, fileName):
		self.m_documentFile = fileName

	def GetTitle(self):
		file = self.GetFileName()
		if file:
			return os.path.split(file)[1]
		else:
			return ""

	def OnCreate(self):
		return True

	def Save(self):
		if self.GetFileName():
			self.Save()
		else:
			self.SaveAs()

	def getLastPath(self):
		return self.__lastPath

	def setLastPath(self, lastPath):
		self.__lastPath = lastPath

	def SaveAs(self):
		dlg = wx.FileDialog(
			self.GetDocumentWindow(),
			_("Save file"),
			self.getLastPath(),
			self.m_documentFile or _("ExcelBookmarksDoc1"),
			self.getFileExtensions(),
			wx.SAVE | wx.OVERWRITE_PROMPT
		)
		try:
			if dlg.ShowModal() == wx.ID_OK:
				fileName = dlg.GetPath()
				self.OnSaveDocument(fileName)
				self.setLastPath(os.path.split(fileName)[0])
		finally:	
			dlg.Destroy()
		
	def Save(self):
		if self.IsModified():
			if self.m_documentFile:
				self.OnSaveDocument(self.m_documentFile)
			else:
				self.SaveAs()

	def Open(self):
		""" @Oleg: Why thereis no function like this in wx.Document ??? """

		dlg = wx.FileDialog(self.GetDocumentWindow(),
			_("Open file"),
			self.getLastPath(),
			"",
			self.getFileExtensions(),
			wx.OPEN)

		try:
			if dlg.ShowModal() == wx.ID_OK:
				fileName = dlg.GetPath()
				self.OnOpenDocument(fileName)
				self.setLastPath(os.path.split(fileName)[0])
		finally:	
			dlg.Destroy()
