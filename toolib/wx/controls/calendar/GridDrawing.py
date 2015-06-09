import wx
from CellAttributes import CellAttributes
import operator

class GridDrawing(object):

	def __init__(self, rows, cols, cellAttributesDict=None):
		self.__rows = rows
		self.__cols = cols
		self.__cellAttributes = cellAttributesDict or {}
		self.__defaultCellAttributes = self.__cellAttributes.get('default') or CellAttributes()
		self.__rowWeight = {}

		self.__xWeight = None
		self.__yWeight = None

		self.__minHeight = None
		self.__maxHeight = None

		self.__minWidth = None
		self.__maxWidth = None

		self.__x = None
		self.__y = None

	def getCellAttributes(self):
		return self.__cellAttributes
	
	def _getCellAttributes(self, flags):
		l = [self.__cellAttributes[flag] for flag in flags]
		a = self.__defaultCellAttributes
		if l:
			a = a.merge(l)
		return a

	def draw(self, dc, rect, cells=None):
		if self.__yWeight is None:
			atts = [self._getCellAttributes(self.getCellFlagsAndText(row, 0)[0]) for row in xrange(self.__rows)]
			self.__minHeight = [a.minHeight if a.minHeight is not None else 0     for a in atts]
			self.__maxHeight = [a.maxHeight if a.maxHeight is not None else 1<<16 for a in atts]
			self.__yWeight   = [a.yWeight or 1. for a in atts]

		if self.__xWeight is None:
			atts = [self._getCellAttributes(self.getCellFlagsAndText(0, col)[0]) for col in xrange(self.__cols)]
			self.__minWidth = [a.minWidth if a.minWidth is not None else 0     for a in atts]
			self.__maxWidth = [a.maxWidth if a.maxWidth is not None else 1<<16 for a in atts]
			self.__xWeight  = [a.xWeight or 1. for a in atts]

		oldy = rect.y
		y = float(rect.y)
		self.__y = []
		self.__x = []

		height = rect.height

		for row in xrange(self.__rows):

			h = (rect.height - y) / reduce(operator.add, self.__yWeight[row:], 0.) * self.__yWeight[row]

			if h < self.__minHeight[row]:
				height -= self.__minHeight[row] - h # reduce overal height
				h = self.__minHeight[row]

			if h > self.__maxHeight[row]:
				height -= self.__maxHeight[row] - h # add overal height
				h = self.__maxHeight[row]

			y += h
			iy = int(round(y))

			self.__y.append(iy)

			oldx = rect.y
			x = float(rect.x)

			for col in xrange(self.__cols):

				if len(self.__x) < self.__cols:
					
					w = (rect.width - x) / reduce(operator.add, self.__xWeight[col:], 0.) * self.__xWeight[col]

					if w < self.__minWidth[col]:
						w = self.__minWidth[col]

					if w > self.__maxWidth[col]:
						w = self.__maxWidth[col]

					x += w
					ix = int(round(x))
					self.__x.append(ix)
				else:
					ix = self.__x[col]
				
				if cells is None or (row, col) in cells:

					self.drawCell(dc, row, col, wx.Rect(oldx, oldy, ix - oldx, iy - oldy))

				oldx = ix
			oldy = iy
			
	def drawCell(self, dc, row, col, rect):
		flags, text = self.getCellFlagsAndText(row, col)
		self._getCellAttributes(flags).drawCell(dc, rect, text)
		
	def getCellFlagsAndText(self, row, col):
		return (), "Cell %s,%s" % (row, col)

	def hitCellTest(self, pos):
		if self.__x is None or self.__y is None:
			return None

		x, y = pos
		col = None
		for i, ix in enumerate(self.__x):
			if x < ix:
				col = i
				break

		row = None
		for i, iy in enumerate(self.__y):
			if y < iy:
				row = i
				break
			
		if row is not None and col is not None:
			return row, col


if __name__ == '__main__':
	from Calendar import test
	test()
