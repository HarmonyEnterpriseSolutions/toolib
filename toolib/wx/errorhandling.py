# -*- coding: Cp1251 -*-
#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/03/20 19:03:25 $"
__version__ = "$Revision: 1.23 $"
# $Source: D:/HOME/cvs/toolib/wx/errorhandling.py,v $
#
#################################################################
from toolib import debug
import codecs
import re
import types
import sys
import traceback
import wx
from controls.WordWrapLabel import WordWrapLabel
from controls.TextCtrl import TextCtrl
from toolib._ import *

ERROR_DIALOG_DETAILS_VISIBLE = debug.isLocation('abrisola', 'kotovsky')

EXC_WRAPPERS = []
try:
	from pywintypes import com_error
except ImportError, e:
	pass
else:
	from toolib.win32.COM_Error import COM_Error
	EXC_WRAPPERS.append((com_error, re.compile('([\w_.]+.\com_error): (\(.+\))$'), COM_Error))

def handleException(parent=None, title=None):
	dlg = ErrorDialog(parent)
	dlg.handleException(sys.exc_info(), title)
	dlg.Destroy()

def hookStderr(parent=None):
	import sys
	sys.stderr = ErrorHandlingStream(sys.stderr, parent)

def exc_instance(e):
	if isinstance(e, tuple):
		if e[1] is None:
			e = e[0]
		else:
			e = e[1]

	for errorClass, regexp, wrapper in EXC_WRAPPERS:
		if isinstance(e, errorClass):
			return wrapper(e)

	return e

def exc_line(e):
	e = exc_instance(e)
	return "%s: %s" % (_(e.__class__.__name__), e)

def exc_traceback(excInfo):
	tblines = traceback.format_exception(*excInfo)[:-1]
	tblines.append(exc_line(excInfo))
	return ''.join(tblines)

##############################################################################
##

HEAD    	= re.compile(re.escape('Traceback (most recent call last):')+'$')
LOCATION	= re.compile('  File "(.+), line (\d+), in (.+)$')
CODE		= re.compile('    (.*)$')

REC_EXC		= re.compile("(?P<className>[\w\.]+): (?P<message>.+)$")

class ErrorHandlingStream(codecs.StreamWriter):


	def __init__(self, stream, parent=None):
		codecs.StreamWriter.__init__(self, stream)
		self._traceback = []
		self._buffer = []
		self._lines = []
		self._parent = parent

		self._state = None

	def write(self, data):
		self.stream.write(data)
		self._buffer.append(data)
		if data.endswith('\n'):
			line = "".join(self._buffer)
			del self._buffer[:]
			self.handleLine(line)

	def isAfter(self, *states):
		return self._state in states

	def setState(self, satte):
		self._state = state

	def match(self, line, *states):
		for state in states:
			if state.match(line):
				self._state = state
				return True
		return False
			

	def handleLine(self, line):
		self._lines.append(line)

		# head is unconditional
		if self.match(line, HEAD):
			return

		# after head is location
		elif self.isAfter(HEAD):
			if self.match(line, LOCATION): 
				return

		# after location is location or code
		elif self.isAfter(LOCATION):
			if self.match(line, LOCATION, CODE): 
				return

		# after code is location
		elif self.isAfter(CODE):
			if self.match(line, LOCATION): 
				return

		self.handleTraceback(self._lines)
		del self._lines[:]
		self._state = None

	def handleTraceback(self, lines):
		if self.isAfter(None):
			lines = filter(lambda line: line.strip() and not line.startswith('* '), lines)
		if lines:
			dlg = ErrorDialog(self._parent)
			try:
				if self.isAfter(None):
					dlg.handleErrorMessage(lines)
				else:
					dlg.handleUnhandledException(lines)
			finally:
				dlg.Destroy()
			

###############################################################

