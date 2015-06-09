"""
Abstract Editor for control
"""

import wx.grid
from toolib._	import *
from toolib		import debug

super = wx.PyControl
class TestControl(wx.PyControl):
	
	def __init__(self, *args, **kwargs):
		"""
		additional arguments:
			noneButton = False
		"""

		super.__init__(self, *args, **kwargs)
		
		self._textCtrl = self.CreateTextControl(-1)

		self.OnSize(None)
		self.Bind(wx.EVT_SIZE, self.OnSize)

		# embedded control should get focus on TAB keypress
		self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)

	def CreateTextControl(self, id):
		"""
		Override to set another control as text
		Control must have GetValue, SetValue
		"""
		return wx.TextCtrl(self, id, '', style=wx.NO_BORDER)
		
	def OnFocus(self, evt):
		self._textCtrl.SetFocus()
		evt.Skip()

	def OnSize(self,evt):
		x,h = self.GetClientSize()
		self._textCtrl.SetDimensions(0,0,x,h)

	def EmulateKeyPress(self, evt):
		return self._textCtrl.EmulateKeyPress(evt)

	def SetInsertionPointEnd(self):
		return self._textCtrl.SetInsertionPointEnd()

	def SetSelection(self, p1, p2):
		return self._textCtrl.SetSelection(p1, p2)

	def GetLastPosition(self):
		return self._textCtrl.GetLastPosition()

	#def PushEventHandler(self, handler):
	#	debug.trace("PushEventHandler(%s)" % (handler,))
	#	return self._textCtrl.PushEventHandler(handler)

	def PopEventHandler(self, delete):
		debug.trace("PopEventHandler(%s)" % (delete,))
		return self._textCtrl.PopEventHandler(delete)

	def Destroy(self):
		debug.trace('TestControl.Destroy')
		super.Destroy(self)


class TestCellEditor(wx.grid.PyGridCellEditor):
	"""
	"""
	def __init__(self):
		wx.grid.PyGridCellEditor.__init__(self)
		self._startValue = None
		self._editStarted = False

		
	##########################################################################
	# Implementation
	#
	def Create(self, parent, id, evtHandler):
		"""
		Called to create the control, which must derive from wxControl.
		"""
		debug.trace("Create")
		self.SetControl(TestControl(parent, id))
		self.GetControl().PushEventHandler(evtHandler)

	def SetSize(self, rect):
		"""
		Called to position/size the edit control within the cell rectangle.
		If you don't fill the cell (the rect) then be sure to override
		PaintBackground and do something meaningful there.
		"""
		debug.trace("SetSize(%s)" % (rect,))
		self.GetControl().SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2, wx.SIZE_ALLOW_MINUS_ONE)

	def IsAcceptedKey(self, evt):
		"""
		Return True to allow the given key to start editing: the base class
		version only checks that the event has no modifiers.  F2 is special
		and will always start the editor.
		"""
		debug.trace("IsAcceptedKey: %d" % (evt.GetKeyCode()))
		## Oops, there's a bug here, we'll have to do it ourself..
		return (    not evt.ControlDown()
				and not evt.AltDown()
				and	evt.GetKeyCode() != wx.WXK_SHIFT
		)

	def Clone(self):
		"""
		Create a new object which is the copy of this one
		"""
		# TODO: initargs here (like pickle)
		return self.__class__()

	def BeginEdit(self, row, col, grid):
		"""
		Fetch the value from the table and prepare the edit control
		to begin editing.  Set the focus to the edit control.
		"""
		debug.trace("BeginEdit(%d, %d)" % (row, col))
		self.GetControl().SetFocus()

	def EndEdit(self, row, col, grid):
		"""
		Complete the editing of the current cell. Returns True if the value
		has changed.  If necessary, the control may be destroyed.
		"""
		debug.trace("EndEdit(%d, %d)" % (row, col))

	def Reset(self):
		"""
		Reset the value in the control back to its starting value.
		*Must Override*
		"""
		debug.trace("Reset")

	def Destroy(self):
		#Does not goes, this is a wx-Python bug!
		debug.trace("Destroy called! Bug is fixed!", level=0)
		wx.grid.PyGridCellEditor.Destroy(self)
