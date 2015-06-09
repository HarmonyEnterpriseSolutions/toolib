import wx
from XIterItems import XIterItems

class XCustomTreeColumns(XIterItems):

	"""
	Input:
		OnPaint
		PaintItem

	Output:
		getColumnCount
		paintColumn

	"""


	def __init__(self, *args, **kwargs):
		super(XCustomTreeColumns, self).__init__(*args, **kwargs)
		self.__x = None
		#window = self.GetMainWindow() if hasattr(self, 'GetMainWindow') else self
		#window.Bind(wx.EVT_PAINT, self.__onPaint, window)

	def getColumnsBaseX(self):
		if self.__x is None:
			self.__x = 0
			for item in self.iterItemsRecursive(stopFn=lambda item: not item.IsExpanded()):
				self.__x = max(self.__x, item.GetX() + item.GetWidth())
			self.__x += 1
		return self.__x

	#def __onPaint(self, event):
	#	self.__x = None
	#	self.getColumnsBaseX()
	#	event.Skip()

	def OnPaint(self, event):
		"""Handles the wx.EVT_PAINT event."""
		self.__x = None
		self.getColumnsBaseX()
		return super(XCustomTreeColumns, self).OnPaint(event)

	def PaintItem(self, item, dc, *args, **kwargs):
		super(XCustomTreeColumns, self).PaintItem(item, dc, *args, **kwargs)

		rect = wx.Rect(
			self.__x,
			item.GetY(),
			0,
			self.GetLineHeight(item),
		)

		xRight = self.ClientSize[0] - 1

		for col in xrange(self.getColumnCount()):
			w = self.getColumnWidth(col)
			rect.Width = min(w, max(xRight - rect.X, 0))
			if rect.Width > 0:
				self.paintCell(dc, item, col, rect)
				rect.Offset((w, 0))
			else:
				break


