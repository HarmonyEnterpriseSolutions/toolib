import wx
import types
from toolib 		           import debug
from toolib.math.Rect          import Rect
from toolib.event.ListenerList import ListenerList
from toolib.wx.mixin.TWindowUtils import TWindowUtils
import operator

BITMAP_BUTTON_EXTRA_INDENT = 4

##############################################################################
# TextCtrlWithButtons
# 
__super__ = wx.PyControl
class TextCtrlWithButtons(__super__):

	class EventWrapper(object):
		"""
		Used to manually
		wrap event from textControl and override method
		GetEventObject to return TextCtrlWithButtons instance instead
		TextControl
		"""
		def __init__(self, event):
			self._event = event

		def __getattr__(self, name):
			return getattr(self._event, name)

		def GetEventObject(self):
			return self._event.GetEventObject().GetParent()


	def __init__(self, 
		parent,
		id         = -1,
		pos        = wx.DefaultPosition,
		size       = wx.DefaultSize,
		style      = 0,
		validator  = wx.DefaultValidator,
		name       = wx.ControlNameStr,
	):
		__super__.__init__(self, parent, id, pos, size, wx.WANTS_CHARS, validator, name)
		
		self.__textControl = self.CreateTextControl(-1, style | wx.NO_BORDER)

		self._buttons = []		# buttons from right to left

		#self.__onSize(None)
		self.Bind(wx.EVT_SIZE, self.__onSize)

		# embedded text control should get focus when control gets
		self.Bind(wx.EVT_SET_FOCUS, self.__onFocus)

		super(TextCtrlWithButtons, self).SetBackgroundColour(wx.RED)#self.__textControl.GetBackgroundColour())


	def addTextButton(self, text, handler=None):
		button = wx.Button(self, -1, text, style=wx.NO_BORDER)
		self.addButton(button, handler)
		button.SetMinSize(wx.Size(16, -1))

	def addBitmapButton(self, bitmap, handler=None):
		button = wx.BitmapButton(self, -1, bitmap, style=wx.NO_BORDER|wx.BU_AUTODRAW)
		self.addButton(button, handler)
		button.SetMinSize((bitmap.GetWidth()+BITMAP_BUTTON_EXTRA_INDENT, bitmap.GetHeight()+BITMAP_BUTTON_EXTRA_INDENT))

	def addButton(self, button, handler=None):
		"""
		Button MinSize is valuable for layout
		"""
		self._buttons.append(button)
		
		if handler:
			button.Bind(wx.EVT_BUTTON, handler)

		return button


	def GetTextControl(self):
		return self.__textControl


	def Enable(self, flag=True):
		wx.PyControl.Enable(self, flag)
		for child in self.GetChildren():
			child.Enable(flag)

	##########################################################################
	# Overrideables
	#
	def CreateTextControl(self, id, style):
		"""
		Override to set another control as text
		Control must have GetValue, SetValue
		"""
		return wx.TextCtrl(self, id, '', style=style)
		
	##########################################################################
	# Event handlers
	#
	def __onFocus(self, evt):
		"""embedded text control should get focus when control gets"""
		self.__textControl.SetFocus()
		self.__textControl.SetSelection(-1,-1)
		evt.Skip()

	def DoGetBestSize(self):
		h = self.__textControl.BestSize.GetHeight()
		borderHeight = self.Size.GetHeight() - self.ClientSize.GetHeight()
		return wx.Size(
			super(TextCtrlWithButtons, self).DoGetBestSize().GetWidth(), 
			max(h, borderHeight + max([b.MinSize.GetHeight() for b in self._buttons]+[0]))
		)

	def GetMinSize(self):
		"""
		my grid ask this to adjust row height
		"""
		return wx.Size(self.MinSize.GetWidth(), self.BestSize.GetHeight())

	def __onSize(self,evt):
		w, h = self.ClientSize
		x = w - reduce(operator.add, (b.MinSize.GetWidth() for b in self._buttons), 0)

		textCtrlHeight = self.__textControl.BestSize.GetHeight() - 2 # -2 because text control has no border but reports same size as with border

		#rint "h=", h, "textCtrlHeight=", textCtrlHeight, h-textCtrlHeight/2

		dw = 1
		dh = max(0, (h - textCtrlHeight) / 2) + 1

		self.__textControl.SetDimensions(dw, dh, x-dw*2, h-dh*2)	# text control has no border, place text cursor better
		#rint self.__textControl.GetSize(), self.__textControl.GetBestSize()
		for b in self._buttons:
			b.SetDimensions(x, 0, b.MinSize.GetWidth(), h)
			#rint b.MinSize.GetWidth(), h, b.GetSize()
			x += b.MinSize.GetWidth()

	def beginEventHandlerRedirect(self):
		"""
		Problem is that 
			I have to push event handler to text control instead container
			I cat't hook wx.PyGridCellEditor.Destroy method to pop this handler
				So i must to push it to control
		Workaround is to temporary pop move event handler to textControl
		"""
		handler = __super__.PopEventHandler(self, False)
		assert debug.trace("PyControl->TextControl: %s" % id(handler))
		self.__textControl.PushEventHandler(handler)

	def endEventHandlerRedirect(self):
		handler = self.__textControl.PopEventHandler(False)
		assert debug.trace("PyControl->TextControl: %s" % id(handler))
		__super__.PushEventHandler(self, handler)

	#######################################################################
	# Window delegation
	#

	# because all events are going thrue _textControl
	# we must disable/enable event there instead of PyControl
	def GetEvtHandlerEnabled(self, *args, **kwargs):
		return self.__textControl.GetEvtHandlerEnabled(*args, **kwargs)

	def SetEvtHandlerEnabled(self, *args, **kwargs):
		return self.__textControl.SetEvtHandlerEnabled(*args, **kwargs)

	def SetWindowStyle(self, style):
		self.__textControl.SetWindowStyle(style)
	
	def GetWindowStyle(self):
		return self.__textControl.GetWindowStyle()

	def SetBackgroundColour(self, colour):
		super(TextCtrlWithButtons, self).SetBackgroundColour(colour)
		self.__textControl.SetBackgroundColour(colour)

	#######################################################################
	# direct delegation of wx.TextCtrl methods to text control
	# This needed to make it working as text control in wx.grid
	# __getattr__ is not suitable because wx.grid checks for methods presence
	#

	def AppendText(self, *args, **kwargs):
		return self.__textControl.AppendText(*args, **kwargs)

	def CanCopy(self, *args, **kwargs):
		return self.__textControl.CanCopy(*args, **kwargs)

	def CanCut(self, *args, **kwargs):
		return self.__textControl.CanCut(*args, **kwargs)

	def CanPaste(self, *args, **kwargs):
		return self.__textControl.CanPaste(*args, **kwargs)

	def CanRedo(self, *args, **kwargs):
		return self.__textControl.CanRedo(*args, **kwargs)

	def CanUndo(self, *args, **kwargs):
		return self.__textControl.CanUndo(*args, **kwargs)

	def ChangeValue(self, *args, **kwargs):
		return self.__textControl.ChangeValue(*args, **kwargs)

	def Clear(self, *args, **kwargs):
		return self.__textControl.Clear(*args, **kwargs)

	def Copy(self, *args, **kwargs):
		return self.__textControl.Copy(*args, **kwargs)

	#def Create(self, *args, **kwargs):
	#	return self.__textControl.Create(*args, **kwargs)

	def Cut(self, *args, **kwargs):
		return self.__textControl.Cut(*args, **kwargs)

	def DiscardEdits(self, *args, **kwargs):
		return self.__textControl.DiscardEdits(*args, **kwargs)

	def EmulateKeyPress(self, *args, **kwargs):
		return self.__textControl.EmulateKeyPress(*args, **kwargs)

	def GetDefaultStyle(self, *args, **kwargs):
		return self.__textControl.GetDefaultStyle(*args, **kwargs)

	def GetInsertionPoint(self, *args, **kwargs):
		return self.__textControl.GetInsertionPoint(*args, **kwargs)

	def GetLastPosition(self, *args, **kwargs):
		return self.__textControl.GetLastPosition(*args, **kwargs)

	def GetLineLength(self, *args, **kwargs):
		return self.__textControl.GetLineLength(*args, **kwargs)

	def GetLineText(self, *args, **kwargs):
		return self.__textControl.GetLineText(*args, **kwargs)

	def GetNumberOfLines(self, *args, **kwargs):
		return self.__textControl.GetNumberOfLines(*args, **kwargs)

	def GetRange(self, *args, **kwargs):
		return self.__textControl.GetRange(*args, **kwargs)

	def GetSelection(self, *args, **kwargs):
		return self.__textControl.GetSelection(*args, **kwargs)

	def GetString(self, *args, **kwargs):
		return self.__textControl.GetString(*args, **kwargs)

	def GetStringSelection(self, *args, **kwargs):
		return self.__textControl.GetStringSelection(*args, **kwargs)

	def GetStyle(self, *args, **kwargs):
		return self.__textControl.GetStyle(*args, **kwargs)

	def GetValue(self, *args, **kwargs):
		return self.__textControl.GetValue(*args, **kwargs)

	def HideNativeCaret(self, *args, **kwargs):
		return self.__textControl.HideNativeCaret(*args, **kwargs)

	def HitTest(self, *args, **kwargs):
		return self.__textControl.HitTest(*args, **kwargs)

	def HitTestPos(self, *args, **kwargs):
		return self.__textControl.HitTestPos(*args, **kwargs)

	def IsEditable(self, *args, **kwargs):
		return self.__textControl.IsEditable(*args, **kwargs)

	def IsEmpty(self, *args, **kwargs):
		return self.__textControl.IsEmpty(*args, **kwargs)

	def IsModified(self, *args, **kwargs):
		return self.__textControl.IsModified(*args, **kwargs)

	def IsMultiLine(self, *args, **kwargs):
		return self.__textControl.IsMultiLine(*args, **kwargs)

	def IsSingleLine(self, *args, **kwargs):
		return self.__textControl.IsSingleLine(*args, **kwargs)

	def LoadFile(self, *args, **kwargs):
		return self.__textControl.LoadFile(*args, **kwargs)

	def MacCheckSpelling(self, *args, **kwargs):
		return self.__textControl.MacCheckSpelling(*args, **kwargs)

	def MarkDirty(self, *args, **kwargs):
		return self.__textControl.MarkDirty(*args, **kwargs)

	def Paste(self, *args, **kwargs):
		return self.__textControl.Paste(*args, **kwargs)

	def PositionToXY(self, *args, **kwargs):
		return self.__textControl.PositionToXY(*args, **kwargs)

	def Redo(self, *args, **kwargs):
		return self.__textControl.Redo(*args, **kwargs)

	def Remove(self, *args, **kwargs):
		return self.__textControl.Remove(*args, **kwargs)

	def Replace(self, *args, **kwargs):
		return self.__textControl.Replace(*args, **kwargs)

	def SaveFile(self, *args, **kwargs):
		return self.__textControl.SaveFile(*args, **kwargs)

	def SelectAll(self, *args, **kwargs):
		return self.__textControl.SelectAll(*args, **kwargs)

	def SendTextUpdatedEvent(self, *args, **kwargs):
		return self.__textControl.SendTextUpdatedEvent(*args, **kwargs)

	def SetDefaultStyle(self, *args, **kwargs):
		return self.__textControl.SetDefaultStyle(*args, **kwargs)

	def SetEditable(self, *args, **kwargs):
		return self.__textControl.SetEditable(*args, **kwargs)

	def SetInsertionPoint(self, *args, **kwargs):
		return self.__textControl.SetInsertionPoint(*args, **kwargs)

	def SetInsertionPointEnd(self, *args, **kwargs):
		return self.__textControl.SetInsertionPointEnd(*args, **kwargs)

	def SetMaxLength(self, *args, **kwargs):
		return self.__textControl.SetMaxLength(*args, **kwargs)

	def SetModified(self, *args, **kwargs):
		return self.__textControl.SetModified(*args, **kwargs)

	def SetSelection(self, *args, **kwargs):
		return self.__textControl.SetSelection(*args, **kwargs)

	def SetStyle(self, *args, **kwargs):
		return self.__textControl.SetStyle(*args, **kwargs)

	def SetValue(self, *args, **kwargs):
		return self.__textControl.SetValue(*args, **kwargs)

	def ShowNativeCaret(self, *args, **kwargs):
		return self.__textControl.ShowNativeCaret(*args, **kwargs)

	def ShowPosition(self, *args, **kwargs):
		return self.__textControl.ShowPosition(*args, **kwargs)

	def Undo(self, *args, **kwargs):
		return self.__textControl.Undo(*args, **kwargs)

	def WriteText(self, *args, **kwargs):
		return self.__textControl.WriteText(*args, **kwargs)

	def XYToPosition(self, *args, **kwargs):
		return self.__textControl.XYToPosition(*args, **kwargs)

	def write(self, *args, **kwargs):
		return self.__textControl.write(*args, **kwargs)


if __name__ == '__main__':
	import locale
	locale.setlocale(locale.LC_ALL, '')

	def oninit(self):
		self.panel = wx.Panel(self, -1)
		self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))

		self.c = TextCtrlWithButtons(
			self.panel,
		)
		#self.c.addBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_TOOLBAR, (16,16)), onLoad)
		#self.c.addBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16)), onLoad)
		#self.c.addBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16,16)), onLoad)
		#self.c.SetEditable(False)

		self.t = wx.TextCtrl(
			self.panel, 
		)

		self.panel.GetSizer().Add(self.c, 0, wx.GROW)
		self.panel.GetSizer().Add(self.t, 0, wx.GROW)

		def f():
			from toolib.wx.debug.dump import dumpWindowSizes
			dumpWindowSizes(self.c)
			dumpWindowSizes(self.t)
		wx.CallAfter(f)
			
	def onLoad(event):
		print event

	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
