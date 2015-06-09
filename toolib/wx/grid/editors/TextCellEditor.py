import wx
import types
from AbstractCellEditor import AbstractCellEditor
from toolib.wx.event.KeyEventEx import KeyEventEx

class TextCellEditor(AbstractCellEditor):
	def __init__(self):
		AbstractCellEditor.__init__(self)

	##########################################################################
	# Methods to override
	#
	def getValueAsText(self, grid, row, col):
		value = grid.GetTable().GetValue(row, col)
		assert isinstance(value, types.StringTypes) or value is None, 'Invalid value type: %s' % type(value)
		return value or ""

	def setValueAsText(self, grid, row, col, value):
		grid.GetTable().SetValue(row, col, value.rstrip() or None)

	##########################################################################

	def StartingKey(self, event):
		"""
		If the editor is enabled by pressing keys on the grid, this will be
		called to let the editor do something about that first key if desired.

		Since this is now happening in the EVT_CHAR event EmulateKeyPress is no
		longer an appropriate way to get the character into the text control.
		Do it ourselves instead.  We know that if we get this far that we have
		a valid character, so not a whole lot of testing needs to be done.
		"""
		tc = self.GetControl()
		code = event.GetKeyCode()

		#from toolib.wx.debug.dump import dump
		#rint dump(event)

		if code in (wx.WXK_DELETE, wx.WXK_BACK):
			tc.SetValue("")
		else:
			char = KeyEventEx.getChar(event)
			if char is not None:
				tc.WriteText(char)

	def createControl(self, parent, id):
		return wx.TextCtrl(parent, id, style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)

	def startEdit(self, grid, row, col):
		return self.getValueAsText(grid, row, col)
	
	def setControlValue(self, value):
		c = self.GetControl()
		c.SetValue(value)
		c.SetInsertionPointEnd()
		c.SetSelection(0, c.GetLastPosition())

	def stopEdit(self, grid, row, col):
		"""
		get control value and set to grid
		"""
		value = self.GetControl().GetValue()
		if value != self.getStartValue():
			self.setValueAsText(grid, row, col, value)
			return True
		return False

	def cleanControl(self):
		self.GetControl().SetValue("")


class MultiLineTextCellEditor(TextCellEditor):

	def __init__(self, cellHeight = 58):
		TextCellEditor.__init__(self, style=wx.TE_MULTILINE)
		self._cellHeight = cellHeight

	def getCellHeight(self):
		return self._cellHeight
