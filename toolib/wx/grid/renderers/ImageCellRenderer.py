import wx
import wx.grid

class ImageCellRenderer(wx.grid.PyGridCellRenderer):

	BACKGROUND_SELECTED	= None
	BACKGROUND			= None


	def __init__(self):
		if self.__class__.BACKGROUND_SELECTED is None: 
			self.__class__.BACKGROUND_SELECTED = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
		if self.__class__.BACKGROUND is None: 
			self.__class__.BACKGROUND = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)

		wx.grid.PyGridCellRenderer.__init__(self)
		self.__brushes = {}
		self._res = (
			(
				self._getBrush(self.BACKGROUND), 
				wx.Pen(self.BACKGROUND, 0, wx.SOLID), 
			),
			(
				self._getBrush(self.BACKGROUND_SELECTED), 
				wx.Pen(self.BACKGROUND_SELECTED, 0, wx.SOLID),
			),
		)
		self._cache = None

	def _getBrush(self, colour):
		key = tuple(colour)
		brush = self.__brushes.get(key)
		if brush is None:
			self.__brushes[key] = brush = wx.Brush(colour, wx.SOLID)
		return brush
	
	def getBitmap(self, grid, row, col):
		if self._cache is None:
			self._cache = grid.getResources().getBitmapCache()
		return self._cache.get(grid.GetTable().GetValue(row, col))

	def Draw(self, grid, attr, dc, rect, row, col, isSelected):

		brush, pen = self._res[isSelected]

		if not isSelected:
			brush = self._getBrush(attr.GetBackgroundColour())
		
		dc.SetBackgroundMode(wx.SOLID)
		dc.SetBrush(brush)
		dc.SetPen(pen)
		dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

		dc.SetClippingRect(rect)

		bmp = self.getBitmap(grid, row, col)
		if bmp is not None:
			dc.DrawBitmap(
				bmp, 
				rect.x + (rect.width - bmp.GetWidth()) / 2 + 1, 
				rect.y + (rect.height - bmp.GetHeight()) / 2 + 1, 
				True
			)

		dc.DestroyClippingRegion()