class ErrorDialog(wx.Dialog):
	DETAILS_SHOW = _('Details >>')
	DETAILS_HIDE = _('Details <<')

	def __init__(self, parent=None, tracebackVisible=ERROR_DIALOG_DETAILS_VISIBLE):
		wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

		self.__tracebackVisible = tracebackVisible

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)

		# icon-message box
		box = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(box, 1, wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, 5)

		# icon
		try:
			bmp = wx.ArtProvider_GetBitmap(wx.ART_ERROR, wx.ART_MESSAGE_BOX)
			icon = wx.StaticBitmap(self, -1, bmp)
			box.Add(icon, 0, wx.ALIGN_LEFT | wx.ALL, 10)
		except Exception, e:
			debug.error("Error setting icon")

		# message
		self._messageLabel = WordWrapLabel(self, size=(600, 70))
		box.Add(self._messageLabel, 1, wx.ALL | wx.EXPAND, 10)

		sizer.Add(
			wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL),
			0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5)

		# buttons box
		box = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(box, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

		# ok
		btn = wx.Button(self, wx.ID_OK, _('Ok'))
		btn.SetDefault()
		##btn.SetFocus()
		box.Add(btn, 1, wx.ALL, 5)

		# details
		self._detailsButton = wx.Button(self, wx.NewId(), self.DETAILS_SHOW)
		box.Add(self._detailsButton, 1, wx.ALL, 5)

		self.Bind(wx.EVT_BUTTON, self.OnDetails, self._detailsButton)

		# traceback view
		self._tbCtrl = TextCtrl(self, -1, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH, size=(600, 140))
		self.__fireTracebackVisibleChanged()

		self.SetAutoLayout(True)

	def isTracebackVisible(self):
		return self.__tracebackVisible

	def setTracebackVisible(self, tracebackVisible):
		oldValue = self.__tracebackVisible
		self.__tracebackVisible = tracebackVisible
		if oldValue != tracebackVisible:
			self.__fireTracebackVisibleChanged()

	def OnDetails(self, event):
		self.setTracebackVisible(not self.isTracebackVisible())

	def handleException(self, exceptionInfo=None, title=None):
		exceptionInfo = exceptionInfo or sys.exc_info()
		assert isinstance(exceptionInfo, tuple)

		self.setExceptionInfo(exceptionInfo)

		e = exc_instance(exceptionInfo)
		self.SetTitle(title or _(e.__class__.__name__))

		if title:
			self.setMessage(exc_line(e))
		else:
			self.setMessage(str(e))
		
		self.ShowModal()

	def handleUnhandledException(self, lines):

		m = REC_EXC.match(lines[-1])
		if m:
			eClass, message = m.groups()
		else:
			eClass, message = "str", lines[-1]

		for errorClass, regexp, wrapper in EXC_WRAPPERS:
			m = regexp.match(lines[-1])
			if m:
				eClass, message = m.groups()
				message = str(wrapper(eval(message)))
				lines[-1] = '%s: %s' % (eClass, message)	# fix traceback

		self.SetTitle(_('Unhandled exception: %s') % _(eClass[eClass.rfind('.')+1:]))
		self.setMessage(message)
		self.setTracebackLines(lines)
		self.ShowModal()

	def handleErrorMessage(self, lines):
		self.SetTitle(_("Error message"))
		self.setMessage(''.join(lines))
		self.setTracebackLines(lines)
		self.setTracebackVisible(False)
		self.ShowModal()
		
	def setExceptionInfo(self, excInfo):
		tblines = traceback.format_exception(*excInfo)
		tblines[-1] = exc_line(exc_instance(excInfo))	# better last line
		tblines = map(lambda s: s+'\n', ''.join(tblines).rstrip('\n').split('\n'))
		self.setTracebackLines(tblines)

	def pack(self):
		self.GetSizer().Fit(self)
		self.Center()

	def setMessage(self, message):
		self._messageLabel.setText(message)

	def setTracebackLines(self, lines):
		dlgfont = self.GetFont()
		if not hasattr(self, "_tbfont"):
			self._tbfont = wx.Font(dlgfont.GetPointSize(), wx.MODERN, wx.NORMAL, wx.NORMAL, encoding = wx.FONTENCODING_CP1251)

		taRed	 = wx.TextAttr(wx.RED,   wx.NullColour, self._tbfont)
		taBlue   = wx.TextAttr(wx.BLUE,  wx.NullColour, self._tbfont)
		taNormal = wx.TextAttr(wx.BLACK, wx.NullColour, self._tbfont)

		self._tbCtrl.SetValue('')

		for line in lines:
			if line.startswith('    '):
				self._tbCtrl.SetDefaultStyle(taRed)
			elif line.startswith('  '):
				self._tbCtrl.SetDefaultStyle(taBlue)
			else:
				self._tbCtrl.SetDefaultStyle(taNormal)
			self._tbCtrl.WriteText(line)#.rstrip('\n') + '\n')
		
		self.pack()

		self._tbCtrl.ScrollLines(max(0, self._tbCtrl.GetNumberOfLines() - self._tbCtrl.getHeightInLines() + 1))


	def __fireTracebackVisibleChanged(self):
		# toggle traceback
		sizer = self.GetSizer()
		tbshown = self._tbCtrl.IsShown()
		if self.__tracebackVisible:
			#if not tbshown:
			sizer.Add(self._tbCtrl, 2, wx.EXPAND | wx.ALIGN_BOTTOM |wx.ALL, 5)
			self._tbCtrl.Show()
			self._detailsButton.SetLabel(self.DETAILS_HIDE)
		else:
			#if tbshown:
			self._tbCtrl.Hide()
			sizer.Remove(self._tbCtrl)
			self._detailsButton.SetLabel(self.DETAILS_SHOW)
		self.pack()


if __name__ == '__main__':
	import toolib.startup
	toolib.startup.hookStd()
	hookStderr()

	class TestApp(wx.PySimpleApp):
		def recursion(self, i):
			if i == 5:
				#import SamakiMasaki
				import syntax
			self.recursion(i+1)

		def xlerror(self):
			import toolib.win32.excel as excel
			book = excel.ExcelBook('bebe')

		def strError(self):
			raise "Error"


		def writeExc(self, text):
			for line in text.split('\n'):
				print >> sys.stderr, line

		def tb(self):
			self.writeExc(r"""Traceback (most recent call last):
  File "./py\toolib\wx\tree\Tree.py", line 152, in OnMouse
  File "./py\toolib\wx\tree\Tree.py", line 163, in popup
  File "./py\xlbookmarks\ExcelBookmarkView.py", line 115, in setMMMenuContext
  File "E:\Pro\PYTHON23\lib\site-packages\win32com\client\dynamic.py", line 471, in __getattr__
    raise pythoncom.com_error, details
pywintypes.com_error: (-2147418111, '\xc2\xfb\xe7\xee\xe2 \xe1\xfb\xeb \xee\xf2\xea\xeb\xee\xed\xe5\xed.', None, None)""")
			

		def OnInit(self):
			#sys.stderr.write("Warning\n")
			#self.xlerror()
			#self.tb()
			#self.recursion(0)

			try:
				#self.xlerror()
				#self.tb()
				self.recursion(0)
				pass
			except:
				handleException()
			return True

	TestApp().MainLoop()
