#----------------------------------------------------------------------
# Name:         popup
# Purpose:      Generic popup control
#
# Author:       Gerrit van Dyk
#
# Created:      2002/11/20
# Version:      0.1
# RCS-ID:       $Id: PopupControl.py,v 1.30 2012/08/16 11:04:25 oleg Exp $
# License:      wxWindows license
#----------------------------------------------------------------------
# 12/09/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatability update.
#
# 12/20/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxPopupDialog -> PopupDialog
# o wxPopupControl -> PopupControl
#
# 2005-09-28
# o Refined by Oleg Noga
#
# 2007-07
# o Refined by Oleg Noga

import wx
import types
from toolib 		           import debug
from toolib.math.Rect          import Rect
from toolib.event.ListenerList import ListenerList
from toolib.wx.mixin.TWindowUtils import TWindowUtils

##############################################################################
# PopupControl
# 
__super__ = wx.PyControl
class PopupControl(__super__):

	class EventWrapper(object):
		"""
		Used to manually
		wrap event from textControl and override method
		GetEventObject to return PopupControl instance instead
		TextControl
		"""
		def __init__(self, event):
			self._event = event

		def __getattr__(self, name):
			return getattr(self._event, name)

		def GetEventObject(self):
			return self._event.GetEventObject().GetParent()

	BUTTON_TEXT_POP  = "..."
	BUTTON_TEXT_EDITOR  = ">"
	BUTTON_TEXT_NONE = "x"

	def __init__(self, 
		parent,
		id         = -1,
		pos        = wx.DefaultPosition,
		size       = wx.DefaultSize,
		style      = 0,
		validator  = wx.DefaultValidator,
		name       = wx.ControlNameStr,
		popButton  = True,
		noneButton = False,
		editorButton = False,
		popupModal = False,
	):
		__super__.__init__(self, parent, id, pos, size, wx.WANTS_CHARS, validator, name)
		
		self.__textControl = self.CreateTextControl(-1, style | wx.NO_BORDER)
		self.__popupWindow = None
		self.__noneSet = False
		self.__popupModal = popupModal

		self._buttons = []		# buttons from right to left
		self.__buttonsDict = {}

		if editorButton:
			b = EditorButton(self, -1, self.BUTTON_TEXT_EDITOR)
			b.Bind(wx.EVT_BUTTON, self.OnEditButton)
			self._buttons.append(b)
			self.__buttonsDict['editor'] = b

		if noneButton:
			b = EditorButton(self, -1, self.BUTTON_TEXT_NONE)
			b.Bind(wx.EVT_BUTTON, self.OnNoneButton)
			self._buttons.append(b)
			self.__buttonsDict['none'] = b

		if popButton:
			b = EditorButton(self, -1, self.BUTTON_TEXT_POP)
			b.Bind(wx.EVT_BUTTON, self.OnPopupButton)
			self._buttons.append(b)
			self.__textControl.Bind(wx.EVT_CHAR, self.OnChar)
			self.__textControl.Bind(wx.EVT_KEY_DOWN, self.__onKeyDown)
			self.__buttonsDict['popup'] = b

		self.__onSize(None)
		self.Bind(wx.EVT_SIZE, self.__onSize)

		# embedded text control should get focus when control gets
		self.Bind(wx.EVT_SET_FOCUS, self.__onFocus)
		self.__textControl.Bind(wx.EVT_KILL_FOCUS, self.__onKillFocus)

		## this was replaced with DoGetBestSize
		#minw,  minh  = self.__textControl.GetMinSize()
		#maxw,  maxh  = self.__textControl.GetMaxSize()
		#
		## min, max are -1 if it not set by user
		## use -1 width and best height by default
		#if minw  == -1 and minh == -1:
		#	minh = self.__textControl.GetBestSize()[1]
		#
		#if maxw  == -1 and maxh == -1:
		#	maxh = minh
		#
		#buttonsWidth = reduce(lambda sum, b: sum + b.getWidth(), self._buttons, 0)
		#
		#if minw != -1: minw += buttonsWidth
		#if maxw != -1: maxw += buttonsWidth
		#
		#self.SetMinSize((minw, minh))
		#self.SetMaxSize((maxw, maxh))

		# 1 pixel border will the same colour as text control
		super(PopupControl, self).SetBackgroundColour(self.__textControl.GetBackgroundColour())

		self.popupListeners = ListenerList()

	def DoGetBestSize(self):
		w, h = self.__textControl.BestSize

		buttonsWidth = reduce(lambda sum, b: sum + b.getWidth(), self._buttons, 0)

		return w + buttonsWidth, h

	def IsPopupModal(self):
		return self.__popupModal

	def SetPopupModal(self, popupModal):
		self.__popupModal = popupModal

	##########################################################################
	# Overrideables
	#
	def CreateTextControl(self, id, style):
		"""
		Override to set another control as text
		Control must have GetValue, SetValue
		"""
		return wx.TextCtrl(self, id, '', style=style)
		
	def FormatContent(self):
		"""
		This method is called just before the popup is displayed
		Use this method to format any controls in the popup
		"""
		pass

	def CreatePopupWindow(self, title, style):
		"""
		overrideable
		"""
		return PopupWindow(self, title=title, style=style)

	def CreatePopupContent(self, parent, id):
		return None

	##########################################################################
	#
	#
	def GetTextControl(self):
		return self.__textControl

	def GetButton(self, name='popup'):
		"""name is one of popup, none, editor"""
		return self.__buttonsDict[name]
	
	def GetPopupContent(self):
		return self.GetPopupWindow().GetContent()

	def GetPopupWindow(self):
		if self.__popupWindow is None:
			self.__popupWindow = self.CreatePopupWindow("", wx.DEFAULT_FRAME_STYLE)
			content = self.CreatePopupContent(self.__popupWindow, -1)
			if content:
				self.__popupWindow.SetContent(content)
		return self.__popupWindow

	def PopUp(self, forceFocus=False):
		self.GetPopupWindow().PopUp(self.__popupModal, forceFocus)

	def PopDown(self):
		if self.GetPopupWindow():
			self.GetPopupWindow().PopDown()

	def Enable(self, enabled=True):
		"""
		will not enable subwidgets, disabled by EnableButton
		"""
		#wx.PyControl.Enable(self, enabled)
		self.__textControl.Enable(enabled)
		for button in self._buttons:
			button.Enable(enabled and getattr(button, '_button_enabled_', True))


	def EnableButton(self, enabled = True, name = 'popup'):
		"""
		this method is stronger than Enable method
		if button disabled, ontly this method will enable it again
		"""
		button = self.GetButton(name)
		button._button_enabled_ = enabled
		button.Enable(enabled)

	##########################################################################
	# Event handlers
	#
	def OnChar(self, event):
		if event.GetKeyCode() == wx.WXK_DOWN:
			self.PopUp(forceFocus=True)
		elif event.GetKeyCode() == wx.WXK_UP:
			self.PopDown()
		else:
			event.Skip()

	def __onKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.PopDown()
		else:
			event.Skip()

	def OnEditButton(self, evt):
		# focus is on button so we must set it to text control
		# so focus will return to text control after popup closes
		self.__textControl.SetFocus()
		self.popupListeners.fireEvent(self, 'onEdit')

	def OnPopupButton(self, evt):
		# focus is on button so we must set it to text control
		# so focus will return to text control after popup closes
		self.__textControl.SetFocus()
		self.PopUp(forceFocus=True)

	def OnNoneButton(self, evt):
		self.__textControl.SetFocus()
		self.SetValue(None)

	def __onFocus(self, evt):
		"""embedded text control should get focus when control gets"""
		self.__textControl.SetFocus()
		self.__textControl.SetSelection(-1,-1)
		evt.Skip()

	def __onKillFocus(self, evt):
		"""popdown when embeded text control looses focus"""

		popdown = True
		
		# do not popdown if focus gone to child window (to popup content)
		w = wx.Window.FindFocus()
		while w is not None:
			w = w.GetParent()
			if w is self:
				popdown = False
				break

		if popdown:
			self.PopDown()

		evt.Skip()

	def __onSize(self,evt):
		w,h = self.GetClientSize()
		for b in self._buttons:
			w -= b.getWidth()
			b.SetDimensions(w, 0, b.getWidth(), h)

		# cosmetical fix for windows: text control have no border
		# so shift it 1 pixel down-right
		shift = 1
		self.__textControl.SetDimensions(shift, shift, w-shift, h-shift)

	###################################################
	# Event handler fix
	#
	#def PushEventHandler(self, handler):
	#	assert debug.trace("PushEventHandler(%s)" % (handler,))
	#	self.__textControl.PushEventHandler(handler)

	#def PopEventHandler(self, delete):
	#	assert debug.trace("PopEventHandler(%s)" % (delete,))
	#	self.__textControl.PopEventHandler(False)

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
		super(PopupControl, self).SetBackgroundColour(colour)
		self.__textControl.SetBackgroundColour(colour)

	#######################################################################
	# TextCtrl delegation
	#
	def SetValue(self, value):
		"""
		set value to text control and
		remember if none was set
		"""
		self.__noneSet = value is None
		self.__textControl.SetValue(value or "")
	
	def GetValue(self):
		"""
		return None if None was set and empty string
		"""
		value = self.__textControl.GetValue()
		if value == "" and self.__noneSet:
			return None
		else:
			return value

	def SetToolTipString(self, *args, **kwargs):
		return self.__textControl.SetToolTipString(*args, **kwargs)

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

	#defined above
	#def GetValue(self, *args, **kwargs):
	#	return self.__textControl.GetValue(*args, **kwargs)

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

	#defined above
	#def SetValue(self, *args, **kwargs):
	#	return self.__textControl.SetValue(*args, **kwargs)

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

