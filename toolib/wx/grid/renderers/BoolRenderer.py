import wx
import os
from ImageCellRenderer import ImageCellRenderer

class BoolRenderer(ImageCellRenderer):

	_bitmaps = {}

	def getBitmap(self, grid, row, col):
		value = grid.GetTable().GetValue(row, col)
	
		bitmap = self._bitmaps.get(value)

		if bitmap is None:
			
			if value is None or value == '':
				name = 'bool_none.bmp'
			elif value:
				name = 'bool_true.bmp'
			else:
				name = 'bool_false.bmp'

			bitmap = wx.Bitmap(os.path.join(os.path.abspath(os.path.split(__file__)[0]), name))

			self._bitmaps[value] = bitmap

		return bitmap