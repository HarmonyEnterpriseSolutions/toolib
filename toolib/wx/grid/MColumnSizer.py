import wx

"""
TODO: disable scrollbar if columns size == grid size
"""

class MColumnSizer(object):
	"""
	Does nothing
	"""

	def __init__(self):
		self.Bind(wx.EVT_SIZE, self.__onSize)
		self.Bind(wx.grid.EVT_GRID_COL_SIZE, self.__onSize)

	def __onSize(self, event):
		if self.GetNumberCols() > 0:
			self.adjustColSizes()
			self.GetGridColLabelWindow().Refresh()
		event.Skip()

	def adjustColSizes(self):
		pass


class MColumnSizer_oneGrows(MColumnSizer):
	"""
	Changes size of one column to fit client

	Requires:
		Bind
		GetClientSize
		GetColLabelSize
		GetColSize
		GetGridColLabelWindow
		GetNumberCols
		SetColSize
	"""

	MIN_WIDTH = 20
	WIDTH_CORRECTION = 0

	def __init__(self, columnIndex):
		MColumnSizer.__init__(self)
		self._columnIndex = columnIndex

	def adjustColSizes(self):
		clientWidth = self.GetClientSize()[0]
		width = clientWidth - self.GetRowLabelSize() + self.WIDTH_CORRECTION

		index = (self._columnIndex + self.GetNumberCols()) % self.GetNumberCols()

		for i in xrange(self.GetNumberCols()):
			if i != index:
				width -= self.GetColSize(i)

		self.SetColSize(index, max(self.MIN_WIDTH, width))


class MColumnSizer_rightGrows(MColumnSizer_oneGrows):
	"""
	Changes size of right column to fit client
	"""

	def __init__(self):
		MColumnSizer_oneGrows.__init__(self, -1)
