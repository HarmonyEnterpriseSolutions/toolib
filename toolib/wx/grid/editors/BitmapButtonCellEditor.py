from toolib import debug
import wx

from AbstractCellEditor import AbstractCellEditor

class BitmapButtonCellEditor(AbstractCellEditor):

	def __init__(self, choices=None, strfunc=None, setfunc=None):
		AbstractCellEditor.__init__(self)

	def createControl(self, parent, id):
		return wx.BitmapButton(parent, id, style=wx.NO_BORDER)

	def startEdit(self, grid, row, col):
		#rint "startEditor", grid.GetTable().GetValue(row, col)
		try:
			actionName, imageName = grid.GetTable().GetValue(row, col).split(':')
		except:
			debug.error("button editor expects value '<table action>:<bitmap name>'")
		else:
			self.GetControl().SetBitmapLabel(grid.getResources().getBitmapCache().get(imageName))

			try:
				method = getattr(grid, "on" + actionName[0].upper() + actionName[1:])
			except AttributeError, e:
				debug.error('Grid has no method: %s' % e)
			else:
				grid.Bind(wx.EVT_BUTTON, method, self.GetControl())

	def stopEdit(self, grid, row, col):
		"""
		get control value and set to grid
		"""

		#here to unbind button
		grid.Unbind(wx.EVT_BUTTON, self.GetControl())
		return True

	def SetSize(self, rect):
		"""
		Called to position/size the edit control within the cell rectangle.
		If you don't fill the cell (the rect) then be sure to override
		PaintBackground and do something meaningful there.
		"""
		self.GetControl().SetDimensions(rect.x+2, rect.y+2, rect.width-1, rect.height-1)
