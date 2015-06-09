import wx
import wx.grid
from toolib._ import *

__super__ = wx.grid.PyGridCellRenderer
class TextCellRenderer(__super__):

	INDENT = 2
	COLOR_ERROR = wx.RED

	def __init__(self, strfunc=None, align=None):
		__super__.__init__(self)
		self._strfunc = strfunc or self.strfunc
		self._align = align

	def strfunc(self, value):
		if value is None:
			return ""
		else:
			return str(value)

	def getAlign(self):
		return self._align

	def setAlign(self, align):
		self._align = align

	def getValueAsTextAndColor(self, grid, row, col):
		"""
		Overrideable
		"""
		try:
			return self._strfunc(grid.GetTable().GetValue(row, col)), None
		except Exception, e:
			return "%s: %s: %s" % (_("Error"), e.__class__.__name__, e), self.COLOR_ERROR


	def Draw(self, grid, attr, dc, rect, row, col, isSelected):
		"""
		Here we draw text in a grid cell using various fonts
		and colors.

		Horizontal alignment will be one of wx.ALIGN_LEFT, wx.ALIGN_CENTRE or wx.ALIGN_RIGHT. 
		Vertical alignment will be one of wx.ALIGN_TOP, wx.ALIGN_CENTRE or wx.ALIGN_BOTTOM.

		Note: overflow is not supported 
		"""
		text, color = self.getValueAsTextAndColor(grid, row, col)

		# grey out fields if the grid is disabled
		if grid.IsEnabled():
			if isSelected:
				dc.SetBrush(wx.Brush(grid.GetSelectionBackground(), wx.SOLID))
				dc.SetTextBackground(grid.GetSelectionBackground())
				dc.SetTextForeground(grid.GetSelectionForeground())
			else:
				dc.SetBrush(wx.Brush(attr.GetBackgroundColour(), wx.SOLID))
				dc.SetTextBackground(attr.GetBackgroundColour())
				dc.SetTextForeground(color or attr.GetTextColour())
		else:
			dc.SetBrush(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE), wx.SOLID))
			dc.SetTextBackground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
			dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

		dc.SetBackgroundMode(wx.SOLID)
		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.DrawRectangle(*rect.Get())

		dc.SetBackgroundMode(wx.TRANSPARENT)
		dc.SetFont(attr.GetFont())

		rect.Deflate(self.INDENT, 0)
		grid.DrawTextRectangle(dc, text, rect, *(self._align or attr.GetAlignment()))

