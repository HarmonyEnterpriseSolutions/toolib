from TScrollTranslation import TScrollTranslation


class GridHitSpace(Exception):	
	pass


class THitTest(TScrollTranslation):
	"""
	Adds hit testing functionality to Grid

	Requires:
		GetNumberRows
		GetNumberCols

		GetRowSize
		GetColSize

		CalcUnscrolledPosition
		CalcScrolledPosition

	Provides:
		hitTest
		
		ScrollTranslation.*

	"""
	def __hitTest(self, hitx, cellCount, getCellSize, leftIndent=0, rightIndent=0):
		"""
		indents can be negative
		"""
		x = 0
		if hitx < 0:
			return -1

		if cellCount > 0:
			if leftIndent < 0:	lindent = max(0, getCellSize(0) + leftIndent)
			else:				lindent = leftIndent

			if hitx < lindent:
				raise GridHitSpace, "indent"
		
			for i in xrange(cellCount):
				x += getCellSize(i)

				if leftIndent < 0:	
					if i < cellCount-1:
						lindent = max(0, getCellSize(i+1) + leftIndent)
					else:
						lindent = 0
				else:
					lindent = leftIndent

				if rightIndent < 0:
					if i > 0:
						rindent = max(0, getCellSize(i-1) + rightIndent)
					else:
						rindent = 0
				else:				
					rindent = rightIndent

				if hitx >= x - rindent and hitx < x + lindent:
					raise GridHitSpace, "indent"
					
				if hitx < x: 
					return i

		raise GridHitSpace, "space"

	def hitTest(self, pos, leftIndent=0, rightIndent=0, topIndent=0, bottomIndent=0, window=None):
		"""
		Returns row, col
		raises Grid.GridSpaceHit

		pos = (0, 0) is origin of grid window
		if window provided pos[0] or/and pos[1] is not used (-1 returned)

		pos is phisical position
		"""
		pos = self.calcUnscrolledPosition(pos)

		y = lambda: self.__hitTest(pos[1], self.GetNumberRows(), self.GetRowSize, topIndent, bottomIndent)
		x = lambda: self.__hitTest(pos[0], self.GetNumberCols(), self.GetColSize, leftIndent, rightIndent)

		if window == self.GetGridColLabelWindow():
			return (-1, x())
		elif window == self.GetGridRowLabelWindow():
			return (y(), -1)
		elif window == self.GetGridCornerLabelWindow():
			return (-1, -1)
		else:
			return (y(), x())