##############################################################################
# Button
# 
class EditorButton(wx.Button):
	WIDTH = 16

	def __init__(self, parent, id, text):
		wx.Button.__init__(self, parent, id, text, style=wx.NO_BORDER)

	def getWidth(self):
		return self.WIDTH

##############################################################################
# PopupWindow
# 
PopupWindowBase = wx.MiniFrame
class PopupWindow(PopupWindowBase, TWindowUtils):
	"""
	Must have at list 
		PopDown
		PopUp
	"""
	def __init__(self, *p, **pp):
		PopupWindowBase.__init__(self, *p, **pp)
		self._content = None
		self.SetSizer(wx.BoxSizer())
		self.Bind(wx.EVT_CLOSE, lambda event: self.PopDown())

		#topLevelParent = self.GetParent()
		#while not isinstance(topLevelParent, wx.TopLevelWindow):
		#	topLevelParent = topLevelParent.GetParent()

		# since modeless window pops down on deactivation
		# we do not need to follow parent window
		for window in (self,): #topLevelParent):
			window.Bind(wx.EVT_MOVE, self.__positionOnParent)
			window.Bind(wx.EVT_SIZE, self.__positionOnParent)

		self.__poppedUp = False
		self.__madeModal = False

	def __on_activate(self, event):
		if not event.GetActive():
			# purpose is not to popdown parent window if window has shown toplevel child
			popdown = True
			for w in self.iterWindowsRecursive(filterFn = lambda w: isinstance(w, wx.TopLevelWindow) and w is not self):
				#rint w, w.GetTitle(), w.IsShown()
				if w.IsShown():
					popdown = False
					break
			
			if popdown:
				wx.CallAfter(self.PopDown)
		event.Skip()

	def __positionOnParent(self, event):
		if self.IsShown():
			wx.CallAfter(self.PositionOnParent)
		event.Skip()

	def SetContent(self, content):
		if self._content is not content:
			
			if self._content:
				self.GetSizer().Remove(self._content)
				self._content.Destroy()

			self._content = content

			if self._content is not None:
				if self._content.GetParent() is not self:
					self._content.Reparent(self)
				self.GetSizer().Add(self._content, 1, wx.EXPAND)

	def GetContent(self):
		return self._content

	def __calcOnScreenArea(self, pos, size):
		swidth  = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
		sheight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

	def _getBoundingRect(self):
		"""
		must return screen rect except taskbar
		"""
		#screenRect = Rect((0,0), (
		#	wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X), 
		#	wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y),
		#))
		global __boundingRect
		try:
			return __boundingRect
		except NameError:
			# only known way is to measure temporary maximized window rect
			# doing once a session
			f = wx.Frame(self, -1, style=0)
			f.Maximize()
			__boundingRect = Rect(f.Position, f.Size)
			f.Destroy()
			return __boundingRect

	def PositionOnParent(self):
		if 0:
			# old algorithm
			parentSize = self.GetParent().GetSize()
			pos = self.GetParent().ClientToScreen((parentSize.width-1, parentSize.height-1))
			pos.x -= self.GetSize().width
			if pos.x < 0:
				pos.x = 0
			self.Move(pos)
			return

		parentRect = Rect(self.GetParent().ClientToScreen((0, 0)), self.GetParent().Size)

		rects = []
		for position in [
			lambda parent, size: Rect((parent.right() - size.width, parent.bottom()),            size),  # bottom right
			lambda parent, size: Rect((parent.right() - size.width, parent.pos.y - size.height), size),  # top right
		]:
			rect = position(parentRect, self.Size)
			if rect.pos.x < 0:	rect.pos.x = 0	     # can shift window right if not fits
			rects.append(rect.intersect(self._getBoundingRect())) # cut what not fits
		
		rect = max(rects, key=lambda rect: rect.area()) # select first rect with biggest area

		self.SetEvtHandlerEnabled(False)
		self.SetDimensions(*(tuple(rect.pos)+tuple(rect.size)))
		self.SetEvtHandlerEnabled(True)

	def PopUp(self, modal=True, forceFocus=False):
		self.GetParent().FormatContent()
	
		# fit only before first popup
		if not self.__poppedUp:
			self.Fit()

		# parent may be moved, hidden window not follows parent
		# position before show
		self.PositionOnParent()

		self.GetParent().popupListeners.fireEvent(self.GetParent(), 'beforePopup')

		# beforePopup can add content so bind ESC listeners as late as possible
		# do it only before first popup
		if not self.__poppedUp:
			self.Bind(wx.EVT_ACTIVATE, self.__on_activate)
			bind_recursive(self, wx.EVT_KEY_DOWN, self.__onKeyDown)

		if modal:
			print "* MakeModal is buggy, in chain <Frame> -> <Modal Dialog> -> <This Frame>, <Frame> can receive WM_ENABLE, so <Modal Dialog> will become modeless at this moment"
			self.MakeModal(True)
			self.__madeModal = True

		self.Show(True)

		# do not set focus to modeless window
		if (modal or forceFocus) and self.GetContent():
			self.GetContent().SetFocus()

		self.__poppedUp = True
		self.GetParent().popupListeners.fireEvent(self.GetParent(), 'afterPopup')

	def PopDown(self):
		#PopupWindowBase.EndModal(self, 0)
		self.GetParent().popupListeners.fireEvent(self.GetParent(), 'beforePopdown')
		
		# MakeModal is buggy, avoid call
		if self.__madeModal:
			self.MakeModal(False)
			self.__madeModal = False
		
		self.Show(False)
		self.GetParent().popupListeners.fireEvent(self.GetParent(), 'afterPopdown')

	def __onKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			#rint "PopDown from", event.GetEventObject().__class__.__name__
			self.PopDown()
		else:
			event.Skip()

def bind_recursive(window, evt, handler):
	#if isinstance(window, wx.Control):
	
	window.Bind(evt, handler, window)
	
	for i in window.GetChildren():
		bind_recursive(i, evt, handler)

if __name__ == '__main__':
	import DateControl
	DateControl.test()
